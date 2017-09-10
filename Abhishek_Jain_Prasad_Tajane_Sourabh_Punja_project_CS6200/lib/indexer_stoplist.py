import os
import sys
import pickle

class Indexer(object):
  DIRECTORY_NAME = "tokenized"

  def __init__(self, n):
    self.files = os.listdir(Indexer.DIRECTORY_NAME)
    self.index = {}
    self.term_freqeuncy = {}
    self.n = n
    self.dl = {}
    self.commonwords = []
    self.generate_stoplist()

  def generate_stoplist(self):
    f = open("common_words", "r+")
    commonwords = f.readlines()
    self.commonwords = [v.replace("\n","") for v in commonwords]

  def process(self):
    for file_name in self.files:
      f = open(Indexer.DIRECTORY_NAME + "/" + file_name, "r+")
      extension = os.path.splitext(file_name)[1]
      if extension == ".txt":
        content = f.read()

        file_name = file_name.replace(".txt", "")
        words = content.split()

        words = [x for x in words if x not in self.commonwords]

        self.dl[file_name] = len(words)

        counts = self.word_count(words)
        for word in counts.keys():
          if word in self.index.keys():
            self.index[word][file_name] = counts[word]
          else:
            self.index[word] = {file_name: counts[word]}

    self.generate_index()

    # self.generate_term_frequency_table()
    self.document_length()
    # self.generate_doc_frequency_table()

  def generate_term_frequency_table(self):
    for term in self.index.keys():
      self.term_freqeuncy[term] = sum(self.index[term].values())

    sorted_terms = sorted(self.term_freqeuncy, key=self.term_freqeuncy.get, reverse=True)

    f = open("term_frequency_" + str(self.n) + ".txt", "w+")

    for term in sorted_terms:
      f.write(str(term) + " || " + str(self.term_freqeuncy[term]))
      f.write("\n")
    f.close()

  def generate_index(self):
    with open('IndexStopped.pickle', 'wb') as handle:
      pickle.dump(self.index, handle, protocol=pickle.HIGHEST_PROTOCOL)
    # f = open("inverted_list_stoplist.txt", "w+")
    # for term in self.index.keys():
    #   f.write(term + " || " + self.parse(self.index[term]))
    #   f.write("\n")
    # f.close()

  def document_length(self):
    with open('DocLengthStopped.pickle', 'wb') as handle:
      pickle.dump(self.dl, handle, protocol=pickle.HIGHEST_PROTOCOL)
    # f = open("document_length_stoplist.txt", "w+")
    # for docID in self.dl.keys():
    #   f.write(docID + " " + str(self.dl[docID]))
    #   f.write("\n")
    # f.close

  def parse(self, inverted_list):
    string = []
    for doc in inverted_list.keys():
      string.append(doc + ":" + str(inverted_list[doc]))
    return ", ".join(string)



  def generate_doc_frequency_table(self):
    f = open("document_frequency_for_" + str(self.n) + ".txt", "w+")
    keys = sorted(self.index.keys())

    for term in keys:
      df = (len(self.index[term].keys()))
      f.write(term + "      ")
      f.write("  ||  ")
      f.write(", ".join(self.index[term].keys()).rjust(10))
      f.write("  ||  ")
      f.write(str(df).rjust(10))
      f.write("\n")

    f.close()

  def word_count(self, words):
    counts = {}

    for index, word in enumerate(words):
      total = words[index:(index+self.n)]
      token = ' '.join(str(x) for x in total)
      if token in counts: 
        counts[token] += 1
      else:
        counts[token] = 1

    return counts


n = sys.argv[1]
i = Indexer(int(n))
i.process()
