# -*- coding: utf-8 -*-
# @Author: SashaChernykh
# @Date: 2018-08-12 07:52:00
# @Last Modified time: 2018-08-30 15:49:15
"""eyo.

Check proper use «ё» letter.
"""
import shutil

import delegator

from erichek.eric_config import files_loop
from erichek.eric_config import pyfancy_debug
from erichek.eric_config import pyfancy_error
from erichek.eric_config import pyfancy_info

# [DEPRECATED]
# I decode mojibake to UTF-8 in each time
# Needs hacks for UTF-8 Windows locale
# https://github.com/kennethreitz/delegator.py/issues/59
# Set Windows locale to UTF-8:
# https://stackoverflow.com/a/34345136/5951529
# https://github.com/kennethreitz/delegator.py/blob/7420834967ead70bf65bc1270c88f7a3a352df2b/delegator.py#L78-L88
# I get mojibakes, if only setx PYTHONIOENCODING utf-8, example:
# [OK] Р‘РѕРєСЃС‘СЂС‹-С‚СЏР¶РµР»РѕРІРµСЃС‹.txt


def eric_eyo():
    """Check files, that «ё» contains.

    Check files, use «eyo» checker:
    https://www.npmjs.com/package/eyo
    """
    for filename_pylint in files_loop():
        eyo_command = delegator.run(
            'eyo --lint --only-safe ' + filename_pylint)
        # Decode mojibake to UTF-8
        pyfancy_info(eyo_command.out.encode('cp1251').decode('utf-8'))
        if eyo_command.return_code == 22:
            # eyo not support in-place replacing:
            # https://github.com/hcodes/eyo/issues/15
            pyfancy_error("«ё» replacing needs in " + filename_pylint)
            delegator.run('eyo ' + filename_pylint + ' > temp')
            # shutil.move move and force overwrite a file:
            # https://stackoverflow.com/a/8858026/5951529
            shutil.move('temp', filename_pylint)
            yield False
        else:
            pyfancy_debug(
                "eyo did not find any gross errors related to «ё» in the file " +
                filename_pylint)


# def eric_eyo_summary():
#     """Report, contains «ё» in all files or no.

#     Chromium style. Do not use else after return.
#     https://stackoverflow.com/a/28250521/5951529

#     Returns:
#         bool -- is «ё» or no in all files or no

#     """
#     if False in [item for item in eric_eyo()]:
#         pyfancy_error(
#             "One or more your files doesn't contain «ё». Please, make your changes locally.")
#         return False
#     pyfancy_notice("All files contains «ё»")
#     return True
