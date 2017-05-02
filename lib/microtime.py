# -*- encoding: utf8 -*-
'''******************************************************************************
    @licence    LGPL
    @author     Thierry Graff
    @history    2014-01-13 23:57:58+01:00 : Thierry Graff, Copied from http://www.php2python.com/wiki/function.microtime/
********************************************************************************'''

import time
import math

def microtime(get_as_float = False) :
    if get_as_float:
        return time.time()
    else:
        return '%f %d' % math.modf(time.time())

