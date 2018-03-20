#!/usr/bin/env python3
# -*- coding: utf8 -*-

import requests
import html.parser

try:
	r = requests.get(url='https://www.chucknorrisfacts.fr/api/get?data=tri:alea;type:txt;nb:1;')
	fact = r.json()[0]["fact"]
	fact = html.parser.HTMLParser().unescape(fact)

	print(fact)
except:
	exit(1)