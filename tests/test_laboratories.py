import numpy as np
import pytest

from pdi_lab.functions import (
    MEAN_KERNEL_3X3,
    SOBEL_X_KERNEL,
    SOBEL_Y_KERNEL,
    adjust_brightness,
    adjust_contrast,
    apply_convolution,
    calculate_histogram,
    copy_image_pixel_by_pixel,
    grayscale_average,
    grayscale_weighted,
    negative_image,
    quantize_image,
    read_kernel,
    split_channels,
    threshold_image,
)


def test_copy_channel_split_and_grayscale():
    image = np.array(
        [
            [[10, 20, 30], [40, 50, 60]],
            [[70, 80, 90], [250, 255, 0]],
        ],
        dtype=np.uint8,
    )

    assert np.array_equal(copy_image_pixel_by_pixel(image), image)

    blue, green, red = split_channels(image)
    assert blue[0, 0].tolist() == [10, 0, 0]
    assert green[0, 0].tolist() == [0, 20, 0]
    assert red[0, 0].tolist() == [0, 0, 30]

    assert int(grayscale_average(image)[0, 0]) == 20
    assert int(grayscale_weighted(image)[0, 0]) == 22


def test_quantization_with_different_levels():
    gradient = np.arange(256, dtype=np.uint8).reshape(1, 256)

    for levels in (16, 8, 4, 2):
        result = quantize_image(gradient, levels)
        assert len(np.unique(result)) == levels

    extremes = np.array([[0, 255]], dtype=np.uint8)
    assert quantize_image(extremes, 2).tolist() == [[0, 255]]

    with pytest.raises(ValueError):
        quantize_image(np.array([[128]], dtype=np.uint8), 1)


def test_point_operations():
    image = np.array([[0, 50, 128, 200, 255]], dtype=np.uint8)

    assert adjust_brightness(image, 50).tolist() == [[50, 100, 178, 250, 255]]
    assert adjust_brightness(image, -50).tolist() == [[0, 0, 78, 150, 205]]
    assert adjust_contrast(image, 1.0).tolist() == image.tolist()
    assert negative_image(image).tolist() == [[255, 205, 127, 55, 0]]
    assert threshold_image(image, 128).tolist() == [[0, 0, 255, 255, 255]]


def test_histogram_and_invalid_parameters():
    image = np.array([[0, 0, 255]], dtype=np.uint8)
    histogram = calculate_histogram(image)

    assert len(histogram) == 256
    assert histogram[0] == 2
    assert histogram[255] == 1
    assert sum(histogram) == 3

    with pytest.raises(ValueError):
        adjust_contrast(np.array([[128]], dtype=np.uint8), -0.1)

    with pytest.raises(ValueError):
        threshold_image(np.array([[128]], dtype=np.uint8), 300)


def test_identity_convolution_and_constant_image():
    identity = [[0, 0, 0], [0, 1, 0], [0, 0, 0]]
    image = np.arange(25, dtype=np.uint8).reshape(5, 5)
    response = apply_convolution(image, identity, "replicate")
    assert np.array_equal(response, image.astype(float))

    constant = np.full((5, 5), 100, dtype=np.uint8)
    response = apply_convolution(constant, MEAN_KERNEL_3X3, "replicate")
    assert np.allclose(response, 100.0)


def test_borders_kernel_file_and_guards(tmp_path):
    image = np.arange(25, dtype=np.uint8).reshape(5, 5)
    result = apply_convolution(image, MEAN_KERNEL_3X3, "copy")
    assert result[0, 0] == image[0, 0]
    assert result[4, 4] == image[4, 4]

    kernel_file = tmp_path / "kernel.txt"
    kernel_file.write_text("3 3\n0 0 0\n0 1 0\n0 0 0\n", encoding="utf-8")
    assert read_kernel(kernel_file).shape == (3, 3)

    with pytest.raises(ValueError):
        apply_convolution(np.zeros((3, 3), dtype=np.uint8), [[1, 1], [1, 1]])

    with pytest.raises(ValueError):
        apply_convolution(np.zeros((3, 3), dtype=np.uint8), [[1]], "invalid")


def test_sobel_on_vertical_and_horizontal_steps():
    vertical_step = np.zeros((7, 7), dtype=np.uint8)
    vertical_step[:, 4:] = 255

    horizontal_step = np.zeros((7, 7), dtype=np.uint8)
    horizontal_step[4:, :] = 255

    gx_vertical = apply_convolution(vertical_step, SOBEL_X_KERNEL, "replicate")
    gy_vertical = apply_convolution(vertical_step, SOBEL_Y_KERNEL, "replicate")
    gx_horizontal = apply_convolution(horizontal_step, SOBEL_X_KERNEL, "replicate")
    gy_horizontal = apply_convolution(horizontal_step, SOBEL_Y_KERNEL, "replicate")

    assert np.max(np.abs(gx_vertical)) > 0
    assert np.max(np.abs(gy_vertical)) == 0
    assert np.max(np.abs(gy_horizontal)) > 0
    assert np.max(np.abs(gx_horizontal)) == 0
