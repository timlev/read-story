import os

#filename = "missing_words.txt"
filename = "missing_words/The One That Got Away.html_missing_words.txt"
soundsdir = "/home/levtim/GitProjects/read-story/sounds"

soundlist = os.listdir(soundsdir)


soundlist = [x.replace(".mp3","") for x in soundlist if not x.startswith(".")]

wordlist = []

with open(filename, "rb") as fp:
    wordlist = fp.readlines()

wordlist = [x.rstrip() for x in wordlist if not x.startswith(".")]


missing_words = [x for x in wordlist if x not in soundlist]

print missing_words

def record(word, directory = "./"):
    os.system('rec "' + os.path.join(directory, word) + '.wav"')
def convert(word, directory = "./"):
    os.system('avconv -i "' + os.path.join(directory, word) + '.wav" "' + os.path.join(directory, word) + '.mp3"')
def remove_wave(filename, directory = "./"):
    os.remove(os.path.join(directory, filename))
    print "rm " + filename

for word in missing_words:
    print "\n\n\n\n\n"
    print word
    print "**********************************************"
    print "\n\n\n\n\n"
    record(word, soundsdir)


for word in missing_words:
    convert(word, soundsdir)

for word in missing_words:
    remove_wave(word + ".wav", soundsdir)
