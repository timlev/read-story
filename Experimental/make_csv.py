import csv, itertools

txtfilename = "5th grade academic vocabulary.txt"
csvfilename = txtfilename[:txtfilename.rindex(".")] + ".csv"
rawdata = []

with open(txtfilename, "r") as csvfile:
    csvreader = csv.reader(csvfile)
    for row in csvreader:
        rawdata.append(row)

#Flatten list
rawdata = [x[0].rstrip() for x in rawdata]
rawdata = list(set(rawdata))
rawdata.sort()

output_list = []
full_cols = len(rawdata) / 27
remainder_rows = len(rawdata) % 27
print len(rawdata[0:27])
cursor = 0
for col in range(1,full_cols + 1):
    output_list.append(rawdata[cursor: col * 27])
    cursor = col * 27
output_list.append(rawdata[cursor:])

output_list = itertools.izip_longest(*output_list)

with open(csvfilename, "wb") as csvfile:
    csvwriter = csv.writer(csvfile)
    for row in output_list:
        csvwriter.writerow(row)
