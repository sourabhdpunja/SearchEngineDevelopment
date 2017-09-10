from math import log
import os
import pickle

INVERTED_LIST_FILE = os.path.join("Index" + ".pickle")
DOCUMENT_LENGTH = os.path.join("DocLength" + ".pickle")
QUERY_FILE = os.path.join("QueryParsed" + ".pickle")
RESULT_DIRECTORY = "../results/tf-idf/results_"


class VectorSpace(object):
  N = 3204

  def __init__(self):
    self.query = ""
    self.inverted_list = {}
    self.doc_length = {}
    self.doc_frequency = {}
    self.query_term_dict = {}
    self.generate_doc_frequency()

  def generate_inverted_list(self):
    with open(INVERTED_LIST_FILE, 'rb') as handle:
      self.inverted_list = pickle.load(handle)
    # f = open("inverted_list.txt", "r+")
    # inverted_list = f.readlines()
    # inverted_list = [x.strip() for x in inverted_list]

    # for il in inverted_list:
    #   line = il.split(" || ")
    #   doc_freq = line[1].split(", ")
    #   dictionary = {}
    #   for doc in doc_freq:
    #     docf = doc.split(":")
    #     key = docf[0]
    #     value = docf[1]
    #     dictionary[key] = int(value)
    #   self.inverted_list[line[0]] = dictionary
    # with open('UnipickleFile.txt', 'wb') as handle:
    #     pickle.dump(self.inverted_list, handle, protocol=pickle.HIGHEST_PROTOCOL)

  def generate_doc_length(self):
    with open(DOCUMENT_LENGTH, 'rb') as handle:
      self.doc_length = pickle.load(handle)

    # f = open("document_length.txt", "r+")
    # doc_length = f.readlines()
    # doc_length = [x.strip() for x in doc_length]

    # for doc in doc_length:
    #   doc = doc.split()
    #   self.doc_length[doc[0]] = int(doc[1])
    # with open('DocpickleFile.txt', 'wb') as handle:
    #     pickle.dump(self.doc_lines, handle, protocol=pickle.HIGHEST_PROTOCOL)


  def generate_doc_frequency(self):
    self.generate_doc_length()
    self.generate_inverted_list()
    # completeName = os.path.join("DocpickleFile" + ".pickle")

    # with open(completeName, 'rb') as handle:
    #     self.doc_length = pickle.load(handle)
    #     # print b

    # completeName = os.path.join("UnipickleFile" + ".pickle")

    # with open(completeName, 'rb') as handle:
    #     self.inverted_list = pickle.load(handle)



    with open(QUERY_FILE, 'rb') as handle:
      self.query_term_dict = pickle.load(handle)


  def process(self):
    for query_id in self.query_term_dict.keys():
      query_array = self.query_term_dict[query_id]
      ranking = {}
      print(query_array)
      for term in query_array.split():
        if term in self.inverted_list.keys():
          for doc in self.inverted_list[term].keys():
            if doc in ranking.keys():
              ranking[doc] += self.tf(term, doc)*self.idf(term)
            else:
              ranking[doc] = self.tf(term, doc)*self.idf(term)

      # for doc in self.doc_length.keys():
      #   tf_idf = 0
      #   print(doc)
      #   for term in query_array:
      #     tf_idf += self.tf(term, doc)*self.idf(term)
      #   ranking[doc] = tf_idf
      self.add_rank_scores_to_file(query_id, ranking)

  def add_rank_scores_to_file(self, query_id, ranking):
    f = open(RESULT_DIRECTORY + str(query_id) + ".txt", "w+")
    sorted_rankings = sorted(ranking, key=ranking.get, reverse=True)
    i = 0
    while(i < 100):
      term = sorted_rankings[i]
      doc = term.split("-")[-1]
      f.write(str(query_id) + " Q0 " + str(doc) + " " + str(i+1) + " " + str(ranking[term]) + " Abhishek ")
      f.write("\n")
      i += 1
    # for doc in sorted_rankings:
    #   f.write(doc)
    #   f.write(" : ")
    #   f.write(str(ranking[doc]))
    #   f.write("\n")
    f.close()

  def idf(self, term):
    nk = 1 #Starting with 1 instead of zero for having non-zero number in division
    if term in self.inverted_list.keys():
      nk = (len(self.inverted_list[term].keys()))
    return log(VectorSpace.N/nk, 10)

  def tf(self, term, doc_id):
    total_number_of_terms = float(self.doc_length[doc_id])
    frequency_of_term = 0
    if term in self.inverted_list.keys():
      inverted_list = self.inverted_list[term]
      if doc_id in inverted_list.keys():
        frequency_of_term = float(inverted_list[doc_id])
    return frequency_of_term/total_number_of_terms


v = VectorSpace()
v.process() 
