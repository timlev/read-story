# -*- coding: utf-8 -*-

import os, argparse, sys, platform

parser = argparse.ArgumentParser()
parser.add_argument("input", nargs='+')
parser.add_argument("--output_dir", default="./sounds")
#parser.add_argument("--skip_sounds", action="store_true")
args = parser.parse_args(sys.argv[1:])

print(args.input)

def record(word, directory = args.output_dir):
    os.system('rec "' + os.path.join(directory, word) + '.wav"')
def convert(word, directory = "./"):
    wavpath = os.path.join(directory, word) + '.wav'
    mp3path = os.path.join(directory, word) + '.mp3'
    #if platform.system() == 'Linux':
        #os.system('avconv -i "' + wavpath + '" "' + mp3path + '"')
   # else:
    os.system('ffmpeg -i "' + wavpath + '" -acodec libmp3lame "' + mp3path + '"')

def remove_wave(filename, directory = "./"):
    os.remove(os.path.join(directory, filename))
    print("rm " + filename)


#filename = "missing_words.txt"
#filename = "missing_words/The One That Got Away.html_missing_words.txt"
#filename = "missing_words/Jumping In.html_missing_words.txt"
#filename = "missing_words/George Washington Carver.html_missing_words.txt"
#filename = "missing_words/Early Birds.html_missing_words.txt"
#filename = "missing_words/The One That Got Away.html_missing_words.txt"
allfilenames = args.input
for filename in allfilenames:
    #soundsdir = "/home/levtim/GitProjects/read-story/sounds"
    #soundsdir = "./sounds"
    soundsdir = args.output_dir

    soundlist = os.listdir(soundsdir)

    soundlist = [x.replace(".mp3","") for x in soundlist if not x.startswith( '.' )]

    wordlist = []

    with open(filename, "r+") as fp:
        wordlist = fp.readlines()
    print(wordlist)
    wordlist = [str(x).rstrip() for x in wordlist if not str(x).startswith( '.' )]


    missing_words = [x for x in wordlist if x not in soundlist]

    print(missing_words)

    for word in missing_words:
        print("\n\n\n\n\n")
        print(word)
        print("**********************************************")
        print("\n\n\n\n\n")
        record(word, soundsdir)
        #record(word)


    for word in missing_words:
        convert(word, soundsdir)
        #convert(word)

    for word in missing_words:
        remove_wave(word + ".wav", soundsdir)
        #remove_wave(os.path.join(soundsdir, word) + ".wav")
