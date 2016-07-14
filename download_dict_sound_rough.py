import os, glob, urllib
import download_dict_sound


def dictionary_rough_search(word, directory="./newdownloads/"):
    #if check_downloaded_word(word, directory):
        #return
    base = "http://dictionary.cambridge.org/us/dictionary/american-english/"
    base2 = "http://dictionary.cambridge.org/us/dictionary/english/"
    qmid = "?q="
    #end = "#"
    end = ""
    query = base + word + qmid + word + end
    query2 = base2 + word
    #print query
    #print query2

    # print query2
    handler = urllib.urlopen(query2)
    response = handler.readlines()
    # print "Found alternate source at", query2
    mp3source = ""
    for line in response:
        if "sound audio_play_button pron-icon us" in line and ".mp3" in line:
            # print line
            start = line.find("data-src-mp3=") + len("data-src-mp3=") + 1
            end = line.find(".mp3") + len(".mp3")
            mp3source = line[start:end]
            print mp3source
            #Stop looking through lines
            break
    print "Downloading", word, "to:", os.path.join(directory, word + ".mp3")
    try:
        getmp3 = urllib.urlopen(mp3source)
        ofp = open(os.path.join(directory, word + ".mp3"),'wb')
        ofp.write(getmp3.read())
        ofp.close()
    except:
        print "Could not download:", word

def download(word, directory="./"):
    if check_downloaded_word(word, directory):
        return
    base = "http://dictionary.cambridge.org/us/dictionary/american-english/"
    qmid = "?q="
    #end = "#"
    end = ""
    query = base + word + qmid + word + end
    print query

    try:
        response = urllib2.urlopen(query)
    except:
        print "Couldn't find entry for", word
        return 1
    mp3source = ""
    for line in response:
        if "sound audio_play_button pron-icon us" in line and word + ".mp3" in line:
            #print line
            start = line.find("data-src-mp3=") + len("data-src-mp3=") + 1
            end = line.find(".mp3") + len(".mp3")
            mp3source = line[start:end]
            break
    print query
    print mp3source
    print "Downloading to:", os.path.join(directory, word + ".mp3")
    try:
        getmp3 = urllib2.urlopen(mp3source)
        ofp = open(os.path.join(directory, word + ".mp3"),'wb')
        ofp.write(getmp3.read())
        ofp.close()
    except:
        print "Could not download:", word

def download_wiktionary(word, directory="./newdownloads/"):
    base = "https://en.wiktionary.org/wiki/"
    query = base + word
    
    handler = urllib.urlopen(query)
    response = handler.readlines()
    oggsource = ""
    for line in response:
        if "src=" in line and "_us_" in line and ".ogg" in line:
            start = line.find("upload.wikimedia")
            end = line.find(".ogg") + len(".ogg")
            oggsource = "https://" + line[start:end]
            print oggsource
            break
    print "Downloading", word, "to:", os.path.join(directory, word + ".ogg")
    try:
        getogg = urllib.urlopen(oggsource)
        ofp = open(os.path.join(directory, word + ".ogg"),'wb')
        ofp.write(getogg.read())
        ofp.close()
    except:
        print "Could not download:", word

def convert_ogg_to_mp3(oggfile, remove_ogg = False):
    oggpath = os.path.abspath(oggfile)
    ogg_dir = os.path.dirname(oggfile)
    oggfile = os.path.basename(oggfile)
    mp3file = oggfile.replace(".ogg",".mp3")
    mp3path = oggpath.replace(".ogg",".mp3")
    os.system('avconv -i "' + oggpath + '" "' + mp3path + '"')
    if remove_ogg:
        os.remove(oggpath)
    return mp3path


if __name__ == "__main__":
    wordlist = ["looks","birds","sharks","tim","rebecca","monkeys","minnesota","penguins","says","joan","bats","names","jenn","goats","animals","teachers","thirtytwo","roseville","okay","students","seals"]
    
    for word in wordlist:
        download_wiktionary(word,"./sounds/")
        try:
            convert_ogg_to_mp3(os.path.join(os.path.relpath("./sounds/"), word + ".ogg"), remove_ogg = True)
        except:
            print "Could't convert", word
            
