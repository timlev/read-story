import csv


with open("HTML IMAGE MAP Calc.csv") as csvfile:
  itemreader = csv.reader(csvfile)
  for row in itemreader:
    item = row[4]
    coords = row[5]
    print '   <area shape="rect"'
    print '      id="' + item +'"'
    print '      coords = "' + coords +'"'
    print '      alt="' + item +'"'
    print '      target = "_self"'
    print '      onClick = "play(this)"'
    print '      />'
