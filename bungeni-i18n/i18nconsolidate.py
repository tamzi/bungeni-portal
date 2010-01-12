#/usr/env/python
import getopt, sys
argv = sys.argv[1:]
tfile='/home/undesa/devel/svn/bungeni-portal/src/bungeni-i18n/%s.po' % argv[0]
translationfile = open(tfile,"r")
messages = {}
while translationfile:
    line = translationfile.readline()
    if line.startswith('msgid'):
        nl = translationfile.readline()
        if nl.startswith('msgstr'):
            messages[line.split('"')[1]] = nl.split('"')[1]
    if not line:
        break
translationfile.close()

dest = '%s/LC_MESSAGES/%spo' % (argv[0], argv[1][:-3])
outfile = open(dest,"w")

infile = open(argv[1], 'r')

while infile:
    line = infile.readline()
    if line.startswith('msgid'):
        nl = infile.readline()
        if nl.startswith('msgstr'):
            message = messages.get(line.split('"')[1], '')
            outfile.write( 'msgid "%s"\n' % line.split('"')[1])         
            outfile.write( 'msgid "%s"\n' % message)    
            outfile.write('#\n')                 
    if not line:
        break
infile.close()

