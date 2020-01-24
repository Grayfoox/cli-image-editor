import unittest.mock as umock
from argparse import ArgumentTypeError

import numpy as np
import pytest

from functions import do_embossing, do_edge_detection, do_blur_5x5, do_blur_3x3, do_sharpen, do_bw, do_darken, \
    do_inverse, do_lighten, do_mirror, do_rotate, percentage, read_image, save_image

test_array = np.array([[1, 1, 1], [1, 1, 1], [1, 1, 1]])

test_image = read_image("test_images/test_img.png")

args_mock = umock.MagicMock()
# zesvetleni a ztmaveni, TODO udelat aby mock vzdy vracel 50, pro pripad ze bude vic unit testu nez hodnot
args_mock.darken = [50, 50, 50, 50, 80, 70, 80, 10, 80]  # TODO mockovat veci v danem testu
args_mock.lighten = [50, 50, 50, 50, 100, 70, 40, 50, 100]


def test_read_image():
    assert read_image("test_images/test_img.png").ndim > 0  # jakykoliv non fail vysledek je ok


def test_image_fail():
    with pytest.raises(FileNotFoundError):
        read_image("nonexistent_file_please_dont_create_file_named_like_this.pls")


def test_do_embossing():
    out = do_embossing(test_array)


def test_do_edge_detection():
    out = do_edge_detection(test_array)


def test_do_blur_5x5():
    out = do_blur_5x5(test_array)


def test_do_blur_3x3():
    out = do_blur_3x3(test_array)


def test_do_sharpen():
    out = do_sharpen(test_array)


def test_do_bw():
    out = do_bw(test_array)


def test_do_inverse():
    out = do_inverse(test_array)
    assert (out == 254).all()


def test_do_darken():
    out = do_darken(test_array, args_mock)
    assert np.all(out == 0.5)


def test_do_lighten():
    out = do_lighten(test_array, args_mock)
    assert np.all(out == 1.5)


def test_do_mirror():
    out = do_mirror(test_array)
    assert ((test_array == out).all())  # po zrcadleni musi byt identicke


def test_do_rotate():
    out = do_rotate(test_array)
    assert ((test_array == out).all())  # po rotaci musi byt identicke


def test_percentage_invalid():
    a = None
    with pytest.raises(ArgumentTypeError):
        percentage(-1)
    assert (a is None)


def test_percentage_high_value():
    a = None
    a = percentage(10000000)
    assert a == 10000000


def test_percentage_zero():
    a = None
    a = percentage(0)
    assert a == 0


def test_rotation_identity():
    # pokud otocime jeden obrazek 4x musi byt stejny jako puvodni
    out = do_rotate(test_image)
    out = do_rotate(out)
    out = do_rotate(out)
    final = do_rotate(out)
    assert (final == test_image).all()


def test_mirror_identity():
    out = do_mirror(test_image)
    final = do_mirror(out)
    assert (final == test_image).all()


def test_multiple_bw():
    # vicero pouzitych bw musi vracet stejnou hodnotu
    out = do_bw(test_image)
    second_out = do_bw(out)
    third_out = do_bw(second_out)

    assert np.logical_and((out == second_out).all(), (second_out == third_out).all())


def test_compare_rotate():
    out = do_rotate(test_image)
    test_input = read_image("test_images/rotate.png")
    assert (out == test_input).all()


def test_compare_mirror():
    out = do_mirror(test_image)
    test_input = read_image("test_images/mirror.png")
    assert (out == test_input).all()


def test_compare_inverse():
    out = do_inverse(test_image)
    test_input = read_image("test_images/inverse.png")
    assert (out == test_input).all()


# TODO before saving there are some slight data diference, that causes fail even if images are same
def test_compare_bw():
    out = do_bw(test_image)
    save_image(out, "test_images/bwOut.png")
    output = read_image("test_images/bwOut.png")
    test_input = read_image("test_images/bw.png")
    assert (output == test_input).all()


# TODO before saving there are some slight data diference, that causes fail even if images are same
def test_compare_lighten():
    out = do_lighten(test_image, args_mock)
    save_image(out, "test_images/lightenOut.png")
    output = read_image("test_images/lightenOut.png")
    test_input = read_image("test_images/lighten.png")
    assert (output == test_input).all()


# TODO before saving there are some slight data diference, that causes fail even if images are same
def test_compare_darken():
    out = do_darken(test_image, args_mock)
    save_image(out, "test_images/darkenOut.png")
    output = read_image("test_images/darkenOut.png")
    test_input = read_image("test_images/darken.png")
    assert (output == test_input).all()


def test_argument_chaining_one_convolution():
    # testuje funkcnost retezeni, vzajmne kompability a toho, ze si testy navzajem neznici file
    # kvuli casove narocnosti testujeme pouze jednu konvolucni fci (pouzivaji stejny kod, pouze kernel se meni)
    out = do_mirror(test_image)
    out = do_rotate(out)
    out = do_lighten(out, args_mock)
    out = do_inverse(out)
    out = do_darken(out, args_mock)
    out = do_bw(out)
    out = do_sharpen(out)
    out = do_mirror(test_image)
    out = do_rotate(out)
    out = do_lighten(out, args_mock)
    out = do_inverse(out)
    out = do_darken(out, args_mock)


"""
casove narocne testy

def test_compare_sharpen():
    out = do_sharpen(test_image)
    test_input = read_image("test_images/sharpen.png")
    assert (out == test_input).all()


def test_compare_blur_3x3():
    out = do_blur_3x3(test_image)
    test_input = read_image("test_images/blur3.png")
    assert (out == test_input).all()


def test_compare_blur_5x5():
    out = do_blur_5x5(test_image)
    test_input = read_image("test_images/blur5.png")
    assert (out == test_input).all()


def test_compare_edge_detection():
    out = do_edge_detection(test_image)
    test_input = read_image("test_images/edges.png")
    assert (out == test_input).all()


def test_compare_embossing():
    out = do_embossing(test_image)
    test_input = read_image("test_images/embossing.png")
    assert (out == test_input).all()
"""
