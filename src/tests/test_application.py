import unittest
from gui import Application
from PIL import Image as pil_image
import os
import sys


class test_gui(unittest.TestCase):
    @property
    def mario_img(self):
        path = os.path.join(sys.path[0], "tests/test_img.png")
        return pil_image.open(path)

    @property
    def mario_link_img(self):
        link = ("https://i.pinimg.com/originals/c5/0e/"
                "0a/c50e0a205f5d839a09c2239e45dee376.png")
        return Application.convert_link_2_img(link)

    # tests the image conversion for proper display in tkinter gui
    def test_img_coversion(self):
        self.assertEqual(self.mario_img, self.mario_link_img)

    # tests color conversion for electric type and a unknown type
    # electric should return yellow
    # an unknown type should return grey
    def test_color_conversion(self):
        self.assertEqual(Application.type_2_color("electric"), "yellow")
        self.assertEqual(Application.type_2_color("giberish"), "grey")
