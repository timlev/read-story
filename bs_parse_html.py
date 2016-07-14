from bs4 import BeautifulSoup, Tag
import string
filename = "The Animals at the Minnesota Zoo.html"
soup = BeautifulSoup(open(filename), "lxml")


paragraphs = soup.findAll('p')

header = soup.find('head')
arguments = [('src', "playsound.js")]
script = soup.new_tag("script", arguments)
header.insert(0, script)

body = soup.find('body')
arguments = [('id','player')]
audio = soup.new_tag("audio", arguments)
body.insert(0, audio)

def buildSpan(word, token, pnum, wnum):
    arguments = [("id", str(pnum) + str(wnum) + "_"+ token), ("onclick","play(this)")]
    tag = soup.new_tag("span", arguments)
    tag.insert(0, word)
    return tag

master_word_list = []

for pnum, p in enumerate(paragraphs):
    words = p.text.replace("\n"," ").split(" ")
    p.string = ""
    for wnum, word in enumerate(words):
        token = word.lower()
        token = "".join([x for x in token if x in string.ascii_letters])
        master_word_list.append(token)
        p.insert(wnum, buildSpan(word, token, pnum, wnum))
    #print p
print soup

#Write out new html file
newfile = "new_" + filename

#with open(newfile, "wb") as wb:
#  wb.write(soup.prettify())

master_word_list = list(set(master_word_list))
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

