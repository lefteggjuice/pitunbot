# -*- coding: utf-8 -*-

import re, random
orig = u'питун, быть или не быть?'
words = orig.split(u'питун')

com = re.sub(u',?','',words[1])
choices = com.split(u'или')
msg = choices[random.randint(0,1)].replace('?','')
msg = u'Ящитаю, '+msg

print msg