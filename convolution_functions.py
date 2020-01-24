import numpy as np

"""
Konvolucni metody jsou ponekud narocnejsi na vykon (protoze nepouzivame plne optimalizovane knihovny na konvoluci)

Pro pridani noveho kernelu ho napiste mezi ostatni kernely a pridejte do filters. Pote napiste wrapper pro nej ve 
functions.py a nakonec napiste CLI prepinac v main.py
"""

#TODO use better functions
def channel_convolution_result(image: np.array, kernel: np.array) -> np.array:
    """
    vezme 2 rozmerne pole a kernel a aplikuje kernel na pole a vrati ho
    :param image: image where we apply convolution
    :param kernel: kernel to apply
    :return: 2 dimensional np.array of sums
    """
    result = np.zeros(image.shape)
    result = result.astype("int32")  # for overflowing and negative values

    kernel_size = kernel.shape[0]
    # Pad with zeros from all sides,
    towork = np.pad(image, [(kernel_size // 2, kernel_size // 2), (kernel_size // 2, kernel_size // 2)],
                    mode='constant', constant_values=0)

    # Using //2 because padding, kernel shape must be square, so it doesnt matter which side we use
    for i in range((towork.shape[0] - ((kernel_size // 2) * 2))):
        for j in range((towork.shape[1] - ((kernel_size // 2) * 2))):
            #  we get the sum of pixels around
            result[i, j] = \
                np.sum((kernel * towork[(i + 0):(i + kernel_size), (j + 0):(j + kernel_size)]))



    # cut values to fit between 0-255 (no clipping, overflowing etc, all above 255 is set to 255, same with 0)
    np.clip(result, 0, 255, result)
    result = result.astype("uint8")
    return result


def apply_filter(image: np.array, kernel: np.array) -> np.array:
    """
    obalová funkce na channel_convolution_result, zkontroluje velikost img pole a podle počtu barevných kanálů zavolá
    channel_convolution_result na každý z nich
    :param image: obrázek na zpracování (v numpy.array formátu)
    :param kernel: matice podle které se obrázek bude editovat
    :return:
    """
    # A given image has to have either 2 (grayscale) or 3 (RGB) dimensions
    assert image.ndim in [2, 3]
    # A given filter has to be 2 dimensional and square
    assert kernel.ndim == 2
    assert kernel.shape[0] == kernel.shape[1]

    # If its 2 dimensional, we can return result, no postprocessing needed
    if image.ndim is 2:
        return channel_convolution_result(image, kernel)
    else:
        result_red = channel_convolution_result(image[::, ::, 0], kernel)
        result_green = channel_convolution_result(image[::, ::, 1], kernel)
        result_blue = channel_convolution_result(image[::, ::, 2], kernel)

        # stack all channels in 3. dimension
        result = np.dstack((result_red, result_green, result_blue))

    return result


"""
Seznam pouzitelnych kernelu
"""

sharpening_kernel = np.array([
    [0, -1, 0],
    [-1, 5, -1],
    [0, -1, 0],
])

approx_gaussian_blur_3_kernel = (1 / 16) * np.array([
    [1, 2, 1],
    [2, 4, 2],
    [1, 2, 1],
])

approx_gaussian_blur_5_kernel = (1 / 256) * np.array([
    [1, 4, 6, 4, 1],
    [4, 16, 24, 16, 4],
    [6, 24, 36, 24, 6],
    [4, 16, 24, 16, 4],
    [1, 4, 6, 4, 1],
])

edge_detection_kernel = np.array([
    [-1, -1, -1],
    [-1, 8, -1],
    [-1, -1, -1],
])

embossing_kernel = np.array([
    [-2, -1, 0],
    [-1, 1, 1],
    [0, 1, 2]
])

# Slovník použitelných kernelů, při přidání nového kernelu je třeba ho přidat i sem
filters = {
    'Sharpening': sharpening_kernel,
    'Gaussian blur 3x3 (approx)': approx_gaussian_blur_3_kernel,
    'Gaussian blur 5x5 (approx)': approx_gaussian_blur_5_kernel,
    'Edge detection': edge_detection_kernel,
    'Embossing': embossing_kernel,
}
