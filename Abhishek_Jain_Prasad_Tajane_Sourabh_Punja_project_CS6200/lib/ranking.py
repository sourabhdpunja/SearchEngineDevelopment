from math import log
import collections
import pickle
import os

INVERTED_LIST_FILE = os.path.join("Index" + ".pickle")
DOCUMENT_LENGTH = os.path.join("DocLength" + ".pickle")
DOC_RANK = 'doc_rank_dict.txt'
RESULTS_DIRECTORY = "../results/BM25/results_"
QUERY_FILE = os.path.join("QueryParsed" + ".pickle")


# INVERTED_LIST_FILE = os.path.join("Index" + ".pickle")
# DOCUMENT_LENGTH = os.path.join("DocLength" + ".pickle")
# DOC_RANK = 'doc_rank_dict.txt'
# RESULTS_DIRECTORY = "../results/BM25_feedback/results_"
# QUERY_FILE = os.path.join("new_query_dict_2" + ".txt")

class Ranking(object):
  N = 3204
  K1 = 1.2
  K2 = 300
  B = 0.75

  def __init__(self):
    self.query = ""
    self.doc_lines = {}
    self.inverted_list = {}
    self.scores = {}
    self.ordered = {}
    self.relevant_docs = {}
    self.generate_inverted_list()
    self.generate_doc_length()
    self.add_relevant_docs()

  def add_relevant_docs(self):
    f = open("../results/cacm.rel")
    documents = f.readlines()
    documents = [x.strip() for x in documents]
    for line in documents:
      line = line.split()
      query = str(line[0])
      doc = line[2].split("-")[-1]
      if query in self.relevant_docs.keys():
        self.relevant_docs[query].append(doc)
      else:
        self.relevant_docs[query] = [doc]

  def generate_inverted_list(self):
    with open(INVERTED_LIST_FILE, 'rb') as handle:
      self.inverted_list = pickle.load(handle)

  def generate_doc_length(self):
    with open(DOCUMENT_LENGTH, 'rb') as handle:
      self.doc_lines = pickle.load(handle)


  def process(self, query, query_id):
    R = 0
    self.relevant_docs_for_query = []
    self.query = query
    queries = self.query.split()
    if query_id in self.relevant_docs.keys():
      R = len(self.relevant_docs[query_id])
      self.relevant_docs_for_query = self.relevant_docs[query_id]

    for token in queries:
      ri = 0
      qi = queries.count(token)
      if(token in self.inverted_list.keys()):
        ni = len(self.inverted_list[token].keys())
        for doc in self.relevant_docs_for_query:
          if doc in self.inverted_list[token].keys():
            ri += 1
      else:
        continue

      docs = self.inverted_list[token].keys()
      for doc in docs:
        fi = int(self.inverted_list[token][doc])
        K = Ranking.K1*((1-Ranking.B) + Ranking.B*((self.doc_lines[doc])/self.avdl()))
        if doc not in self.scores.keys():
          self.scores[doc] = self.calculate_score(K, ni, Ranking.N, fi, qi, Ranking.K1, Ranking.K2, doc, R, ri)
        else:
          self.scores[doc] += self.calculate_score(K, ni, Ranking.N, fi, qi, Ranking.K1, Ranking.K2, doc, R, ri)


    self.generate_file_for_scores(query_id)


  def calculate_score(self, K, ni, N, fi, qi, k1, k2, doc, r, ri):
    log_value = log(self.score(ni, r, ri), 10)
    first = ((k1+1)*fi)/(K+fi)
    second = float((k2+1)*qi)/(k2+qi)
    return log_value*first*second

  def score(self, ni, r, ri):
    N = Ranking.N
    return ((ri + 0.5)/(r-ri+0.5))/((ni-ri + 0.5)/(N-ni-r+ri+0.5))


  def avdl(self):
    return sum(self.doc_lines.values())/Ranking.N

  def create_doc_rank_pickle(self):
    with open(DOC_RANK, 'wb') as handle:
      pickle.dump(self.ordered, handle, protocol=pickle.HIGHEST_PROTOCOL)


  def generate_file_for_scores(self, query_id):
    f = open(RESULTS_DIRECTORY + query_id + ".txt", "w+")
    self.ordered[query_id] = []
    sorted_terms = sorted(self.scores, key=self.scores.get, reverse=True)

    i = 0
    while(i < 100):
      term = sorted_terms[i]
      doc = term.split("-")[-1]
      f.write(query_id + " Q0 " + doc + " " + str(i+1) + " " + str(self.scores[term]) + " Abhishek ")
      f.write("\n")
      i += 1

    i = 0
    while(i < 20):
      self.ordered[query_id].append(sorted_terms[i])
      i += 1

    f.close()


r = Ranking()

queries = {}

with open(QUERY_FILE, 'rb') as handle:
  queries = pickle.load(handle)
for query_id in queries:
  r.process(queries[query_id], str(query_id))

r.create_doc_rank_pickle()
