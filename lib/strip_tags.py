# -*- encoding: utf8 -*-
'''******************************************************************************
    @licence    LGPL
    @author     Thierry Graff
    @history    2009.12.04 : Creation
********************************************************************************'''


# ***************************************************
def strip_tags(html):
    '''
    Removes html tags from a string
    '''
    from html.parser import HTMLParser
    result = []
    parser = HTMLParser()
    parser.handle_data = result.append
    parser.feed(html)
    parser.close()
    return ''.join(result)
# end strip_tags


# ************************************************************************************
#                                       tests
# ************************************************************************************
if __name__ == '__main__':
    def test_strip_tags():
        print(strip_tags('<html>une phrase avec <b>du gras</b></html>'))
        print(strip_tags('<html>une phrase avec <b align="none">du gras</b></html>'))
    #test_strip_tags()
    

