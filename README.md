
This code loads geonames data in a postgresql database.  
In the target database, each country is stored in a schema.  
Each schema contain the following tables :
- admin1  
- admin2  
- admin3  
- admin4  
- cities  
- postal  

For each entity, a slug is computed.

Complete structure of the tables can be seen in directory <code>sql/</code>.

<h2>Install</h2>

- Copy <code>config.yml.dist</code> to <code>config.yml</code>  
- Adapt the parameters in <code>config.yml</code>

<h2>Usage</h2>

Type :
<pre>python geonames2postgres.py</pre>
and follow usage instructions

<h2>About postal codes</h2>

In geonames.org, postal codes are not stored with city informations, but in separate files (because one city can have several postal codes).  
This code tries to merge the two lists, and associates a postal code to each city. When one city has several postal codes, the first one is retained. This generally (always ?) correspond to the most generic code of the city, but the merge process remains basic. For a better merge of postal codes, see <a href="https://pypi.python.org/pypi/django-cities">https://pypi.python.org/pypi/django-cities</a>