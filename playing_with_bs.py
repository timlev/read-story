# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup, Tag
import string, re


filename = "prefixes.html"
soup = BeautifulSoup(open(filename), "lxml")


paragraphs = soup.findAll('p')

"""for s in soup('span'):
	if s.string != None:
		print [x.encode(errors='ignore') for x in s.string.split(" ")]
"""
for p in paragraphs:
	if p.text.encode(errors="ignore") != "":
		p.string = " ".join([x.encode(errors="ignore") for x in p.text.split(" ")])
	else:
		p.extract()
print paragraphs
	#print [x.encode(errors="ignore") for x in p.contents]
	#for item in p.descendants:
		#print item
"""
	#for item in p.contents:
		#print item.find_all("span")
		#print item.extract()
			#print item.unwrap()

	for item in p.contents:
		print item.string
		if item.string != None:
			print item.string
			print [x.encode(errors="ignore") for x in item.string.split(" ")]
"""
