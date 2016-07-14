from bs4 import BeautifulSoup, Tag
import string
filename = "The Animals at the Minnesota Zoo.html"
soup = BeautifulSoup(open(filename), "lxml")


paragraphs = soup.findAll('p')

header = soup.find('head')
arguments = [('src', "playsound.js")]
script = soup.new_tag("script", src="playsound.js")
header.insert(0, script)

body = soup.find('body')
arguments = [('id','player')]
audio = soup.new_tag("audio", id="player")
body.insert(0, audio)

def buildSpan(word, token, pnum, wnum):
    spanID = str(pnum) + str(wnum) + "_" + token
    tag = soup.new_tag("span", id=spanID, onclick="play(this)")
    tag.insert(0, word.encode('ascii','ignore'))
    return tag

master_word_list = []

for pnum, p in enumerate(paragraphs):
    words = p.text.replace("\n"," ").split(" ")
    p.string = ""
    if p.find("img"):
		img_tag = p.find("img").extract()
		print p, img_tag.name
    
    for wnum, word in enumerate(words):
        token = word.lower()
        token = "".join([x for x in token if x in string.ascii_letters])
        master_word_list.append(token)
        p.insert(wnum, buildSpan(word, token, pnum, wnum))
    #print p
#print soup

#Write out new html file
newfile = "new_" + filename
print "Saving new file ..."
with open(newfile, "wb") as wb:
  wb.write(soup.prettify(formatter="html"))
print "File saved at", newfile



master_word_list = list(set(master_word_list))
print master_word_list
problem_words = []


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


