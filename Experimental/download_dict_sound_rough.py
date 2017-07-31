import os, glob, urllib
import download_dict_sound

unable_to_download = []

def dictionary_rough_search(word, directory="./sounds/"):
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
        #print line
        if ".mp3" in line and "American" in line:
        #if 'title="' + word + ':' in line and ".mp3" in line and "American" in line:
        #if "sound audio_play_button pron-icon us" in line and ".mp3" in line:
            print line
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
        unable_to_download.append(word)

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

