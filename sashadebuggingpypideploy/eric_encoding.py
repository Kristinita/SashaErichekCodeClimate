# -*- coding: utf-8 -*-
# @Author: SashaChernykh
# @Date: 2018-01-22 18:30:38
# @Last Modified time: 2018-08-25 19:19:59
"""Encoding checker.

Check, that files in Windows-1251 encoding.

Bugs:
    1. if no Cyrillic symbols in a file, chardet detect file encoding as ASCII;
    2. chardet can detect Windows-1251 as MacCyrillic.
"""
import chardet
import codecs
import erichek.eric_config
import os

from erichek.eric_config import ALL_TXT_IN_ERIC_ROOM_WITHOUT_SUBFOLDERS
from erichek.eric_config import pyfancy_critical
from erichek.eric_config import pyfancy_debug
from erichek.eric_config import pyfancy_notice

erichek.eric_config.LOG = os.path.splitext(os.path.basename(__file__))[0]


# Flags, see https://www.computerhope.com/jargon/f/flag.htm
# https://stackoverflow.com/a/48052480/5951529
ENCODING_UTF_8 = True


def eric_encoding_function():
    """Check encoding of the file.

    chardet check, that each file in Windows-1251.
    MacCyrillic — also true.
    In local testing UTF-8 convert to Cyrillic-1251.
    """
    # Get list all filenames in a directory
    # https://stackoverflow.com/a/1120736/5951529
    for filename in ALL_TXT_IN_ERIC_ROOM_WITHOUT_SUBFOLDERS:

        filename_without_path = os.path.basename(filename)

        # Not 100%, see https://stackoverflow.com/a/436299/5951529
        # Can doesn't work for Latin packages
        # Check decoding — http://bit.ly/2C3xSUD
        # https://stackoverflow.com/a/37531241/5951529
        rawdata = open(filename, "rb").read()
        chardet_data = chardet.detect(rawdata)
        # Python dictionary
        fileencoding = (chardet_data['encoding'])

        # [DEPRECATED] Migrating from Cyrillic 1251 to UTF-8
        # chardet_confidence = (chardet_data['confidence'])
        # # Needs MacCyrillic, because chardet can check Windows-1251
        # # as MacCyrillic
        # if fileencoding == 'windows-1251':
        #     LOG.debug(filename_without_path + " in windows-1251 encoding")
        # # Integer to string:
        # # https://stackoverflow.com/a/961638/5951529
        # elif fileencoding == 'MacCyrillic':
        #     LOG.info(pyfancy().green("Encoding of file " + filename_without_path +
        #                              " chardet detect as MacCyrillic with confidence " +
        #                              str(chardet_confidence)))
        # else:
        #     # Convert file from UTF-8 to Cyrillic 1251
        #     # https://stackoverflow.com/q/19932116/5951529
        #     with codecs.open(filename, "r", "utf-8") as file_for_conversion:
        #         read_file_for_conversion = file_for_conversion.read()
        #     with codecs.open(filename, "w", "windows-1251") as file_for_conversion:
        #         if read_file_for_conversion:
        #             file_for_conversion.write(read_file_for_conversion)
        #     red_background(filename_without_path +
        #                    " in " +
        #                    fileencoding +
        #                    ", not in Windows-1251 encoding! Please, save " +
        #                    filename_without_path + " in Windows-1251 encoding.")
        #     green_foreground("If encoding of file " + filename_without_path +
        #                      " is UTF-8 and you see message above in local wwtd testing, " +
        #                      filename_without_path +
        #                      " automatically will converted from UTF-8 to Windows-1251.")
        #     global ENCODING_WINDOWS_1251
        #     ENCODING_WINDOWS_1251 = False
        if fileencoding == 'utf-8':
            pyfancy_debug(filename_without_path + " in UTF-8 encoding")
        else:
            # Convert file from Cyrillic 1251 to UTF-8
            # https://stackoverflow.com/q/19932116/5951529
            with codecs.open(filename, "r", "windows-1251") as file_for_conversion:
                read_file_for_conversion = file_for_conversion.read()
            with codecs.open(filename, "w", "utf-8") as file_for_conversion:
                if read_file_for_conversion:
                    file_for_conversion.write(read_file_for_conversion)
            pyfancy_critical(filename_without_path +
                             " in " +
                             fileencoding +
                             ", not in UTF-8 encoding! Please, save " +
                             filename_without_path + " in UTF-8 encoding.")
            pyfancy_notice("If encoding of file " + filename_without_path +
                           " is Windows-1251 and you see message above in local wwtd testing, " +
                           filename_without_path +
                           " automatically will converted from Windows-1251 to UTF-8.")
            global ENCODING_UTF_8
            ENCODING_UTF_8 = False


def eric_encoding_summary():
    """Report, all files in UTF-8 or no."""
    eric_encoding_function()
    if ENCODING_UTF_8:
        pyfancy_notice("All files in UTF-8 encoding")

    if not ENCODING_UTF_8:
        pyfancy_critical(
            "One or more your files not in UTF-8 encoding. Please, convert it (them) to UTF-8.")