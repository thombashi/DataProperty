# encoding: utf-8

'''
@author: Tsuyoshi Hombashi
'''


class Align:

    class __AlignData:

        @property
        def align_code(self):
            return self.__align_code

        @property
        def align_string(self):
            return self.__align_string

        def __init__(self, code, string):
            self.__align_code = code
            self.__align_string = string

    AUTO = __AlignData(1 << 0, "auto")
    LEFT = __AlignData(1 << 1, "left")
    RIGHT = __AlignData(1 << 2, "right")
    CENTER = __AlignData(1 << 3, "center")
