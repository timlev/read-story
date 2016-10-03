import os, string

directory = os.path.abspath("/home/levtim/Dropbox/Apps/Hi-Q Recordings")
#directory = os.path.abspath("sounds")

for f in os.listdir(directory):
    if f[0] in string.ascii_uppercase:
        nf = f[0].lower() + f[1:]
        #print nf
        os.rename(os.path.join(directory, f),os.path.join(directory,nf))

#print string.ascii_uppercase
