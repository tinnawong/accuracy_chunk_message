# from guppy import hpy
# import psutil,time,sys
# import psutil,os
# import platform,codecs
# from prove import generateMatrix
# print(platform.node())

# print(platform.machine())
# print(platform.node())
# print(platform.architecture())
from unicategories import unicodedata
def isMn(aChar):
    cc = u'{}'.format(aChar)
    print(unicodedata.category(cc))



if __name__ == "__main__":
    isMn('')