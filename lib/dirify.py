# -*- encoding: utf8 -*-
'''******************************************************************************
    @licence    LGPL
    @author     Thierry Graff
    @history    2009.12.04 : Creation
********************************************************************************'''


# ****************************
def dirify(s, replace='-'):
    '''
    Transforms an UTF8 string to a string usable in a file name.
    Port of an ddaptation from a script found at http://www.phpit.net/code/dirify/,	2005.12.22 02:24
    @param str The string to dirify.
    @param replace Replacement character (or string) for space characters
    @return The transformed string
    '''
    import sys
    from os.path import abspath, dirname
    path = dirname(dirname(abspath(__file__)))
    sys.path.append(path)
    import re
    from strip_tags import strip_tags
    from remove_accents import remove_accents
    try:
        s = remove_accents(s)
    except UnicodeDecodeError:
        s = remove_accents(s.encode('utf-8'))
    s = s.lower()                       ## lower-case.
    s = strip_tags(s)                   ## remove HTML tags.
    s = re.sub('&#038;[^;\s]+;','', s)  ## remove HTML entities.
    s = re.sub('[^\w\s]',replace, s)    ## remove non-word/space chars.
    s = re.sub('\s+', replace, s)       ## change space chars to replace
    # remove multiple replace
    tmp = replace + replace
    while s.find(tmp) != -1:
        s = s.replace(tmp, replace)
    # if last character is replace, remove it
    if s[-1:] == replace :
        s = s[0:-1]
    # if first character is replace, remove it
    if s[0:1] == replace:
        s = s[1:]
    #
    return s		
# end dirify


# ************************************************************************************
#                                       tests
# ************************************************************************************
if __name__ == '__main__':
    def test_dirify():
        print(dirify("un éléphant, , '76''' (ça trompe) énormément..."))
    #test_dirify()
    

