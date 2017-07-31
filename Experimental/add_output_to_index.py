# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup, Tag
import os, string

#Add to Index
index = BeautifulSoup(open("/home/levtim/GitProjects/read-story/index.html"), "lxml")

htmlfiles = [os.path.relpath(x) for x in os.listdir("/home/levtim/GitProjects/read-story/html_output") if x.endswith(".html")]
print htmlfiles
for newfile in htmlfiles:
	print newfile, type(newfile)

for newfile in htmlfiles:
    base_name = os.path.basename(newfile)
    short_name = os.path.splitext(base_name)[0]
    newfile = os.path.join("html_output",newfile)
    new_link = index.new_tag('a', href = newfile)
    new_link.string = short_name
    index.body.append(index.new_tag('br'))
    index.body.append(new_link)
    print '<a href="' + newfile + '"> ' + short_name + '</>'
"""
    #Write Index file
    print "Updating index.html..."
    with open(index, "wb") as wb:
      wb.write(index.prettify(formatter="html"))
    print "File saved at index.html"
"""
