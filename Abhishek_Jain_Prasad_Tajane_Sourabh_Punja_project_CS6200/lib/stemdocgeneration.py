import re
import os
import operator
import urllib
from collections import Counter
import collections
from itertools import islice, izip
import pickle
import sys

def main(argv):
    uniinverteddict={}
    docfile={}
    directory = os.path.normpath(argv)
    with open(directory, 'r') as f:
        text = f.read()
        text=re.sub(r"^\d+\t\d+\t\d+$", " ", text, flags=re.M)
        # print text
        textlist = text.split('#')
        # filedict = Counter(textlist)
        # print textlist
        for eachtext in textlist:
            if eachtext != "":
                if eachtext.rfind("pm") != -1:
                    k = eachtext.rfind("pm")
                elif eachtext.rfind("am") != -1:
                    k = eachtext.rfind("am")
                filenum= re.search(r'\d+', eachtext).group()
                eachtext = eachtext.replace(filenum, "", 1)
                eachtext = eachtext[2:k+2]
                filedict = Counter(eachtext.split())
                docfile[filenum] = sum(filedict.values())
                completeName = os.path.join("C:\Users\Sourabh Punja\PycharmProjects\Project\ParsedDocuments", "CACM-"+str('%04d'%(int(filenum)))+".html")
                if os.path.isfile(completeName):
                    completeName = os.path.join("C:\Users\Sourabh Punja\PycharmProjects\Project\ParsedDocuments",
                                                file + "1"+".html")
                target = open(completeName, "w")
                target.write(eachtext)
                # f.close()
                for key, value in filedict.items():
                    if key in uniinverteddict:
                        uniinverteddict[key][filenum] = str(value)
                    else:
                        uniinverteddict[key] = {filenum: str(value)}
        uniinverteddict = collections.OrderedDict(sorted(uniinverteddict.items()))
        print  uniinverteddict

        with open('C:\Users\Sourabh Punja\PycharmProjects\Project\PickleFile\UniquerypickleFile.pickle', 'wb') as handle:
            pickle.dump(uniinverteddict, handle, protocol=pickle.HIGHEST_PROTOCOL)
        with open('C:\Users\Sourabh Punja\PycharmProjects\Project\PickleFile\DocquerypickleFile.pickle', 'wb') as handle:
            pickle.dump(docfile, handle, protocol=pickle.HIGHEST_PROTOCOL)

if __name__ == "__main__":
   # main(sys.argv[1:])
   main("C:\Users\Sourabh Punja\PycharmProjects\Project\Index\cacm_stem.txt")