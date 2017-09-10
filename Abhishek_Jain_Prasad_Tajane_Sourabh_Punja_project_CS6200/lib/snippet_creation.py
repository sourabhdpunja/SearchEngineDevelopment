from nltk.tokenize import sent_tokenize, word_tokenize
import nltk
from bs4 import BeautifulSoup
import os
import re
import operator
import pickle

f = open("queries.txt", "r+")
content = f.read()
soup = BeautifulSoup(content, 'html.parser')
querylist= []
for tag in soup(["docno"]):
  tag.extract()

queries = soup.select('doc')
i = 1
for query in queries:
    onequery=str(query.get_text().encode('utf-8'))
    parsedquery = re.sub('\s+', ' ', onequery).strip()
    parsedquery = parsedquery.replace('\r', '').rstrip().lstrip()
    parsedquery = re.sub(' +', ' ', parsedquery)
    querylist.append(parsedquery)
# print querylist
completeName = os.path.join("common_words")
with open(completeName, 'r') as f:
     commonwords = f.readlines()
        # print commonwords
commonwords = [v.replace("\n", "") for v in commonwords]
directory = os.path.normpath("cacm/")
snippitdict = {}
files = os.listdir("../cacm/")

for filename in files:
    f = open("../cacm/" + filename, 'r')
    soup = BeautifulSoup(f.read(), "html.parser")
    text = soup.find("pre").text
    sent = sent_tokenize(text)
    querynum = 1
    # for onesent in sent:
        # for
    for query in querylist:
        sentdict = {}
        for onesent in sent:
            snippitscore=0
            significancenum=0
            significantword=[]
            sentlength = float(len(onesent.split()))
            for onequeryterm in (str(query)).split():
                count = sum(1 for _ in re.finditer(r'\b%s\b' % re.escape(onequeryterm), onesent))
                if count>0 and onequeryterm not in commonwords:
                    onesent = str(onesent).replace(onequeryterm,"<b>"+str(onequeryterm)+"</b>")
                significancenum =  significancenum + count
            snippitscore = ((significancenum*significancenum)/sentlength)
            sentdict[onesent] = snippitscore
        sentdict = max(sentdict.iteritems(), key=operator.itemgetter(1))[0]
        docname = filename.replace('.html','').replace('CACM-','')

        sentdict = re.sub(r"^\d+\t\d+\t\d+$", " ", sentdict, flags=re.M)
        if querynum in snippitdict:
            snippitdict[querynum][docname] = str(sentdict)
        else:
            snippitdict[querynum] = {docname: str(sentdict)}
        querynum = querynum + 1


# completeName = os.path.join("C:\Users\Sourabh Punja\PycharmProjects\Project\documentrank",
#                                 "Document_Frequency_Table_Unigram" + ".txt")
# file1 = open(completeName, "w")
# file1.write("Unigram Inverted index in terms of Token, Doc ID and DocumentFrequency\n\n")
# file1.write("1-TOKEN --> DOC-ID : DOCUMENTFREQUENCY\n\n")
# for key, value in snippitdict.items():
#      file1.write(str(key) + " --> " + str(value) + "\n")
# file1.close()
with open('snippetCreationFile.pickle', 'wb') as handle:
  pickle.dump(snippitdict, handle, protocol=pickle.HIGHEST_PROTOCOL)
