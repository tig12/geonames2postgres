# -*- encoding: utf8 -*-
'''******************************************************************************
    Implémenté pour mysql et postgresql
    
    @copyright  jetheme.org
    @history    2009.12.15 23:33:30, Thierry Graff : Integration of old code to jetheme
********************************************************************************'''

import sys
from pprint import pprint, pformat
from os.path import abspath, dirname

# ****************************
'''
    Returns a list with 2 elements : a connection object and a cursor
    @param  config          dictionary with keys : 'dbhost', 'dbuser', 'dbpassword', 'dbname', 'dbport', 'dbschema'
    @param create_schema    boolean. If True, missing schema(s) are created
'''
def get_postgresql_link(config, create_schema=False):
    # pypy compatibility
    # from psycopg2ct import compat
    # compat.register()
    #
    import psycopg2
    import psycopg2.extras
    import psycopg2.extensions
    psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
    
    params = dict(database=config['dbname'])
    if config.get('dbuser'):
        params['user'] = config['dbuser']
    if config.get('dbpassword'):
        params['password'] = config['dbpassword']
    if config.get('dbhost'):
        params['host'] = config['dbhost']
    if config.get('dbport'):
        params['port'] = config['dbport']

    #assert config.get('schema') and config.get('dbname'), 'dbname or schema %s missing' % config
    assert config.get('dbname'), 'dbname %s missing' % config

    x = psycopg2.connect(**params)
    cur = x.cursor()
    '''
    if create_schema:
        cur.execute("select nspname from pg_namespace where nspname=%s", (config['schema'],))
        if len(cur.fetchall()) == 0:
            print "create schema %s" % config['schema']
            cur.execute("create schema %s" % (config['schema'],))
    cur.execute("set schema %s",(config['schema'],))
    '''
    return x, cur
# end get_postgresql_link

