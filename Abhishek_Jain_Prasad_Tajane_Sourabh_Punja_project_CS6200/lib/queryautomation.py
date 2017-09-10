from struct import pack

from bs4 import BeautifulSoup
import re
import string
import pickle
import os

def extract_queries(bool):
  f = open("C:\Users\Sourabh Punja\PycharmProjects\Project\PickleFile\queries.txt", "r+")
  content = f.read()
  soup = BeautifulSoup(content, 'html.parser')

  for tag in soup(["docno"]):
    tag.extract()

  queries = soup.select('doc')

  query_dict = {}
  i = 1
  for query in queries:
    onequery=str(query.get_text().encode('utf-8'))
    print onequery
    parsedquery = re.sub('\s+', ' ', onequery).strip()
    parsedquery = parse_text(parsedquery)
    parsedquery = parsedquery.replace('\r', '').rstrip().lstrip()
    parsedquery = re.sub(' +', ' ', parsedquery)
    if bool:
        completeName = os.path.join("C:\Users\Sourabh Punja\PycharmProjects\Project",
                                    "common_words")
        with open(completeName, 'r') as f:
            commonwords = f.readlines()
        # print commonwords
        commonwords = [v.replace("\n", "") for v in commonwords]
        for stopword in commonwords:
         if str(" "+stopword+" ") in parsedquery:
            parsedquery = parsedquery.replace(str(" "+stopword+" "), " ")
           # newqueries.append(value)
    #        # print newqueries
    query_dict[i] = parsedquery
    # queries.append(result.replace('\r', '').replace('\n', '').rstrip().lstrip())
    # query_dict[i]
    i += 1
  return query_dict

def parse_text(text):
    words = []
    for word in text.split():
      if not hasNumbers(word):
        for c in string.punctuation.replace("-", "").replace("'",""):
          word = word.replace(c, " ")
      words.append(word.lower())

    return " ".join(words)

def hasNumbers(inputString):
  return bool(re.search(r'\d', inputString))


query_dict = {}
query_dict = extract_queries(False)
with open('C:\Users\Sourabh Punja\PycharmProjects\Project\PickleFile\QueryParsed.pickle', 'wb') as handle:
    pickle.dump(query_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)
print query_dict
completeName = os.path.join("C:\Users\Sourabh Punja\PycharmProjects\Project\documentrank",
                                "queries" + ".txt")
file1 = open(completeName, "w")
file1.write("QUERIES\n\n")
    # file1.write("1-TOKEN --> DOC-ID : DOCUMENTFREQUENCY\n\n")
for key in query_dict.values():
  file1.write(str(key) + "\n")
file1.close()