#!/usr/bin/env python
#-*- coding: utf-8 -*-

import requests
import smtplib
from email.mime.text import MIMEText

notification_config = {
	'cs': ['murbanec-ctr@wikimedia.org', 'mmiller@wikimedia.org'],
	'ar': ['hmhenni-ctr@wikimedia.org', 'mmiller@wikimedia.org'],
	'ko': ['mmiller@wikimedia.org'],
}

def notify_ambassador(lang, not_in_order):
	if lang not in notification_config:
		return
	notification = ""
	parts = []
	for part in not_in_order:
		if len(not_in_order[part]) > 0:
			parts.append(part)
			notification += "<h1>%s</h1>\n" % part
			notification += "<ul>\n"
			for key in not_in_order[part]:
				notification += "<li>%s</li>\n" % key
			notification += "</ul>\n"
	if notification != "":
		msg = MIMEText(notification, 'html')
		msg['From'] = 'urbanecm@tools.wmflabs.org'
		msg['To'] = ", ".join(notification_config[lang])
		msg['Subject'] = '[urgent] Translations of GrowthExperiments are not in order for %s (%s)' % (lang, ", ".join(parts))
		s = smtplib.SMTP('mail.tools.wmflabs.org')
		s.sendmail('urbanecm@tools.wmflabs.org', notification_config[lang], msg.as_string())
		s.quit()

def make_url(part, lang):
	return 'https://raw.githubusercontent.com/wikimedia/mediawiki-extensions-GrowthExperiments/master/i18n/%(part)s/%(lang)s.json' % { 'lang': lang, 'part': part }

parts = ['confirmemail', 'extension', 'help', 'homepage', 'welcomesurvey']
mainlang = 'en'

for lang in notification_config:
	not_in_order = {}
	for part in parts:
		not_in_order[part] = []
		main_messages = requests.get(make_url(part, mainlang)).json()
		lang_messages = requests.get(make_url(part, lang)).json()
		if len(main_messages) != len(lang_messages):
			for key in main_messages:
				if main_messages[key] == "":
					continue
				if key not in lang_messages:
					not_in_order[part].append(key)
	notify_ambassador(lang, not_in_order)
