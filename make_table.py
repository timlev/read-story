import csv, os, download_dict_sound, sys

datafile = ""


if len(sys.argv) > 1:
    datafile = sys.argv[1]
else:
    datafile = "5th grade academic vocabulary.csv"

rawdata = []
if datafile.endswith(".txt"):
    with open(datafile, "r") as fp:
        rawdata = fp.readlines()

csvfilename = datafile
title = csvfilename[:csvfilename.rfind(".")]
htmlfilename = title + ".html"

if os.path.isdir(title) == False:
    os.mkdir(title)

#GET WORDS
data = []
with open(csvfilename, "r") as csvfile:
    csvreader = csv.reader(csvfile)
    for row in csvreader:
        data.append(row)

#Form HTML BLOB
htmlblob = """<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
	"http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">

<head>
	<title>""" + title + """</title>
	<meta http-equiv="content-type" content="text/html;charset=utf-8" />
	<meta name="generator" content="Geany 1.23.1" />
	<link rel="stylesheet" type="text/css" href='../css_file.css'>
	<script>
		function revert_color(obj){
			setTimeout(function (){document.getElementById(obj.id).style.backgroundColor = 'transparent';},1000);
		};
		function play(sndobj){
			txtobjId = sndobj.id + "_text";
			txtobj = document.getElementById(txtobjId);
			document.getElementById(txtobj.id).style.backgroundColor = 'yellow';
			document.getElementById(sndobj.id).play();
			document.getElementById(sndobj.id).addEventListener( "ended", revert_color(txtobj));
		};
	</script>
</head>

<body>
<div><img align="left" src="../click.png" width="75" height="75"></img><h2>Click to listen to the words.</h2></div>
<div>"""

htmlblob += "<table border=1>\n"
for row in data:
    htmlblob += "<tr>\n"
    for item in [x for x in row if x != ""]:
		htmlblob += "<td>\n"
		htmlblob += """\t<audio src='""" + item + """.mp3' id='"""+ item + """'> \n"""
		htmlblob += """\t</audio>\n"""
		htmlblob += """\t<div id='""" + item + """_text' onClick="play(document.getElementById('""" + item + """'));">""" + item + """</div>\n"""
		htmlblob += "</td>\n"
    htmlblob += "</tr>\n"

htmlblob += "</table>\n"
htmlblob += """</div>
</body>

</html>"""
with open(os.path.join(title, htmlfilename), "w") as htmlfile:
    htmlfile.write(htmlblob)

#MAKE LIST OF WORDS TO DOWNLOAD
toDownload = []
for row in data:
    for item in [x for x in row if x != ""]:
        toDownload.append(item)

#DOWNLOAD WORDS
not_downloaded = []

for word in toDownload:
    #print word
    if download_dict_sound.download(word, os.path.relpath(title)) != 0:
        not_downloaded.append(word)
print "Not downloaded:\n"
print not_downloaded

#WRITE FILE WITH LIST OF NOT DOWNLOADED
with open(os.path.join(title, "not_downloaded.txt"),"w") as fp:
    fp.write("\n".join(not_downloaded))
