import os
import glob
import pickle

path = "/Users/prasadtajane/PycharmProjects/untitled/final/results/Lucene/"
file_name = "1.txt"
write_file = "lucene_top_20.txt"

for name in glob.glob(path + "*"):
    print name

    r_file = open(name) #(path + file_name)
    data = r_file.read()
    r_file.close()
    #print data

    list_data = data.split("\n")
    list_data.remove("")
    #print list_data

    w_file = open(write_file, "a")
    w_file.write("####\n")

    counter = 0
    for each_val in list_data:
        counter += 1
        doc_name = each_val.split("    ")[2]
        print doc_name
        w_file.write(doc_name)
        w_file.write("\n")
        if counter == 20:
            break

    print (counter)

w_file.close()
#cName = os.path.join("lucene_doc_rank_dict" + ".txt")
#with open(cName, 'rb') as handle:
#    lucene_doc_rank_dict = pickle.load(handle)
#
#print lucene_doc_rank_dict

