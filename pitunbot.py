# -*- coding: utf-8 -*-

#            DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
#                    Version 2, December 2004

# Copyright (C) 2004 Sam Hocevar <sam@hocevar.net>

# Everyone is permitted to copy and distribute verbatim or modified
# copies of this license document, and changing it is allowed as long
# as the name is changed.

#            DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
#   TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION

#  0. You just DO WHAT THE FUCK YOU WANT TO.

import vk_api
import time
import random
import requests
import urllib
import json
import traceback
import ConfigParser
import os.path, sys

config = None

mamka = u'МАМКУ КОЖЕДЕДА ЕБАЛ))'

photos = [u'photo246855283_402012939',u'photo246855283_400065588',u'photo246855283_390112782',u'photo246855283_372545561',u'photo-85449651_357908801',u'photo-85449651_357908893',u'photo-85449651_357908911',u'photo-85449651_357909122']
pony = [u'ПЕТУХ ЗАКУКАРЕКАЛ!',u'ПАДИ ПАДМОЙСЯ, МАНЯ!',u'КОКОКОКОК',u'Что, простите?',u'Переведите с петушиного, пожалуйста.']

def load_config():
	global config
	config = ConfigParser.RawConfigParser()
	if not os.path.isfile('config.cfg'):
		config.add_section('vk')
		config.set('vk','login','login')
		config.set('vk','password','password')
		config.add_section('google')
		config.set('google','key','key')
		config.set('google','cx','cx')

		with open('config.cfg','wb') as config_file:
			config.write(config_file)

		print 'Config file was not found, creating default one and exit.'
		sys.exit()

	config.read('config.cfg')

def send_quote(data):
	r = requests.post("http://perevedko.pythonanywhere.com/add", data={'text': data})

def get_joke():
	msg = '[random kojeded\'s joke]'
	try:
		jokes = json.loads(urllib.urlopen('http://perevedko.pythonanywhere.com/jokes.json').read())
		jokes = set(jokes)
		msg = random.sample(jokes,1)
	except Exception as err:
		print 'error while retrieving jokes...'
		print err

	return msg

def getAneks():
	pass

def google(what,item_target='link'):
	msg = 'это какая-то хуйня'
	try:
		key = config.get('google','key')
		cx = config.get('google','cx')
		query = urllib.urlencode({'key':key, 'cx':cx, 'q':what.encode('utf-8')})
		search_res = urllib.urlopen('https://www.googleapis.com/customsearch/v1?'+query).read()
		search_res = unicode(search_res,'utf-8')
		with open('google.log','a') as log_file:
			log_file.write(search_res.encode('utf-8')+'\n\n')
		search_res = json.loads(search_res.encode('utf-8'))
		msg = search_res['items'][0][item_target]
	except Exception as err:
		print err
		traceback.print_exc()

	return msg

def main():
	login = config.get('vk','login')
	password = config.get('vk','password')
	vk_session = vk_api.VkApi(login, password)

	try:
		vk_session.authorization()
	except vk_api.AuthorizationError as error_msg:
		print error_msg
		return

	vk = vk_session.get_api()
	print 'Authorized!'

	while True:
		try:
			response = vk.messages.get()
		except Exception as err:
			print err
			time.sleep(10)
			next
		for r in response['items']:
			if r['user_id'] == 233657566 and r['read_state'] == 0:
				try:
					msg = random.choice(pony)
					vk.messages.send(chat_id=r['chat_id'],message=msg,forward_messages=r['id'])
				except Exception as err:
					print err
			if r['user_id'] == 51007975 and r['read_state'] == 0:
				send_quote(r['body'])
				msg = get_joke()
				try:
					vk.messages.markAsRead(message_ids=r['id'])
					res = vk.messages.send(chat_id=r['chat_id'],message=msg,forward_messages=r['id'])
				except requests.exceptions.ConnectionError as err:
					print err
			if u'питун' in r['body'] and r['read_state'] == 0:
				print r['body']
				words = r['body'].split(u'питун')
				print words[1]
				if words[1].strip() == u'мать':
					try:
						res = vk.messages.send(chat_id=r['chat_id'],message=mamka)
					except requests.exceptions.ConnectionError as err:
						print err
					print res
				elif u'цп в лс' in words[1].strip():
					res = vk.messages.send(chat_id=r['chat_id'],attachment=u'photo-114839877_413114704')
				elif u'солевую' in words[1].strip():
					photo = photos[random.randint(0,len(photos)-1)]
					res = vk.messages.send(chat_id=r['chat_id'],attachment=photo)
				elif u'кожешутку' in words[1].strip():
					msg = get_joke()
					try:
						res = vk.messages.send(chat_id=r['chat_id'],message=msg)
					except Exception as err:
						print err
				elif u'что такое' in words[1]:
					try:
						what = words[1].split(u'что такое')[1]
						msg = google(what,'snippet')
						vk.messages.send(chat_id=r['chat_id'],message=msg)
					except Exception as err:
						print err
						traceback.print_exc()
				elif u'гугл' in words[1]:
					try:
						what = words[1].split(u'гугл')[1]
						msg = google(what,'link')
						vk.messages.send(chat_id=r['chat_id'],message=msg)
					except Exception as err:
						print err
						traceback.print_exc()
				try:
					vk.messages.markAsRead(message_ids=r['id'])
				except Exception as err:
					print err
		time.sleep(5)

if __name__ == '__main__':
	load_config()
	main()


