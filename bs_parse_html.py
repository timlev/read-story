# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup, Tag
import string
import re
import argparse
import sys
import os
import download_wiktionary_word
import copy
import glob

def stripID(audioID):
    chunk = audioID[audioID.index("_") + 1:]
    return chunk

def tokenize_word(word):
    token = word.lower()
    token = "".join([x for x in token if x in string.ascii_letters + string.digits     + "-" +"'"])
    if token != "":
        return token
    else:
        return False


def buildAllAudio(master_word_list):
    for token in master_word_list:
        audioID = token + "_audio"
        source = "../sounds/" + token + ".mp3"
        audio = soup.new_tag("audio", id=audioID, src=source, type="audio/mpeg", preload="auto")#, oncanplaythrough="console.log(this)")
        #print audio
        body.append(audio)


def buildSpan(word, token, pnum, wnum):
    spanID = str(pnum) + str(wnum) + "_" + token
    tag = soup.new_tag("span", id=spanID, onclick="play(this)")
    tag.insert(0, word)
    return tag

def download_sound_files(master_word_list):
    print "Downloading sound files ..."
    soundfiles = [f.replace(".mp3","") for f in os.listdir("./sounds/") if f.endswith(".mp3")]

    for word in [word for word in master_word_list if word not in soundfiles]:
        downloaded_word = False
        try:
            oggpath = download_wiktionary_word.get_wiki(word, "./sounds/")
            if oggpath != 2:
                download_wiktionary_word.convert_ogg_to_mp3(oggpath, True)
                downloaded_word = True
        except:
            print "Could't convert from wiki", word
        if downloaded_word == False:
            try:
                mp3path = download_wiktionary_word.download_gstatic(word, "./sounds/")
            except:
                print "Couldn't download from GStatic"


parser = argparse.ArgumentParser()
parser.add_argument("input", nargs='+')
parser.add_argument("--output_dir", default="./html_output")
parser.add_argument("--index", default="./index.html")
parser.add_argument("--skip_sounds", action="store_true")
parser.add_arugment("--skip_index", action="store_true")
args = parser.parse_args(sys.argv[1:])

allfilenames = args.input

print "Files to analyze: {}".format(allfilenames)

for filename in allfilenames:
    print "Processing {} ...".format(filename)

    base_name = os.path.basename(filename)
    short_name = os.path.splitext(base_name)[0]

    #soup = BeautifulSoup(open(filename), "lxml")
    #soup = BeautifulSoup(open(filename), "html.parser")
    soup = BeautifulSoup(open(filename), "html5lib")
    paragraphs = soup.findAll('p')

    orig_header = soup.find('head')
    if orig_header is None:
        new_header = soup.new_tag("head")
    else:
        new_header = copy.copy(orig_header)
    script = soup.new_tag("script", src="../js/playsound.js")
    new_header.insert(0, script)
    if new_header.find("title") is None:
        new_header.insert(0, soup.new_tag("title"))
    new_header.title.string = short_name
    style = soup.new_tag('style', 'word-wrap: normal;')
    new_header.insert(0, style)

    styles = soup.findAll('style')
    for style in styles:
        if style.string is not None and "font-size" in style.string:
            style.string = re.sub("font-size\s*?:.*?;","font-size:2em;", style.string)
        if style.string is not None and "line-height" in style.string:
            style.string = re.sub("line-height\s*?:.*?%","", style.string)
        new_header.insert(0, style)

    font = soup.new_tag('link', href="https://fonts.googleapis.com/css?family=Didact+Gothic", rel="stylesheet")
    new_header.insert(0, font)

    fontstyles = soup.new_tag('style')
    fontstyles.string = "p {font-family: 'Didact Gothic', sans-serif; line-height: 1.5;text-indent: 5%;}\n span:hover {cursor: pointer;}"
    new_header.insert(0, fontstyles)

    if orig_header is None:
        soup.insert(0, new_header)
    else:
        orig_header.replace_with(new_header)

    body = soup.find('body')
    body['style'] = "font-size:2em"
    #arguments = [('id','player')]
    audio = soup.new_tag("audio", id="player", type="audio/mpeg", preload="auto")
    body.insert(0, audio)

    fspimg = soup.new_tag("img", src="../images/plus-800px.png", onclick='increaseFont()')
    fsmimg = soup.new_tag("img", src="../images/minus-800px.png", onclick='decreaseFont()')
    body.insert(0,fsmimg)
    body.insert(0,fspimg)

    #Build Master Word List
    master_word_list = []

    for pnum, p in enumerate(paragraphs):
        words = p.text.replace("\n"," ").split(" ")
        #print words
        p.string = ""
        #print words
        for pos, word in enumerate(words):
            if u'\u2019' in word:
                words[pos] = word.replace(u'\u2019', "'")
            if u'\u201c' in word:
                words[pos] = word.replace(u'\u201c', '"')
            if u'\u201d' in word:
                words[pos] = word.replace(u'\u201d', '"')
            if u'\u2014' in word:
                words[pos] = word.replace(u'\u2014', '--')
        words = [x.encode('ascii', errors='ignore') for x in words]


        #words = [word.encode('ascii', 'xmlcharrefreplace') for word in words]
        print words
        if 'style' in p and "line-height" in p['style']:
            #print p['style']
            p['style'] = re.sub("line-height\s*?:.*?%","", p['style'])
        for wnum, word in enumerate(words):
            token = tokenize_word(word)
            if token != False:
                master_word_list.append(token)
                p.insert(wnum, buildSpan(word, token, pnum, wnum))


    master_word_list = list(set(master_word_list))
    buildAllAudio(master_word_list)

    #Write out new html file
    newfile = args.output_dir + "/new_" + base_name
    print "Saving new file ..."
    with open(newfile, "wb") as wb:
      wb.write(soup.prettify(formatter="html"))
    print "File saved at", newfile

    #Add to Index
    if not args.skip_index:
        index = BeautifulSoup(open(args.index), "html5lib")
        new_link = index.new_tag('a', href = newfile)
        new_link.string = short_name
        index.body.append(index.new_tag('br'))
        index.body.append(new_link)

        #Write Index file
        print "Updating index.html..."
        with open(args.index, "wb") as wb:
          wb.write(index.prettify(formatter="html"))
        print "File saved at " + args.index

    #Download Words
    if not args.skip_sounds:
        download_sound_files(master_word_list)

    soundfiles = [f.replace(".mp3","") for f in os.listdir("./sounds/") if f.endswith(".mp3")]
    missing_words = "\n".join([word for word in master_word_list if word not in soundfiles])

    with open("missing_words/" + base_name + "_missing_words.txt","wb") as wb:
        wb.write(missing_words)
