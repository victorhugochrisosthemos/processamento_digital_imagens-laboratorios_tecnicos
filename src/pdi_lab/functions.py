import csv
import math
import os
from pathlib import Path

import cv2
import numpy as np


DEFAULT_OUTPUT_FOLDER = "imagens_geradas"


def create_output_folder():
    folder = Path.cwd() / DEFAULT_OUTPUT_FOLDER
    folder.mkdir(parents=True, exist_ok=True)
    return folder


def read_image(image_path):
    path = Path(image_path)
    if not path.is_file():
        raise FileNotFoundError(f"Arquivo nao encontrado: {path}")

    image = cv2.imread(str(path), cv2.IMREAD_UNCHANGED)
    if image is None:
        raise ValueError(f"Nao foi possivel abrir a imagem: {path}")
    if image.dtype != np.uint8:
        raise ValueError("O programa trabalha com imagens de 8 bits (uint8).")
    return image


def channel_count(image):
    if image.ndim == 2:
        return 1
    if image.ndim == 3:
        return image.shape[2]
    raise ValueError("Formato de imagem nao suportado.")


def clamp_uint8(value):
    if value < 0:
        return 0
    if value > 255:
        return 255
    return int(round(value))


def resolve_output_path(requested_output, default_name):
    if requested_output is None:
        return create_output_folder() / default_name

    path = Path(requested_output)
    text = str(requested_output)
    looks_like_folder = path.is_dir() or text.endswith(os.sep) or path.suffix == ""

    if looks_like_folder:
        path.mkdir(parents=True, exist_ok=True)
        return path / default_name

    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def write_image(path, image):
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)

    if image.dtype != np.uint8:
        raise ValueError("A imagem deve estar em uint8 antes de ser gravada.")
    if not cv2.imwrite(str(destination), image):
        raise IOError(f"Nao foi possivel salvar a imagem: {destination}")
    return destination


def copy_image_pixel_by_pixel(image):
    copy = np.empty_like(image)
    height, width = image.shape[:2]
    channels = channel_count(image)

    for row in range(height):
        for column in range(width):
            if channels == 1:
                copy[row, column] = image[row, column]
            else:
                for channel in range(channels):
                    copy[row, column, channel] = image[row, column, channel]
    return copy


def inspect_image(image):
    height, width = image.shape[:2]
    channels = channel_count(image)
    pixel_count = width * height

    data = {
        "width": width,
        "height": height,
        "channels": channels,
        "pixels": pixel_count,
        "type": str(image.dtype),
    }

    if channels == 1:
        minimum = 255
        maximum = 0
        total = 0
        for row in range(height):
            for column in range(width):
                value = int(image[row, column])
                total += value
                if value < minimum:
                    minimum = value
                if value > maximum:
                    maximum = value
        data["minimum"] = minimum
        data["maximum"] = maximum
        data["mean"] = total / pixel_count
        return data

    if channels != 3:
        raise ValueError("A inspecao colorida considera imagens BGR de tres canais.")

    minimums = [255, 255, 255]
    maximums = [0, 0, 0]
    totals = [0, 0, 0]

    for row in range(height):
        for column in range(width):
            for channel in range(3):
                value = int(image[row, column, channel])
                totals[channel] += value
                if value < minimums[channel]:
                    minimums[channel] = value
                if value > maximums[channel]:
                    maximums[channel] = value

    data["by_channel"] = {}
    for index, name in enumerate(("blue", "green", "red")):
        data["by_channel"][name] = {
            "minimum": minimums[index],
            "maximum": maximums[index],
            "mean": totals[index] / pixel_count,
        }
    return data


def split_channels(image):
    if channel_count(image) != 3:
        raise ValueError("A separacao de canais exige uma imagem colorida de tres canais.")

    height, width = image.shape[:2]
    blue_channel = np.zeros_like(image)
    green_channel = np.zeros_like(image)
    red_channel = np.zeros_like(image)

    for row in range(height):
        for column in range(width):
            blue_channel[row, column, 0] = image[row, column, 0]
            green_channel[row, column, 1] = image[row, column, 1]
            red_channel[row, column, 2] = image[row, column, 2]

    return blue_channel, green_channel, red_channel


def grayscale_average(image):
    channels = channel_count(image)
    if channels == 1:
        return copy_image_pixel_by_pixel(image)
    if channels != 3:
        raise ValueError("A conversao para cinza exige uma imagem de tres canais.")

    height, width = image.shape[:2]
    result = np.zeros((height, width), dtype=np.uint8)

    for row in range(height):
        for column in range(width):
            blue = int(image[row, column, 0])
            green = int(image[row, column, 1])
            red = int(image[row, column, 2])
            average = (red + green + blue) / 3.0
            result[row, column] = clamp_uint8(average)
    return result


