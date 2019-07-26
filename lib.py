#!/usr/bin/env python
#-*- coding: utf-8 -*-

import smtplib
from email.mime.text import MIMEText

notification_config = {
	'cs': ['murbanec-ctr@wikimedia.org']
}

def notify_ambassador(lang, not_in_order, subject):
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
		msg['Subject'] = subject
		s = smtplib.SMTP('mail.tools.wmflabs.org')
		s.sendmail('urbanecm@tools.wmflabs.org', notification_config[lang], msg.as_string())
		s.quit()
