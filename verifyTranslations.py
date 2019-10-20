#!/usr/bin/env python
#-*- coding: utf-8 -*-

import requests
import smtplib
from email.mime.text import MIMEText

notification_config = {
	'cs': ['murbanec-ctr@wikimedia.org', 'mmiller@wikimedia.org', 'bevellin@wikimedia.org'],
	'ar': ['hmhenni-ctr@wikimedia.org', 'mmiller@wikimedia.org', 'bevellin@wikimedia.org'],
	'ko': ['mmiller@wikimedia.org', 'bevellin@wikimedia.org'],
	'vi': ['ppham-ctr@wikimedia.org', 'mmiller@wikimedia.org', 'bevellin@wikimedia.org'],
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
			for msg in not_in_order[part]:
				notification += "<li>%s</li>\n" % msg['key']
			notification += "</ul>\n"
	if notification != "":
		msg = MIMEText(notification, 'html')
		msg['From'] = 'urbanecm@tools.wmflabs.org'
		msg['To'] = ", ".join(notification_config[lang])
		msg['Subject'] = '[urgent] Translations of GrowthExperiments are not in order for %s (%s)' % (lang, ", ".join(parts))
		s = smtplib.SMTP('mail.tools.wmflabs.org')
		s.sendmail('urbanecm@tools.wmflabs.org', notification_config[lang], msg.as_string())
		s.quit()

parts = [
	'ext-growthexperiments-confirmemail',
	'ext-growthexperiments-helppanel',
	'ext-growthexperiments-homepage',
	'ext-growthexperiments-welcomesurvey'
]

for lang in notification_config:
	not_in_order = {}
	for part in parts:
		r = requests.get('https://translatewiki.net/w/api.php', params={
			"action": "query",
			"format": "json",
			"list": "messagecollection",
			"mcgroup": part,
			"mclanguage": lang,
			"mclimit": "max",
			"mcfilter": "!optional|!ignored|!hastranslation"
		})
		not_in_order[part] = r.json()["query"]["messagecollection"]
	notify_ambassador(lang, not_in_order)
