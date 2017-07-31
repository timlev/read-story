import string
filename = """The Animals at the Minnesota Zoo.html"""
contents = ""

with open(filename, "rb") as fp:
  contents = fp.read()

 
#print contents

def findbody():
  start = contents.index("<body")
  end = contents.rindex("</body")
  return contents[start:end]

#print findbody()[0:100]


def removeTags():
  body = findbody()
  beginningtags = []
  endingtags = []
  for pos, c in enumerate(body):
    if c == "<":
      beginningtags.append(pos)
    elif c == ">":
      endingtags.append(pos)
  pairs = zip(beginningtags, endingtags)
  backwardpairs = pairs[::-1]
  bodylist = list(body)
  for pair in backwardpairs:
    #body = body.replace(body[pair[0]:pair[1]],"")
    bodylist[pair[0]:pair[1] + 1] = []
  #bodylist = [x for x in bodylist if x != "\n"]
  body = "".join(bodylist)
  body = body.replace("\n", " ")
  body = body.split(' ')
  body = [x for x in body if x != " " and x != ""]
  return body

#print removeTags()

def tokenizeWords(wordset):
  #clean words
  tokenized = []
  for word in wordset:
    tokenized.append("".join([x for x in list(word) if x in string.ascii_letters]).lower())
  translated = zip(wordset, tokenized)
  translated = [(x, y) for (x, y) in translated if y != ""]
  return translated

def is_ascii(s):
  try:
    s.decode('ascii')
    return True
  except UnicodeDecodeError:
    return False

#print tokenizeWords(removeTags())

original_body = findbody()
translated = tokenizeWords(removeTags())

cursor = 0

def addSpan(pos, word, token, so, eo):
  global cursor
  global original_body
  #add beginning
  beg = "<span id='"
  beg += str(pos)
  beg += "_" + token + "'"
  beg += """ class='sp' onclick='play(this)'>"""
  end = "</span>"
  span = beg + word + end
  cursor += len(span)
  original_body = original_body[:so] + span +  original_body[eo:]
  print span


def findfirstaftercursor(pos, word, token):
  global cursor
  search_area = original_body[cursor:]
  s = search_area.index(word)
  e = s + len(word)
  so = s + cursor
  eo = e + cursor
  #cursor = eo
  addSpan(pos, word, token, so, eo)
  print pos, cursor, search_area[s:e], original_body[so:eo]

"""    while cursor < len(original_body):
      if orginal_body[cursor : cursor + len(word)] == word:
        return word, cursor
      else:
        cursor += 1
"""

for pos, word in enumerate(translated):
  findfirstaftercursor(pos, word[0], word[1])
print original_body

newfile = "new_" + filename

header = "<head> <style> span {color : yellow;}</style></head>"
original_body = header + original_body
with open(newfile, "wb") as wb:
  wb.write(original_body)
