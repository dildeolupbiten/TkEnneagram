# -*- coding: utf-8 -*-

import sys
try:
    import virtualenv
    sys.stdout.write("True")
except ModuleNotFoundError:
    sys.stdout.write("False")
