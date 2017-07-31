# read-story
Read Text Out Loud

Read-Story is a command line program takes the text from an html document, downloads sound files for each word, and creates a clickable html file that plays the pronunciation of each word that is clicked.

The purpose of this app is to support students learning to read in English.

Requires:
python2.7
python-html5
ffmpeg or avconv (libav-tools)
LibreOffice (for best results)
SoX (optional, for using record_missing_words.py)

Steps:
1. Export document as html from LibreOffice to html_input
2. Type command to create clickable html file in html_output/new_NAMEOFFILE.html:
  python parse_html.py html_input/NAMEOFFILE.html
3. Record missing sounds as mp3 files in sounds/
  a. Words are listed under missing_words/NAMEOFFILE.html_missing_words.txt
  b. Recordings can be made using command:
      python record_missing_words.py missing_words/NAMEOFFILE.html_missing_words.txt
  c. Hit Ctrl-C after saying each word to stop recording
4. Open html_output/new_NAMEOFFILE.html in preferred web browser. 
