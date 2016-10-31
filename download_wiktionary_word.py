import urllib2
import os
import tempfile
import platform
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
        return 0
#search for wiktionary word
    base = "http://en.wiktionary.org/wiki/"
    query = base + word
    print query
    try:
        response = urllib2.urlopen(query)
    except:
        print "Couldn't find", word
        return 1
    oggsource = ""
    for line in response:
        if "src" in line and "n-us" in line and ".ogg" in line:
            print line
            start = line.find("""src="//""") + len("""src="//""")
            end = line.find(".ogg") + len(".ogg")
            oggsource = line[start:end]
            oggsource = "https://" + oggsource
            print oggsource
            break
    print query
    print oggsource
    print "Downloading to:", os.path.join(directory, word + ".ogg")
    try:
        print "Getting ogg..."
        getogg = urllib2.urlopen(oggsource)
        print "Saving file ..."
        ofp = open(os.path.join(directory, word + ".ogg"),'wb')
        print "Writing file ..."
        ofp.write(getogg.read())
        ofp.close()
        return os.path.join(directory, word + ".ogg")
    except:
        print "Could not download:", word
        return 2
"""

#download wiktionary ogg file


"""
#convert ogg to mp3

def convert_ogg_to_mp3(oggfile, remove_ogg = False):
    oggpath = os.path.abspath(oggfile)
    ogg_dir = os.path.dirname(oggfile)
    oggfile = os.path.basename(oggfile)
    mp3file = oggfile.replace(".ogg", ".mp3")
    mp3path = oggpath.replace(".ogg",".mp3")
    if platform.system() == 'Linux':
        os.system('avconv -i "' + oggpath + '" "' + mp3path + '"')
    if remove_ogg:
        os.remove(oggpath)
    return mp3path
    
if __name__ == "__main__":
    if get_wiki("joyful") == 0:
        convert_ogg_to_mp3("i'm" + ".ogg", True)
    print "https://upload.wikimedia.org/wikipedia/commons/b/b9/En-us-I%27m.ogg" == "https://upload.wikimedia.org/wikipedia/commons/b/b9/En-us-I%27m.ogg"
