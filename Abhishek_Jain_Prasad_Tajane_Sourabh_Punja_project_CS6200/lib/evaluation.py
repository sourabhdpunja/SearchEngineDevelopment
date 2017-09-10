import pickle
import os
import collections
import sys

class Evaluation(object):
  def __init__(self):
    self.relevant_docs = collections.OrderedDict()
    self.add_relevant_docs()


  def add_relevant_docs(self):
    f = open("../results/cacm.rel")
    documents = f.readlines()
    documents = [x.strip() for x in documents]
    for line in documents:
      line = line.split()
      query = int(line[0])
      doc = int(line[2].split("-")[-1])
      if query in self.relevant_docs.keys():
        self.relevant_docs[query].append(doc)
      else:
        self.relevant_docs[query] = [doc]

  def process_and_result(self, algo):
    self.evaluation_scores = collections.OrderedDict()
    queries = collections.OrderedDict()
    average_precision = collections.OrderedDict()

    completeName = os.path.join("QueryParsed" + ".pickle")
    with open(completeName, 'rb') as handle:
      queries = pickle.load(handle)

    i = 0
    mean_avg_precison_sum = 0
    r_rank_sum = 0

    for query_id in queries.keys():
      query_id = int(query_id)
      if query_id in self.relevant_docs.keys():
        i += 1
        self.process(algo, query_id)
        average_precision[query_id] = self.average_precision(query_id)
        mean_avg_precison_sum += average_precision[query_id]
        r_rank_sum += self.reciprocal_rank(query_id)

    mean_avg_precison = mean_avg_precison_sum/i
    mrr = r_rank_sum/i

    self.add_average_precision_to_file(average_precision, algo)

    self.result_to_file(self.evaluation_scores, algo, mean_avg_precison, mrr)

  def add_average_precision_to_file(self, avg_precision, algo):
    with open(algo + "_avg_precisions.pickle", 'wb') as handle:
      pickle.dump(avg_precision, handle, protocol=pickle.HIGHEST_PROTOCOL)

  def reciprocal_rank(self, query_id):
    precision = self.evaluation_scores[query_id]
    for rank in precision.keys():
      if precision[rank]["relevant"]:
        return 1.0/int(rank)
    return 0

  def average_precision(self, query_id):
    precision = self.evaluation_scores[query_id]
    summation = 0
    i = 0
    for rank in precision.keys():
      if precision[rank]["relevant"]:
        i += 1
        summation += precision[rank]["score"]
    return summation/float(i) if (i > 0) else 0

  def process(self, algo, query_id):
    relevant_docs = self.relevant_docs[query_id]
    result_set = "../results/" + algo + "/" + "results_" + str(query_id) + ".txt"
    # result_set = "../results/" + algo + "/" + str(query_id) + ".txt"
    f = open(result_set, "r+")
    rankings = f.readlines()
    rankings = [x.strip() for x in rankings]

    number_of_relevant_docs = 0
    total_relevant_docs = len(relevant_docs)

    precision = collections.OrderedDict()

    for page in rankings:
      line = page.split()
      doc = line[2]
      rank = line[3]
      relevant = False

      if int(doc) in relevant_docs:
        relevant = True
        number_of_relevant_docs += 1

      recall = float(number_of_relevant_docs)/total_relevant_docs
      precision_value = float(number_of_relevant_docs)/int(rank)
      precision[rank] = {"score": precision_value, "relevant": relevant, "recall": recall}


    self.evaluation_scores[query_id] = precision


  def result_to_file(self, precision, algo, mean_avg_precison, mrr):
    f = open("../results/" + algo + "_evaluation.txt", "w+")

    f.write("Mean Average Precision:  ")
    f.write(str(mean_avg_precison))
    f.write("\n\n\n")

    f.write("Mean Reciprocal Rank:   ")
    f.write(str(mrr))
    f.write("\n\n\n")

    sorted_terms = sorted(self.evaluation_scores)

    for query_id in sorted_terms:
      precisions = self.evaluation_scores[query_id]
      f.write("Query " + str(query_id))
      f.write("\n\n\n")
      f.write("Rank   Relevant     Precision         Recall")
      f.write("\n\n")
      for rank in precisions.keys():
        f.write(rank)
        if(precisions[rank]["relevant"]):
          f.write("      R      ")
        else:
          f.write("      N      ")
        f.write("      " + str(precisions[rank]["score"])[:7])
        f.write("             " + str(precisions[rank]["recall"])[:7])
        f.write("\n")

      f.write("\n\n")
      f.write("Precision at 5: ")
      f.write(str(precisions["5"]["score"])[:7])

      f.write("\n\n")
      f.write("Precision at 20: ")
      f.write(str(precisions["20"]["score"])[:7])
      f.write("\n\n")
      f.write("\n\n")
      f.write("\n\n")




e = Evaluation()
n = sys.argv[1]
e.process_and_result(n)

# e.process_and_result("BM25")
# e.process_and_result("Lucene")
# e.process_and_result("tf-idf")
# e.process_and_result("BM25_stoplist")
# e.process_and_result("Lucene_stoplist")
# e.process_and_result("Lucene_feedback")
# e.process_and_result("BM25_feedback")

