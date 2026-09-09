import argparse
import sys
from pathlib import Path

from .functions import (
    LAPLACIAN_KERNEL_3X3,
    MEAN_KERNEL_3X3,
    MEAN_KERNEL_5X5,
    SOBEL_X_KERNEL,
    SOBEL_Y_KERNEL,
    WEIGHTED_MEAN_KERNEL_3X3,
    absolute_matrix_to_uint8,
    adjust_brightness,
    adjust_contrast,
    apply_convolution,
    calculate_histogram,
    calculate_sobel_magnitudes,
    copy_image_pixel_by_pixel,
    grayscale_average,
    grayscale_weighted,
    inspect_image,
    matrix_to_uint8,
    negative_image,
    quantize_image,
    read_image,
    read_kernel,
    resolve_output_path,
    sharpen_with_laplacian,
    split_channels,
    threshold_image,
    write_histogram,
    write_image,
    write_matrix_csv,
)


OPERATIONS = (
    "inspect",
    "copy",
    "channel_b",
    "channel_g",
    "channel_r",
    "grayscale_average",
    "grayscale_weighted",
    "quantize",
    "brightness",
    "contrast",
    "negative",
    "threshold",
    "histogram",
    "convolution",
    "mean_filter",
    "weighted_mean",
    "laplacian",
    "sobel",
)


def build_parser():
    parser = argparse.ArgumentParser(
        description="M1.1, M1.2 and M1.3 image processing laboratories"
    )
    parser.add_argument("--input", required=True, help="Input image path")
    parser.add_argument("--output", help="Output file or directory")
    parser.add_argument("--operation", required=True, choices=OPERATIONS)
    parser.add_argument("--levels", type=int)
    parser.add_argument("--value", type=float)
    parser.add_argument("--alpha", type=float)
    parser.add_argument("--threshold", type=int)
    parser.add_argument("--kernel", help="Kernel text file")
    parser.add_argument(
        "--border",
        choices=("copy", "replicate"),
        default="replicate",
    )
    parser.add_argument(
        "--kernel-size",
        type=int,
        choices=(3, 5),
        default=3,
    )
    return parser


def related_path(main_path, suffix, extension=".png"):
    main_path = Path(main_path)
    return main_path.with_name(main_path.stem + suffix + extension)


def print_inspection(data):
    print(f"width={data['width']}")
    print(f"height={data['height']}")
    print(f"channels={data['channels']}")
    print(f"pixels={data['pixels']}")
    print(f"type={data['type']}")

    if data["channels"] == 1:
        print(f"minimum={data['minimum']}")
        print(f"maximum={data['maximum']}")
        print(f"mean={data['mean']:.6f}")
        return

    for channel_name in ("blue", "green", "red"):
        channel_data = data["by_channel"][channel_name]
        print(f"minimum_{channel_name}={channel_data['minimum']}")
        print(f"maximum_{channel_name}={channel_data['maximum']}")
        print(f"mean_{channel_name}={channel_data['mean']:.6f}")


