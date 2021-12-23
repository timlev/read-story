import urllib
import urllib.parse
import urllib.request
import os
import tempfile
import platform
import bs4

def check_downloaded_word(word, directory="./"):
    """Check if word is already in directory in any format.
    Returns oggpath
    Return 1 if you have trouble searching.
    Return 2 if you can't download wiktionary page or ogg file."""
    soundfiles = os.listdir(directory)
    #strip extension
    downloaded_words = [os.path.splitext(x)[0] for x in soundfiles]
    if word in downloaded_words:
        return True
    else:
        return False

def get_wiki(word, directory="./"):
    """Check if word is in directory and download word.ogg into directory"""
    if check_downloaded_word(word, directory):
        print(word + " already downloaded")
        return 0
    #search for wiktionary word
    base = "https://en.wiktionary.org/wiki/"
    query = base + urllib.parse.quote(word)
    print(query)
    try:
        response = urllib.request.urlopen(query)
        print(response)
    except:
        print("Couldn't find", word)
        return 1
    print("Processing response")
    index = bs4.BeautifulSoup(response,"html5lib")
    filenameguess = "File:en-us-" + word + ".ogg"
    #Jump to file wiktionary page
    query = base + filenameguess
    try:
        response = urllib.request.urlopen(query)
    except:
        print("HTTP error for " + query)
        return 2
    print(response)
    index = bs4.BeautifulSoup(response, "html5lib")
    links = index.find_all("a")
    oggsource = ""
    for link in links:
        href = str(link.get("href"))
        if "upload" in href and "n-us" in href and ".ogg" in href and word in href:
            oggsource = "https:" + href

    print("Downloading to: " + os.path.join(directory, word + ".ogg"))
    try:
        print("Getting ogg...")
        getogg = urllib.request.urlopen(oggsource)
        print("Saving file ...")
        ofp = open(os.path.join(directory, word + ".ogg"),'wb')
        print("Writing file ...")
        ofp.write(getogg.read())
        ofp.close()
        return os.path.join(directory, word + ".ogg")
    except:
        #print("Could not download:", word)
        return 2


#convert ogg to mp3

def convert_ogg_to_mp3(oggfile, remove_ogg = False):
    oggpath = os.path.abspath(oggfile)
    ogg_dir = os.path.dirname(oggfile)
    oggfile = os.path.basename(oggfile)
    mp3file = oggfile.replace(".ogg", ".mp3")
    mp3path = oggpath.replace(".ogg",".mp3")
    if os.path.exists(oggpath):
        os.system('ffmpeg -i "' + oggpath + '" -acodec libmp3lame "' + mp3path + '"')
        if remove_ogg:
            os.remove(oggpath)
        return mp3path
    else:
        print("************\n Problem with " + word + "\n******************\n")
    

if __name__ == "__main__":
    wordlist = ["musician"]
    print(len(wordlist))
    missing_words = []
    for word in wordlist:
        get_wiki(word)
        convert_ogg_to_mp3(word + ".ogg", True)
    print("Missing Words: {}".format(missing_words))