def grayscale_weighted(image):
    channels = channel_count(image)
    if channels == 1:
        return copy_image_pixel_by_pixel(image)
    if channels != 3:
        raise ValueError("A conversao para cinza exige uma imagem de tres canais.")

    height, width = image.shape[:2]
    result = np.zeros((height, width), dtype=np.uint8)

    for row in range(height):
        for column in range(width):
            blue = int(image[row, column, 0])
            green = int(image[row, column, 1])
            red = int(image[row, column, 2])
            intensity = 0.299 * red + 0.587 * green + 0.114 * blue
            result[row, column] = clamp_uint8(intensity)
    return result


def quantize_image(gray_image, levels):
    if channel_count(gray_image) != 1:
        raise ValueError("A quantizacao exige uma imagem em tons de cinza.")
    if not isinstance(levels, int) or not 2 <= levels <= 256:
        raise ValueError("A quantidade de niveis deve ser um inteiro entre 2 e 256.")

    height, width = gray_image.shape
    result = np.zeros_like(gray_image)
    step = 255.0 / (levels - 1)

    for row in range(height):
        for column in range(width):
            intensity = int(gray_image[row, column])
            nearest_level = int(round(intensity / step))
            result[row, column] = clamp_uint8(
                nearest_level * step
            )
    return result


def adjust_brightness(gray_image, brightness_value):
    if channel_count(gray_image) != 1:
        raise ValueError("O ajuste de brilho exige uma imagem em tons de cinza.")

    height, width = gray_image.shape
    result = np.zeros_like(gray_image)
    for row in range(height):
        for column in range(width):
            new_value = int(gray_image[row, column]) + brightness_value
            result[row, column] = clamp_uint8(new_value)
    return result


def adjust_contrast(gray_image, alpha):
    if channel_count(gray_image) != 1:
        raise ValueError("O ajuste de contraste exige uma imagem em tons de cinza.")
    if alpha < 0:
        raise ValueError("O fator de contraste nao pode ser negativo.")

    height, width = gray_image.shape
    result = np.zeros_like(gray_image)
    for row in range(height):
        for column in range(width):
            intensity = int(gray_image[row, column])
            new_value = alpha * (intensity - 128) + 128
            result[row, column] = clamp_uint8(new_value)
    return result


def negative_image(gray_image):
    if channel_count(gray_image) != 1:
        raise ValueError("O negativo exige uma imagem em tons de cinza.")

    height, width = gray_image.shape
    result = np.zeros_like(gray_image)
    for row in range(height):
        for column in range(width):
            result[row, column] = 255 - int(gray_image[row, column])
    return result


def threshold_image(gray_image, threshold):
    if channel_count(gray_image) != 1:
        raise ValueError("A limiarizacao exige uma imagem em tons de cinza.")
    if not 0 <= threshold <= 255:
        raise ValueError("O limiar deve estar entre 0 e 255.")

    height, width = gray_image.shape
    result = np.zeros_like(gray_image)
    for row in range(height):
        for column in range(width):
            intensity = int(gray_image[row, column])
            result[row, column] = 0 if intensity < threshold else 255
    return result


def calculate_histogram(gray_image):
    if channel_count(gray_image) != 1:
        raise ValueError("O histograma exige uma imagem em tons de cinza.")

    counts = [0 for _ in range(256)]
    height, width = gray_image.shape
    for row in range(height):
        for column in range(width):
            intensity = int(gray_image[row, column])
            counts[intensity] += 1
    return counts


def write_histogram(path, counts):
    if len(counts) != 256:
        raise ValueError("O histograma precisa possuir 256 posicoes.")

    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        # Cabecalho oficial mantido por compatibilidade com o contrato tecnico.
        writer.writerow(["intensity", "count"])
        for intensity, amount in enumerate(counts):
            writer.writerow([intensity, amount])
    return destination


def validate_kernel(kernel):
    matrix = np.asarray(kernel, dtype=np.float64)
    if matrix.ndim != 2 or matrix.size == 0:
        raise ValueError("Nucleo vazio ou invalido.")
    rows, columns = matrix.shape
    if rows != columns:
        raise ValueError("O nucleo deve ser quadrado.")
    if rows % 2 == 0:
        raise ValueError("A dimensao do nucleo deve ser impar.")
    return matrix


def read_kernel(kernel_path):
    path = Path(kernel_path)
    if not path.is_file():
        raise FileNotFoundError(f"Nucleo nao encontrado: {path}")

    rows = [
        row.strip()
        for row in path.read_text(encoding="utf-8").splitlines()
        if row.strip()
    ]
    if not rows:
        raise ValueError("O arquivo do nucleo esta vazio.")

    header = rows[0].split()
    if len(header) != 2:
        raise ValueError("A primeira linha deve informar linhas e colunas.")

    try:
        row_count = int(header[0])
        column_count = int(header[1])
    except ValueError as error:
        raise ValueError("As dimensoes do nucleo sao invalidas.") from error

    values = []
    for row in rows[1:]:
        for text in row.split():
            try:
                values.append(float(text))
            except ValueError as error:
                raise ValueError("O arquivo possui um valor de nucleo invalido.") from error

    if len(values) != row_count * column_count:
        raise ValueError("A quantidade de valores nao corresponde as dimensoes do nucleo.")

    matrix = np.array(values, dtype=np.float64).reshape(
        (row_count, column_count)
    )
    return validate_kernel(matrix)


