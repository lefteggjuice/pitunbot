# -*- coding: utf-8 -*-

import re, random, urllib, json
def choiser():
	orig = u'питун, пилить тебя дальше или заняться работой?'
	words = orig.split(u'питун')

	com = re.sub(u',?','',words[1])
	m = re.match(ur'(.+)\s+или\s+(.+)',com)
	print m.group(1)
	print m.group(2)
	choices = [m.group(1),m.group(2)]
	msg = choices[random.randint(0,1)].replace('?','')
	msg = u'Ящитаю, '+msg

	print msg

def currency():
	res = urllib.urlopen('https://api.fixer.io/latest?base=USD&symbols=RUB').read()
	obj = json.loads(res)
	price = obj['rates']['RUB']
	msg = str(price)+u' деревянных за доллар. Скален!'

	print msg

def delimiter():
	r = {'body':u'кожешутку!'}

	m = re.match(u'питун,?\s*?(.+)',r['body'],re.I | re.U)
	if not m:
		print 'NEXT'
		return
	words = [u'питун',m.group(1)] #words are DEPRICATED and will be removed soon.

	print words[1]

delimiter()
