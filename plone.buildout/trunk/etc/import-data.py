#!/usr/bin/python
import urllib

username = ''
password = ''
url = 'localhost:8082/site'

ids_to_transfer = ['front-page', 'have-your-say', 'how-we-work', 'reference-material']

for id in ids_to_transfer:

    urllib.urlopen('http://%s:%s@%s/manage_delObjects?ids=%s' % (username, password, url, id))
    urllib.urlopen('http://%s:%s@%s/manage_importObject?file=%s.zexp' % (username, password, url,id))

print "Data imported successfully"    
