#!/usr/bin/python
# -*- encoding: utf8 -*-
"""
    Import geonames.org in postgres
    Compute postal codes of cities when possible
    
    @license    GPL
    @copyright  Thierry Graff
    @history    2014-01-12 23:11:43+01:00, Thierry Graff, creation from old code
    @history    2017-05-02 09:12:34+02:00, Thierry Graff, convert to autonom program
    
    @todo better merge of postal code, see https://pypi.python.org/pypi/django-cities
"""
import sys
import os
from os.path import abspath, dirname
from pprint import pprint, pformat
import csv; csv.field_size_limit(1000000000)
import yaml
import glob
from datetime import datetime

ACTION_ALL = 'all'

DS = os.sep # directory separator

USAGE = '''usage: python import_geonames.py <action>
  <action> can be a country code or 'ALL' (or 'all')
ex: python geonames2postgres.py FR
ex: python geonames2postgres.py ALL
if action = 'ALL', imports all the countries located in countries directory
Some countries do not have postal codes'''

dir_root = dirname(abspath(__file__))

sys.path.append(dir_root + DS + 'lib')
from dirify import dirify
from microtime import microtime
import DB

yamlfile = dir_root + DS + 'config.yml'
yamlarray = yaml.load(file(yamlfile, 'r'), Loader=yaml.BaseLoader)

dbgeo, curgeo = DB.get_postgresql_link(yamlarray['postgresql'])

dir_countries = yamlarray['dir-countries']
dir_postal = yamlarray['dir-postal']
dir_sql = dir_root + DS + 'sql'

# fields of cities files
FIELDS_CITIES = (
    'geonameid',         # integer id of record in geonames database
    'name',              # name of geographical point (utf8) varchar(200)
    'asciiname',         # name of geographical point in plain ascii characters, varchar(200)
    'alternatenames',    # alternatenames, comma separated varchar(5000)
    'latitude',          # latitude in decimal degrees (wgs84)
    'longitude',         # longitude in decimal degrees (wgs84)
    'feature_class',     # see http://www.geonames.org/export/codes.html, char(1)
    'feature_code',      # see http://www.geonames.org/export/codes.html, varchar(10)
    'country_code',      # ISO-3166 2-letter country code, 2 characters
    'cc2',               # alternate country codes, comma separated, ISO-3166 2-letter country code, 60 characters
    'admin1_code',       # fipscode (subject to change to iso code), see exceptions below, see file admin1Codes.txt for display names of this code; varchar(20)
    'admin2_code',       # code for the second administrative division, a county in the US, see file admin2Codes.txt; varchar(80) 
    'admin3_code',       # code for third level administrative division, varchar(20)
    'admin4_code',       # code for fourth level administrative division, varchar(20)
    'population',        # bigint (8 byte int) 
    'elevation',         # in meters, integer
    'dem',               # digital elevation model, srtm3 or gtopo30, average elev. of 3''x3'' (ca 90mx90m) or 30''x30'' (ca 900mx900m) area in meters, integer. srtm processed by
    'timezone',          # the timezone id (see file timeZone.txt) varchar(40)
    'modification_date', # date of last modification in yyyy-MM-dd format
)

# fields of postal files
FIELDS_POSTAL = (
    'country_code',      # iso country code, 2 characters
    'postal_code',       # varchar(20)
    'place_name',        # varchar(180)
    'admin_name1',       # 1. order subdivision (state) varchar(100)
    'admin_code1',       # 1. order subdivision (state) varchar(20)
    'admin_name2',       # 2. order subdivision (county/province) varchar(100)
    'admin_code2',       # 2. order subdivision (county/province) varchar(20)
    'admin_name3',       # 3. order subdivision (community) varchar(100)
    'admin_code3',       # 3. order subdivision (community) varchar(20)
    'latitude',          # estimated latitude (wgs84)
    'longitude',         # estimated longitude (wgs84)
    'accuracy',          # accuracy of lat/lng from 1=estimated to 6=centroid
)


