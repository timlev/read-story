import urllib
import urllib.parse
import urllib.request
import os
import tempfile
import platform
import bs4

def check_downloaded_word(word, directory="./"):
    soundfiles = os.listdir(directory)
    #strip extension
    downloaded_words = [os.path.splitext(x)[0] for x in soundfiles]
    if word in downloaded_words:
        return True
    else:
        return False

def get_wiki(word, directory="./"):
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
    #print(index.find(title=filenameguess))
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

    # oggsource = ""
    # for line in response:
        # if "src" in line and "n-us" in line and ".ogg" in line:
            # print(line)
            # start = line.find("""src="//""") + len("""src="//""")
            # end = line.find(".ogg") + len(".ogg")
            # oggsource = line[start:end]
            # oggsource = "https://" + oggsource
            # print(oggsource)
            # break
    # print(query)
    # print(oggsource)
    # print("Downloading to:", os.path.join(directory, word + ".ogg"))
    # try:
        # print("Getting ogg...")
        # getogg = urllib.urlopen(oggsource)
        # print("Saving file ...")
        # ofp = open(os.path.join(directory, word + ".ogg"),'wb')
        # print("Writing file ...")
        # ofp.write(getogg.read())
        # ofp.close()
        # return os.path.join(directory, word + ".ogg")
    # except:
        # #print("Could not download:", word)
        # return 2

#download wiktionary ogg file

def download_gstatic(word, directory="./"):
    if check_downloaded_word(word, directory):
        return 0
    base = "https://ssl.gstatic.com/dictionary/static/sounds/de/0/"
    query = base + word + ".mp3"
    print(query)
    try:
        response = urllib.urlopen(query)
    except:
        print("Couldn't find", word)
        return 1
    try:
        print("Getting mp3...")
        getmp3 = urllib.urlopen(query)
        print("Saving file ...")
        ofp = open(os.path.join(directory, word + ".mp3"),'wb')
        print("Writing file ...")
        ofp.write(getmp3.read())
        ofp.close()
        return os.path.join(directory, word + ".mp3")
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
    os.system('ffmpeg -i "' + oggpath + '" -acodec libmp3lame "' + mp3path + '"')
    if remove_ogg:
        os.remove(oggpath)
    return mp3path

if __name__ == "__main__":
    #if get_wiki("joyful") == 0:
    #    convert_ogg_to_mp3("i'm" + ".ogg", True)
    #print(download_gstatic("blowhole"))
    #print(download_gstatic("myword"))
    #wordlist = ["zero", "ten", "twenty", "one", "eleven", "twenty-one", "two", "twelve", "twenty-two", "three", "thirteen", "twenty-three", "four", "fourteen", "twenty-four", "five", "fifteen", "twenty-five", "six", "sixteen", "twenty-six", "seven", "seventeen", "twenty-seven", "eight", "eighteen", "twenty-eight", "nine", "nineteen", "twenty-nine", "thirty", "forty", "seventy", "thirty-one", "fifty", "eighty", "thirty-two", "sixty", "ninety"]
    wordlist = ["musician"]
    print(len(wordlist))
    for word in wordlist:
        get_wiki(word)
        """try:
            convert_ogg_to_mp3(word + ".ogg", True)
        except:
            print("************\n Problem with " + word + "\n******************\n")
"""
