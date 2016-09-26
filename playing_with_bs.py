# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup, Tag
import string, re


filename = "prefixes.html"
soup = BeautifulSoup(open(filename), "lxml")


paragraphs = soup.findAll('p')

for p in paragraphs:
	for item in p.contents:
		print item
		#print item.extract()
			#print item.unwrap()
"""
	for item in p.contents:
		print item.string
		if item.string != None:
			print item.string
			print [x.encode(errors="ignore") for x in item.string.split(" ")]
"""
