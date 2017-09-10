import pickle
import os
import collections
from scipy import stats

class Ttest(object):
  def __init__(self, algo1, algo2):
    self.score_algo1 = self.fetch_scores(algo1)
    self.score_algo2 = self.fetch_scores(algo2)

  def fetch_scores(self, algo):
    scores = collections.OrderedDict()
    completeName = os.path.join(algo + "_avg_precisions" + ".pickle")
    with open(completeName, 'rb') as handle:
      scores = pickle.load(handle)
    return scores

  def calculate_t_test(self):
    a = stats.ttest_ind(self.score_algo1.values(), self.score_algo2.values())
    n = 64
    pval = float(stats.t.sf(abs(a[0]), n - 1))
    return [pval, a[0]]

Baselines = ["BM25", "Lucene", "tf-idf"]
Improved_System = ["BM25_feedback", "BM25_stoplist", "Lucene_feedback", "Lucene_stoplist"]

f = open("../results/t-test-scores.txt", "w+")
alpha = 0.1

for baseline in Baselines:
  for version in Improved_System:
    t = Ttest(baseline, version)
    results = t.calculate_t_test()
    f.write("\n")
    f.write("Baseline: " + baseline)
    f.write("\n")
    f.write("Alternative System: " + version)
    f.write("\n")
    f.write("---------------------------------")
    f.write("\n")
    f.write("P Value: " + str(results[0]))
    f.write("\n")
    f.write("T value: " + str(results[1]))
    f.write("\n")
    if(results[0] > alpha):
      f.write("Null hypothesis cannot be rejected.")
    else:
      f.write("Alternative System is better than Baseline system. Null hyposthesis can be rejected in this case.")
    f.write("\n\n\n")