def run(args):
    image = read_image(args.input)
    operation = args.operation

    if operation == "inspect":
        print_inspection(inspect_image(image))
        return None

    if operation == "copy":
        destination = resolve_output_path(args.output, "copy.png")
        write_image(destination, copy_image_pixel_by_pixel(image))

    elif operation in ("channel_b", "channel_g", "channel_r"):
        blue, green, red = split_channels(image)
        outputs = {
            "channel_b": blue,
            "channel_g": green,
            "channel_r": red,
        }
        destination = resolve_output_path(args.output, f"{operation}.png")
        write_image(destination, outputs[operation])

    elif operation == "grayscale_average":
        destination = resolve_output_path(args.output, "gray_average.png")
        write_image(destination, grayscale_average(image))

    elif operation == "grayscale_weighted":
        destination = resolve_output_path(args.output, "gray_weighted.png")
        write_image(destination, grayscale_weighted(image))

    elif operation == "quantize":
        if args.levels is None:
            raise ValueError("quantize requires --levels")
        gray = grayscale_weighted(image)
        destination = resolve_output_path(args.output, f"quant_{args.levels}.png")
        write_image(destination, quantize_image(gray, args.levels))

    elif operation == "brightness":
        if args.value is None:
            raise ValueError("brightness requires --value")
        gray = grayscale_weighted(image)
        destination = resolve_output_path(args.output, "brightness.png")
        write_image(destination, adjust_brightness(gray, args.value))

    elif operation == "contrast":
        if args.alpha is None:
            raise ValueError("contrast requires --alpha")
        gray = grayscale_weighted(image)
        destination = resolve_output_path(args.output, "contrast.png")
        write_image(destination, adjust_contrast(gray, args.alpha))

    elif operation == "negative":
        gray = grayscale_weighted(image)
        destination = resolve_output_path(args.output, "negative.png")
        write_image(destination, negative_image(gray))

    elif operation == "threshold":
        if args.threshold is None:
            raise ValueError("threshold requires --threshold")
        gray = grayscale_weighted(image)
        destination = resolve_output_path(args.output, "threshold.png")
        write_image(destination, threshold_image(gray, args.threshold))

    elif operation == "histogram":
        gray = grayscale_weighted(image)
        destination = resolve_output_path(args.output, "histogram.csv")
        write_histogram(destination, calculate_histogram(gray))

    elif operation == "convolution":
        if not args.kernel:
            raise ValueError("convolution requires --kernel")
        gray = grayscale_weighted(image)
        kernel = read_kernel(args.kernel)
        response = apply_convolution(gray, kernel, args.border)
        destination = resolve_output_path(args.output, "convolution.png")
        write_image(destination, matrix_to_uint8(response))

    elif operation == "mean_filter":
        gray = grayscale_weighted(image)
        kernel = MEAN_KERNEL_3X3 if args.kernel_size == 3 else MEAN_KERNEL_5X5
        response = apply_convolution(gray, kernel, args.border)
        destination = resolve_output_path(
            args.output,
            f"mean_{args.kernel_size}x{args.kernel_size}.png",
        )
        write_image(destination, matrix_to_uint8(response))

    elif operation == "weighted_mean":
        gray = grayscale_weighted(image)
        response = apply_convolution(gray, WEIGHTED_MEAN_KERNEL_3X3, args.border)
        destination = resolve_output_path(args.output, "weighted_mean.png")
        write_image(destination, matrix_to_uint8(response))

    elif operation == "laplacian":
        gray = grayscale_weighted(image)
        response = apply_convolution(gray, LAPLACIAN_KERNEL_3X3, args.border)
        destination = resolve_output_path(args.output, "laplacian.png")
        write_image(destination, absolute_matrix_to_uint8(response))
        write_image(
            related_path(destination, "_sharpened"),
            sharpen_with_laplacian(gray, response),
        )
        write_matrix_csv(
            related_path(destination, "_raw_response", ".csv"),
            response,
        )

    elif operation == "sobel":
        gray = grayscale_weighted(image)
        gradient_x = apply_convolution(gray, SOBEL_X_KERNEL, args.border)
        gradient_y = apply_convolution(gray, SOBEL_Y_KERNEL, args.border)
        approximate, euclidean = calculate_sobel_magnitudes(gradient_x, gradient_y)
        destination = resolve_output_path(args.output, "sobel.png")
        write_image(destination, matrix_to_uint8(euclidean))
        write_image(related_path(destination, "_gx"), absolute_matrix_to_uint8(gradient_x))
        write_image(related_path(destination, "_gy"), absolute_matrix_to_uint8(gradient_y))
        write_image(related_path(destination, "_approximate"), matrix_to_uint8(approximate))

    else:
        raise ValueError(f"Unknown operation: {operation}")

    print(destination)
    return destination


def main():
    try:
        args = build_parser().parse_args()
        run(args)
        return 0
    except Exception as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
