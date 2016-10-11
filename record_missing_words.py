import os

#filename = "missing_words.txt"
filename = "words_to_record.txt"
soundsdir = "/home/levtim/GitProjects/read-story/sounds"

soundlist = os.listdir(soundsdir)


soundlist = [x.replace(".mp3","") for x in soundlist if not x.startswith(".")]

wordlist = []

with open(filename, "rb") as fp:
    wordlist = fp.readlines()

wordlist = [x.rstrip() for x in wordlist if not x.startswith(".")]


missing_words = [x for x in wordlist if x not in soundlist]

print missing_words
def record(word):
    os.system("rec " + word + ".wav")
def convert(word):
    os.system("avconv -i " + word + ".wav " + word + ".mp3")

for word in missing_words:
    #record(word)
    convert(word)

