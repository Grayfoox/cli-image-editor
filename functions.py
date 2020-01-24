from argparse import ArgumentTypeError

import numpy as np
from PIL import Image

from convolution_functions import apply_filter, filters

debug_mode = False

"""
Seznam pouzitelnych funkci pro tento program na upravu obrazku.
Pro pridani fuknce ji napiste zde, a pridejte do action_dict (seznam pouzitelnych fci) 
a pote ji udelejte CLI callable v Main pres add_argument. 
"""


def read_image(file_name: str) -> np.array:
    """
    pomocna funkce na nacteni obrazku

    :param file_name: cesta k souboru
    :return: numpy array, pripravene na upravy pomoci nasich funkcni
    """
    return np.asarray(Image.open(file_name), dtype=np.int32)


def save_image(array, file_path):
    """
    pomocna funkce na ulozeni obrazku, sama prevede pole z int32 na unit8 a ulozi

    :param array:
    :param file_path:
    :return:
    """
    out = array.astype("uint8")
    Image.fromarray(out).save(file_path)


def percentage(val):
    """
    Vlastni datovy typ pro argparse, pouze kontroluje zda uzivatel zadal cislo vetsi nez nula
    :param val: vstup z argparse
    :return: int v rozmezi 0 - 100 (bez upravy)
    """
    try:
        n = int(val)
        if 0 <= n:
            return n
        else:
            msg = "Cislo nemuze byt mensi nez nula"
            raise ArgumentTypeError(msg)
    except ValueError:
        msg = 'Zadaný vstup se nepodařilo převést na číslo!'
        raise ArgumentTypeError(msg)


"""
image edit functions
"""


def do_rotate(np_image, args=None):
    out = np.rot90(np_image)
    if debug_mode:
        print("a do_rotate")
    return out


def do_mirror(np_image, args=None):
    assert np_image.ndim > 1
    out = np_image[::, ::-1]
    if debug_mode:
        print("a do_mirror")
    return out


def do_inverse(np_image, args=None):
    """
    funkce inverze barev (z cerne se stane bila apod).
    :param np_image: numpy obrazek co chceme upravit
    :param args: Neni zde potreba, pouze pro kompabilitu
    :return: upraaveny obrazek v Numpy array
    """
    if len(np_image.shape) > 2:
        out = np.abs(np_image[::, ::, 0:min(np_image.shape[2], 3)] - 255)
    else:
        out = np.abs(np_image - 255)

    if debug_mode:
        print("a do_inverse")
    return out


def do_bw(np_image, args=None):
    """
    funkce do prevodu sedi, pouzivame ITU-R 601-2 luma vzorec.
    :param np_image: numpy obrazek co chceme upravit
    :param args: Neni zde potreba, pouze pro kompabilitu
    :return: upraaveny obrazek v Numpy array
    """
    if np_image.ndim is not 3:  # obrazek je uz v grayscale, takze neni treba ho opakovat
        print("Jiz ve stupni sedi, redudantni --bw")
        return np_image

    result_red = (np_image[::, ::, 0] * 0.299)
    result_green = (np_image[::, ::, 1] * 0.587)
    result_blue = (np_image[::, ::, 2] * 0.114)

    final = (result_red + result_green + result_blue)
    if debug_mode:
        print("a do_bw")
    return final


def do_lighten(np_image, args):
    """
    funkce ktera zesvetla vsechny pixely o dane procento
    :param np_image: numpy obrazek co chceme upravit
    :param args: Bere z argparseru lighten value
    :return: upraaveny obrazek v Numpy array
    """
    if args is None:
        raise ValueError
    value = args.lighten.pop(0)
    # vime ze 100% = 1, 50% = 0.5, proto prenasobime a pricteme 1 abychom obrazek omylem neztmavili
    percentil_value = (value * 0.01) + 1
    if len(np_image.shape) > 2:
        out = np.minimum(np_image[::, ::, 0:min(np_image.shape[2], 3)] * percentil_value, 255)
    else:
        out = np.minimum(np_image * percentil_value, 255)

    if debug_mode:
        print("a do_lighten")
    return out


def do_darken(np_image, args):
    """
    funkce ktera ztmavi vsechny pixely o dane procento
    :param np_image: numpy obrazek co chceme upravit
    :param args: Bere z argparseru lighten value
    :return: upraaveny obrazek v Numpy array
    """
    if args is None:
        raise ValueError
    value = args.darken.pop(0)
    if len(np_image.shape) > 2:
        out = np_image[::, ::, 0:min(np_image.shape[2], 3)] * (value * 0.01)
    else:
        out = (np_image * (value * 0.01))

    if debug_mode:
        print("a do_darken")
    return out


def do_sharpen(np_image, args=None):
    """
    funkce zostreni, zavola konvolucni metodu s danym filtrem a vrati vysledek
    :param np_image: numpy obrazek co chceme upravit
    :param args: Neni zde potreba, pouze pro kompabilitu
    :return: upraaveny obrazek v Numpy array
    """
    out = apply_filter(np_image, filters["Sharpening"])
    if debug_mode:
        print("a do_sharpen")
    return out


def do_blur_3x3(np_image, args=None):
    """
    funkce rozmazani, zavola konvolucni metodu s danym filtrem a vrati vysledek
    :param np_image: numpy obrazek co chceme upravit
    :param args: Neni zde potreba, pouze pro kompabilitu
    :return: upraaveny obrazek v Numpy array
    """
    out = apply_filter(np_image, filters['Gaussian blur 3x3 (approx)'])
    if debug_mode:
        print("a do_blur_3x3")
    return out


def do_blur_5x5(np_image, args=None):
    """
    funkce rozmazani s vetsim zaberem okolim, zavola konvolucni metodu s danym filtrem a vrati vysledek
    :param np_image: numpy obrazek co chceme upravit
    :param args: Neni zde potreba, pouze pro kompabilitu
    :return: upraaveny obrazek v Numpy array
    """
    out = apply_filter(np_image, filters['Gaussian blur 5x5 (approx)'])
    if debug_mode:
        print("a do_blur_5x5")
    return out


def do_edge_detection(np_image, args=None):
    """
    funkce detekce hran, zavola konvolucni metodu s danym filtrem a vrati vysledek
    :param np_image: numpy obrazek co chceme upravit
    :param args: Neni zde potreba, pouze pro kompabilitu
    :return: upraaveny obrazek v Numpy array
    """
    out = apply_filter(np_image, filters['Edge detection'])
    if debug_mode:
        print("a do_edge_detection")
    return out


def do_embossing(np_image, args=None):
    """
    funkce vyrazeni, zavola konvolucni metodu s danym filtrem a vrati vysledek
    :param np_image: numpy obrazek co chceme upravit
    :param args: Neni zde potreba, pouze pro kompabilitu
    :return: upraaveny obrazek v Numpy array
    """
    out = apply_filter(np_image, filters['Embossing'])
    if debug_mode:
        print("a do_embossing")
    return out


"""
Slovník (Dictionary) všech možných úprav obrázku, slouží pro parsování argparse a tohoto programu
pro přidání nové fce je třeba jí napsat do funcions.py a poté jí přidat sem
"""
action_dict = {
    "--rotate": do_rotate,
    "--mirror": do_mirror,
    "--inverse": do_inverse,
    "--bw": do_bw,
    "--lighten": do_lighten,
    "--darken": do_darken,
    "--sharpen": do_sharpen,
    "--blur_3x3": do_blur_3x3,
    "--blur_5x5": do_blur_5x5,
    "--edge_detection": do_edge_detection,
    "--embossing": do_embossing
}
