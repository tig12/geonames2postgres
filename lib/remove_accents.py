# -*- encoding: utf8 -*-
'''******************************************************************************
    @licence    LGPL
    @author     Thierry Graff
    @history    2009.12.04 : Creation
********************************************************************************'''


# ***************************************************
def remove_accents(s):
    '''
    Removes accents from a utf-8 string
    '''
#    import unicodedata
#    nkfd_form = unicodedata.normalize('NFKD', unicode(s.decode('utf-8')))
#    nkfd_form = unicodedata.normalize('NFKD', unicode(s))
#    return u"".join([c for c in nkfd_form if not unicodedata.combining(c)])
#
#    import unicodedata
#    return unicodedata.normalize("NFKD", unicode(s.decode('utf-8'))).encode('ascii')
#    return ''.join(x for x in unicodedata.normalize('NFKD', s) if x in string.ascii_letters).lower()
    ####
    convert = {
        'À' : 'A',
        'Á' : 'A',
        'Â' : 'A',
        'Ã' : 'A',
        'Ä' : 'A',
        'Å' : 'A',
        'Æ' : 'AE',
        'à' : 'a',
        'á' : 'a',
        'â' : 'a',
        'ã' : 'a',
        'ä' : 'a',
        'å' : 'a',
        'æ' : 'ae',
        #
        'ç' : 'c',
        'Ç' : 'C',
        #
        'È' : 'E',
        'É' : 'E',
        'Ê' : 'E',
        'Ë' : 'E',
        'è' : 'e',
        'é' : 'e',
        'ê' : 'e',
        'ë' : 'e',
        #
        'Ì' : 'I',
        'Í' : 'I',
        'Î' : 'I',
        'Ï' : 'I',
        'ì' : 'i',
        'í' : 'i',
        'î' : 'i',
        'ï' : 'i',
        #
        'Ñ' : 'N',
        'ñ' : 'n',
        #
        'Ò' : 'O',
        'Ó' : 'O',
        'Ô' : 'O',
        'Õ' : 'O',
        'Ö' : 'O',
        'Ø' : 'O',
        'ò' : 'o',
        'ó' : 'o',
        'ô' : 'o',
        'õ' : 'o',
        'ö' : 'o',
        'ø' : 'o',
        #
        'ß' : 'ss',
        #
        'Ù' : 'U',
        'Ú' : 'U',
        'Û' : 'U',
        'Ü' : 'U',
        'ù' : 'u',
        'ú' : 'u',
        'û' : 'u',
        'ü' : 'u',
        #
        'Ý' : 'Y',
        'ý' : 'y',
        'ÿ' : 'y',
    }
    for k in convert.keys():
        s = s.replace(k, convert[k])
    return s
# end remove_accents


# ************************************************************************************
#                                       tests
# ************************************************************************************
if __name__ == '__main__':
    
    def test_remove_accents():
        print remove_accents("avé des àccents, ç plùs dur Øòó")
    test_remove_accents()
    

