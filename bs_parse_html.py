import BeautifulSoup
filename = "The Animals at the Minnesota Zoo.html"
soup = BeautifulSoup.BeautifulSoup(open(filename))


paragraphs = soup.findAll('p')

header = soup.find('head')
arguments = [('src', "playsound.js")]
script = BeautifulSoup.Tag(soup, "script", arguments)
header.insert(0, script)

body = soup.find('body')
arguments = [('id','player')]
audio = BeautifulSoup.Tag(soup, "audio", arguments)
body.insert(0, audio)

def buildSpan(word, token, pnum, wnum):
	arguments = [("id", str(pnum) + str(wnum) + "_"+ token), ("onclick","play(this)")]
	tag = BeautifulSoup.Tag(soup, "span", arguments)
	tag.insert(0, word)
	return tag


for pnum, p in enumerate(paragraphs):
	words = p.text.replace("\n"," ").split(" ")
	p.replaceWholeText = ""
	for wnum, word in enumerate(words):
		token = word.lower()
		p.insert(wnum, buildSpan(word, token, pnum, wnum))
	#print p
print soup

#Write out new html file
newfile = "new_" + filename

with open(newfile, "wb") as wb:
  wb.write(soup.prettify())
