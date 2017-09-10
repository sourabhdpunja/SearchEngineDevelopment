import os
import pickle
directory = "../results/BM25"
docrankdict={}
snippitdict={}
querynum = 0

for subdir, dirs, files in os.walk(directory):
  for file in files:
    listofdoc = []
    f = open(os.path.join(subdir, file), 'r')
    rankings = f.readlines()
    rankings = [x.strip() for x in rankings]
    for page in rankings:
        line = page.split()
        doc = line[2]
        querynum= line[0]
        listofdoc.append(str('%04d'%(int(doc))))

    # if querynum in docrankdict:
    listofdoc=listofdoc[0:10]
    docrankdict[querynum]= listofdoc
# print docrankdict
completeName = os.path.join("snippetCreationFile" + ".pickle")
with open(completeName, 'rb') as handle:
    snippitdict = pickle.load(handle)
# doc1query={}
# doc1query['1']=docrankdict['1']
        # rank = line[3]
# print snippitdict
# print docrankdict

for key,value in docrankdict.items():
    completeName = os.path.join("../results/SnippitResults", str("result_"+key+".txt"))
    target = open(completeName, "w")
    i = 0

    target.write("Query:" + key +"\n")
    for docfile in value:
        i += 1
        target.write("Document number:" + docfile+"\n")
        target.write("Rank:" + str(i) +"\n")
        #print (value)
        target.write(str(snippitdict[int(key)][docfile]).strip()+"\n\n\n\n\n\n")
        # print (snippitdict[int(key)][docfile])
target.close()