# **************************************
def perform_action(action):
    '''
        Entry point to import one or several geonames files
    '''
    # available countries
    os.chdir(dir_countries)
    countries = []
    files = sorted(glob.glob('*.zip')) # ex FR.zip
    for f in files:
        countries.append(f[:-4])
    #
    # available postal codes
    os.chdir(dir_postal)
    postals = []
    files = sorted(glob.glob('*.zip')) # ex FR.zip
    for f in files:
        postals.append(f[:-4])
    #
    #
    if action.lower() == ACTION_ALL:
        actions = countries
    else:
        actions = [action]
    #
    # perform actions
    for country in actions:
        if country not in countries:
            print "ERROR : Unable to import country " + country
            print "(missing file " + dir_countries + DS + country + ".zip)"
            continue
        postal = True if country in postals else False
        import_country(country, postal)


# **************************************
def create_country_tables(do_postal):
    '''
        Creates the tables in a schema of a country
    '''
    create_table('cities')
    if do_postal:
        create_table('postal')
    create_table('admin1')
    create_table('admin2')
    create_table('admin3')
    create_table('admin4')
    curgeo.execute("create index idx_cities_slug on cities(slug)")
    curgeo.execute("create index idx_cities_geoid on cities(geoid)")
    if do_postal:
        curgeo.execute("create index idx_postal_slug on postal(place_slug)")


# **************************************
def create_table(table):
    curgeo.execute("drop table if exists " + table + " cascade")
    text = 'create table ' + table + '(' + open(dir_sql + DS + table).read() + ')'
    curgeo.execute(text)


# **************************************
def import_country(country, do_postal):
    '''
        Stores one country file in database
        @param country ISO 3166
        @param do_postal boolean
    '''
    # @todo put in param
    do_create_table = True
    do_import_cities = True
    do_import_postal = True
    do_merge_postal = True
    #
    #
    from zipfile import ZipFile
    schema = dirify(country, '_') # lower() enough for all countries, except for "no-country"
    #
    if do_create_table:
    #
        t1 = microtime(True)
        # create schema if needed
        curgeo.execute("select nspname from pg_namespace where nspname=%s", (schema,))
        if len(curgeo.fetchall()) == 0:
            print "create schema %s" % schema
            curgeo.execute("create schema %s" % (schema,))
        curgeo.execute("set schema %s",(schema,))
        create_country_tables(do_postal)
        dbgeo.commit()
        t2 = microtime(True)
        dt = t2 - t1
        print country, "created tables in", round(dt, 2), "s"
    curgeo.execute("set schema %s",(schema,))
    #
    if do_import_cities:
    #
        t1 = microtime(True)
        # extract and read
        myzip = ZipFile(dir_countries + DS + country + '.zip', 'r')
        filename = country + '.txt'
        csvreader = csv.reader(myzip.open(filename), delimiter='\t')
        myzip.close()
        try:
            for row in csvreader:
                cur = {}
                for i, field in enumerate(row):
                    cur[FIELDS_CITIES[i]] = field
                if 'feature_class' not in cur:
                    continue
                if cur['feature_class'] == 'P' and (cur['feature_code'][:3] == 'PPL' or cur['feature_code'][:3] == 'PPH') :
                    import_ppl(cur)
                elif cur['feature_class'] == 'A' and cur['feature_code'][:3] == 'ADM':
                    import_adm(cur)
                else:
                    pass
        except:
            dbgeo.rollback()
            print "ERROR in country", country, ':', sys.exc_info()[1], '- database NOT affected for this country'
            raise
        dbgeo.commit()
        t2 = microtime(True)
        dt = t2 - t1
        print country, "imported cities + adm in", round(dt, 2), "s"
    #
    if do_import_postal and do_postal:
    #
        t1 = microtime(True)
        # extract and read
        myzip = ZipFile(dir_postal + DS + country + '.zip', 'r')
        filename = country + '.txt'
        csvreader = csv.reader(myzip.open(filename), delimiter='\t')
        myzip.close()
        try:
            for row in csvreader:
                cur = {}
                for i, field in enumerate(row):
                    cur[FIELDS_POSTAL[i]] = field
                import_postal(cur)
        except :
            dbgeo.rollback()
            print "ERROR in country", country, ':', sys.exc_info()[1], '- database NOT affected for this country'
            raise
        dbgeo.commit()
        t2 = microtime(True)
        dt = t2 - t1
        print country, "imported postal in", round(dt, 2), "s"
    #
    if do_merge_postal and do_postal:
    #
        t1 = microtime(True)
        schema = country.lower()
        curgeo.execute("select * from " + schema + ".cities")
        rows1 = curgeo.fetchall()
        ngood = nbad = 0
        for r1 in rows1:
            geoid = r1[0]
            # for each city, find the first row of table postal with slug_place
            # consider that the first postal code found is ok
            # à priori coherent, the most generic code of a place is (always?) the first row
            curgeo.execute("select * from " + schema + ".postal where place_slug=%s order by postal_code limit 1", (r1[2],))
            rows2 = curgeo.fetchall()
            if len(rows2) == 0:
                nbad += 1
                continue
            for r2 in rows2:
                query = "update " + country + ".cities set postal_code='" + r2[0] + "' where geoid='" + geoid + "'"
                curgeo.execute(query)
                ngood += 1
        dbgeo.commit()
        t2 = microtime(True)
        dt = t2 - t1
        ntotal = ngood + nbad
        print country, "merged postal in", round(dt, 2), "s -", 'nb of merged postal codes :', ngood, '/', ntotal


