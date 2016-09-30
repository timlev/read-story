# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup, Tag
import string,re
filename = "Voting in the United States.html"
#filename = "ApartmentManagerConversation.html"
soup = BeautifulSoup(open(filename), "lxml")
#soup = BeautifulSoup(open(filename))


paragraphs = soup.findAll('p')

header = soup.find('head')
#arguments = [('src', "playsound.js")]
script = soup.new_tag("script", src="playsound.js")
header.insert(0, script)
header.title.string = filename.replace(".html","")
print header.find_all('style')
#arguments = [('style', 'word-wrap: normal;')]
style = soup.new_tag('style', 'word-wrap: normal;')
styles = soup.findAll('style')

for style in styles:
	if "font-size" in style.string:
		style.string = re.sub("font-size\s*?:.*?;","font-size:1em;", style.string)
header.insert(0,style)

body = soup.find('body')
body['style'] = "font-size:1em"
#arguments = [('id','player')]
audio = soup.new_tag("audio", id="player", type="audio/mpeg", preload="auto")
body.insert(0, audio)

fspimg = soup.new_tag("img", src="plus-800px.png", onclick='increaseFont()')
fsmimg = soup.new_tag("img", src="minus-800px.png", onclick='decreaseFont()')
body.insert(0,fsmimg)
body.insert(0,fspimg)

def stripID(audioID):
    chunk = audioID[audioID.index("_") + 1:]
    return chunk

def tokenize_word(word):
    token = word.lower()
    token = "".join([x for x in token if x in string.ascii_letters])
    if token != "":
        return token
    else:
        return False


def buildAllAudio(master_word_list):
    for token in master_word_list:
        audioID = token + "_audio"
        source = "sounds/" + token + ".mp3"
        audio = soup.new_tag("audio", id=audioID, src=source, type="audio/mpeg", preload="auto")#, oncanplaythrough="console.log(this)")
        print audio
        body.append(audio)

    
def buildSpan(word, token, pnum, wnum):
    spanID = str(pnum) + str(wnum) + "_" + token
    tag = soup.new_tag("span", id=spanID, onclick="play(this)")
    tag.insert(0, word)
    return tag


#Build Master Word List
master_word_list = []

for pnum, p in enumerate(paragraphs):
    words = p.text.replace("\n"," ").split(" ")
    if "<b>" in p:
		print p
    p.string = ""
    words = [x.encode('ascii',errors='ignore') for x in words]
    if p.find("img"):
		img_tag = p.find("img").extract()
		print p, img_tag.name
    
    for wnum, word in enumerate(words):
        token = tokenize_word(word)
        if token != False:
            master_word_list.append(token)
            p.insert(wnum, buildSpan(word, token, pnum, wnum))


master_word_list = list(set(master_word_list))
buildAllAudio(master_word_list)

#Write out new html file
newfile = "new_" + filename
print "Saving new file ..."
with open(newfile, "wb") as wb:
  wb.write(soup.prettify(formatter="html"))
print "File saved at", newfile


#Download Words
problem_words = []

print "Downloading sound files ..."
import download_dict_sound_rough, os
soundfiles = [f.replace(".mp3","") for f in os.listdir("./sounds/") if f.endswith(".mp3")]

for word in [word for word in master_word_list if word not in soundfiles]:
    try: download_dict_sound_rough.dictionary_rough_search(word,"./sounds/")
    except:
        problem_words.append(word)
            

soundfiles = [f.replace(".mp3","") for f in os.listdir("./sounds/") if f.endswith(".mp3")]

for word in [word for word in master_word_list if word not in soundfiles]:
	try:
		download_dict_sound_rough.download_wiktionary(word, "./sounds/")
		download_dict_sound_rough.convert_ogg_to_mp3(os.path.join(os.path.relpath("./sounds/"), word + ".ogg"), remove_ogg = True)
	except:
		print "Could't convert", word

soundfiles = [f.replace(".mp3","") for f in os.listdir("./sounds/") if f.endswith(".mp3")]


missing_words = "\n".join([word for word in master_word_list if word not in soundfiles])

with open("missing_words.txt","wb") as wb:
    wb.write(missing_words)