def _replicated_coordinate(coordinate, limit):
    if coordinate < 0:
        return 0
    if coordinate >= limit:
        return limit - 1
    return coordinate


def apply_convolution(gray_image, kernel, border_mode="replicate"):
    if channel_count(gray_image) != 1:
        raise ValueError("A convolucao exige uma imagem em tons de cinza.")
    if border_mode not in ("copy", "replicate"):
        raise ValueError("Border mode must be 'copy' or 'replicate'.")

    kernel = validate_kernel(kernel)
    height, width = gray_image.shape
    kernel_size = kernel.shape[0]
    offset = kernel_size // 2
    result = np.zeros((height, width), dtype=np.float64)

    for row in range(height):
        for column in range(width):
            neighborhood_outside = (
                row - offset < 0
                or row + offset >= height
                or column - offset < 0
                or column + offset >= width
            )

            if border_mode == "copy" and neighborhood_outside:
                result[row, column] = float(gray_image[row, column])
                continue

            total = 0.0
            for kernel_row in range(kernel_size):
                for kernel_column in range(kernel_size):
                    image_row = row + kernel_row - offset
                    image_column = column + kernel_column - offset

                    if border_mode == "replicate":
                        image_row = _replicated_coordinate(image_row, height)
                        image_column = _replicated_coordinate(image_column, width)

                    total += (
                        float(gray_image[image_row, image_column])
                        * float(kernel[kernel_row, kernel_column])
                    )
            result[row, column] = total
    return result


def matrix_to_uint8(matrix):
    height, width = matrix.shape
    result = np.zeros((height, width), dtype=np.uint8)
    for row in range(height):
        for column in range(width):
            result[row, column] = clamp_uint8(
                float(matrix[row, column])
            )
    return result


def absolute_matrix_to_uint8(matrix):
    height, width = matrix.shape
    result = np.zeros((height, width), dtype=np.uint8)
    for row in range(height):
        for column in range(width):
            result[row, column] = clamp_uint8(
                abs(float(matrix[row, column]))
            )
    return result


def sharpen_with_laplacian(gray_image, laplacian_response):
    if laplacian_response.shape != gray_image.shape:
        raise ValueError("A imagem e a resposta do Laplaciano devem ter o mesmo tamanho.")

    height, width = gray_image.shape
    result = np.zeros_like(gray_image)
    for row in range(height):
        for column in range(width):
            value = float(gray_image[row, column]) + float(
                laplacian_response[row, column]
            )
            result[row, column] = clamp_uint8(value)
    return result


def calculate_sobel_magnitudes(gradient_x, gradient_y):
    if gradient_x.shape != gradient_y.shape:
        raise ValueError("Os gradientes X e Y precisam ter as mesmas dimensoes.")

    height, width = gradient_x.shape
    approximate_magnitude = np.zeros((height, width), dtype=np.float64)
    euclidean_magnitude = np.zeros((height, width), dtype=np.float64)

    for row in range(height):
        for column in range(width):
            value_x = float(gradient_x[row, column])
            value_y = float(gradient_y[row, column])
            approximate_magnitude[row, column] = abs(value_x) + abs(value_y)
            euclidean_magnitude[row, column] = math.sqrt(
                value_x * value_x + value_y * value_y
            )
    return approximate_magnitude, euclidean_magnitude


def write_matrix_csv(path, matrix):
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        for row in range(matrix.shape[0]):
            writer.writerow(
                [float(matrix[row, column]) for column in range(matrix.shape[1])]
            )
    return destination


MEAN_KERNEL_3X3 = np.array(
    [[1 / 9, 1 / 9, 1 / 9], [1 / 9, 1 / 9, 1 / 9], [1 / 9, 1 / 9, 1 / 9]],
    dtype=np.float64,
)

MEAN_KERNEL_5X5 = np.full((5, 5), 1 / 25, dtype=np.float64)

WEIGHTED_MEAN_KERNEL_3X3 = np.array(
    [[1 / 16, 2 / 16, 1 / 16], [2 / 16, 4 / 16, 2 / 16], [1 / 16, 2 / 16, 1 / 16]],
    dtype=np.float64,
)

LAPLACIAN_KERNEL_3X3 = np.array(
    [[0, -1, 0], [-1, 4, -1], [0, -1, 0]], dtype=np.float64
)

SOBEL_X_KERNEL = np.array(
    [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]], dtype=np.float64
)

SOBEL_Y_KERNEL = np.array(
    [[-1, -2, -1], [0, 0, 0], [1, 2, 1]], dtype=np.float64
)