# **************************************
def import_postal(row):
    ''' Stores one postal code (= one row of table postal) '''
#    pprint(row)
#    sys.exit()
    curgeo.execute("insert into postal values(%s, %s, %s, %s, %s, %s, %s, %s, %s)",(
        row['postal_code'],
        row['place_name'],
        dirify(row['place_name']),
        row['admin_code1'],
        row['admin_code2'],
        row['admin_code3'],
        row['latitude'],
        row['longitude'],
        row['accuracy']
    ))


# **************************************
def import_ppl(row):
    ''' Stores one populated place (= one row of table cities) '''
    capital_of = ''
    if len(row['feature_code']) > 3:
        if row['feature_code'] == 'PPLA':
            capital_of = row['admin1_code']
        elif row['feature_code'] == 'PPLA2':
            capital_of = row['admin2_code']
        elif row['feature_code'] == 'PPLA3':
            capital_of = row['admin3_code']
        elif row['feature_code'] == 'PPLA4':
            capital_of = row['admin4_code']
    curgeo.execute("insert into cities values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",(
        row['geonameid'],
        row['name'],
        dirify(row['asciiname']),
        row['country_code'],
        '', # postal code
        row['population'],
        row['timezone'],
        row['latitude'],
        row['longitude'],
        row['elevation'],
        row['alternatenames'],
        capital_of,
        row['admin1_code'],
        row['admin2_code'],
        row['admin3_code'],
        row['admin4_code']
    ))


# **************************************
def import_adm(row):
    ''' Stores one administrative area (= one row of table admin*) '''
    if row['feature_code'] == 'ADM1':   table = 'admin1'
    elif row['feature_code'] == 'ADM2': table = 'admin2'
    elif row['feature_code'] == 'ADM3': table = 'admin3'
    elif row['feature_code'] == 'ADM4': table = 'admin4'
    else:
        return
    ncols = int(row['feature_code'][-1]) + 8
    str_percent = '%s,' * (ncols - 1) + '%s'
    inserted_row = [
        row['geonameid'],
        row['name'],
        dirify( row['asciiname']),
        row['alternatenames'],
        '', # @todo geoid_capital
        row['country_code'],
        row['admin1_code']
    ]
    if ncols > 9:  inserted_row.append(row['admin2_code'])
    if ncols > 10: inserted_row.append(row['admin3_code'])
    if ncols > 11: inserted_row.append(row['admin4_code'])
    inserted_row.append(row['population'])
    inserted_row.append(row['timezone'])
    curgeo.execute("insert into " + table + " values(" + str_percent + ")", tuple(inserted_row))


# **************************************
def dump(row):
    print row['geonameid'].ljust(10), row['feature_class'], row['feature_code'].ljust(5), row['name'].ljust(30), row['admin1_code'].ljust(10), row['admin2_code'].ljust(10), row['admin3_code'].ljust(10), row['admin4_code'].ljust(10), row['population'].ljust(10)


# **************************************
if __name__ == '__main__':
    def main():
        if len(sys.argv) != 2:
            print USAGE
            sys.exit()
        perform_action(sys.argv[1])
    main()


