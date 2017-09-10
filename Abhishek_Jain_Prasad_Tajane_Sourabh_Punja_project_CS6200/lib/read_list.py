import os
import pickle

r_file = open("lucene_top_20.txt", "r")
data = r_file.read()
print data

data_list = data.split("####")

print data_list
data_list.remove("")
print data_list

doc_rank_dict = {}
i = 0
for line in data_list:
    i += 1
    doc_rank_dict[str(i)] = line.split("\n")
    doc_rank_dict[str(i)].remove("")
    doc_rank_dict[str(i)].remove("")

print doc_rank_dict

completeName = os.path.join("lucene_doc_rank_dict" + ".txt")
file1 = open(completeName, "wb")
pickle.dump(doc_rank_dict, file1)

print doc_rank_dict.__len__()