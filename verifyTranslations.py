#!/usr/bin/env python
#-*- coding: utf-8 -*-

import requests
from lib import notify_ambassador

def make_url(part, lang):
	return 'https://raw.githubusercontent.com/wikimedia/mediawiki-extensions-GrowthExperiments/master/i18n/%(part)s/%(lang)s.json' % { 'lang': lang, 'part': part }

parts = ['confirmemail', 'extension', 'help', 'homepage', 'welcomesurvey']
langs = ['cs']
mainlang = 'en'

for lang in langs:
	not_in_order = {}
	parts = set()
	for part in parts:
		not_in_order[part] = []
		main_messages = requests.get(make_url(part, mainlang)).json()
		lang_messages = requests.get(make_url(part, lang)).json()
		if len(main_messages) != len(lang_messages):
			for key in main_messages:
				if main_messages[key] == "":
					continue
				if key not in lang_messages:
					parts.add(part)
					not_in_order[part].append(key)
	notify_ambassador(lang, not_in_order, '[urgent] Translations of GrowthExperiments are not in order for %s (%s)' % (lang, ", ".join(parts)))
