import os
import copy
import pickle
from collections import Counter
from operator import itemgetter
import collections
import math
from datetime import datetime

docdict ={}
doc_term_dict={}
empty_list=[]
uniinverteddict ={}
doc_name_list=[]        # added as part of PRF, saves name of 20 ranks
query_term_dict={}          # query number -> list of original query terms
new_query_term_dict={}      # query number -> list of all query terms
expnd_query_term_dict={}    # query number -> list of expanded query terms
exqdict_with_term_count={}
doc_rank_dict={}        # added as part of PRF, saves top 20 ranks for every query
new_query_dict = {}
final_query = {}
final_query_1 = {}

#def check_in_list()

def main():
    #completeName = os.path.join("doc_rank_dict" + ".txt")
    completeName = os.path.join("lucene_doc_rank_dict" + ".txt")
    with open(completeName, 'rb') as handle:
        doc_rank_dict = pickle.load(handle)

    print (doc_rank_dict.__len__())

    completeName = os.path.join(
                                    "QueryParsed" + ".pickle")
    with open(completeName, 'rb') as handle:
        query_term_dict = pickle.load(handle)

    # completeName = os.path.join("/Users/prasadtajane/PycharmProjects/untitled/Project/4_Input",
    #                                 "DocpickleFile" + ".txt")
    # with open(completeName, 'rb') as handle:
    #     docdict = pickle.load(handle)
        # print b

    completeName = os.path.join(
                                    "Index" + ".pickle")
    with open(completeName, 'rb') as handle:
        uniinverteddict = pickle.load(handle)
        # print b
    doctabledict={}


    print ("*"*100)
    print ("doc_rank_dict")
    # print (doc_rank_dict)
    print ("*"*100)
    print ("query_term_dict")
    # print (query_term_dict)
    print ("*"*100)
    print ("docdict")
    #print (docdict)
    print ("*"*100)
    print ("uniinverteddict")
    # print (uniinverteddict)
    print ("*"*100)
    print (datetime.now().strftime('%Y-%m-%d %H:%M:%S'))


    for uni_term, value in uniinverteddict.items():
        for doc_name in value.keys():
            if not (doc_term_dict.keys().__contains__(doc_name)):
                doc_term_dict[doc_name] = empty_list
            doc_term_dict[doc_name].append(uni_term)

    print ("doc_term_dict created")
    print (datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    #for document in doc_term_dict.keys():
    #    doc_len = doc_term_dict[document].__len__()
    #    term_occr_dict = collections.Counter(doc_term_dict[document])
    #    dictn = {}

    #    for term in term_occr_dict:
    #        dictn[term] = term_occr_dict[term]/doc_len

    #    doc_term_freq_dict[document] = copy.copy(dictn)

    # print(doc_rank_dict.keys())

    for query_num, docs in doc_rank_dict.items():
        # expnd_query_term_dict[query_num] = query_term_dict[query_num]
        expnd_query_term_dict[query_num] = empty_list
        for document in docs:
            mergedlist = expnd_query_term_dict[query_num] + doc_term_dict[document]
            expnd_query_term_dict[query_num] = copy.copy(mergedlist)

    print ("expnd_query_term_dict created")
    print (datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    #exqdict_with_term_count
    for q_num, t_list in expnd_query_term_dict.items():
        exqdict_with_term_count[q_num] = collections.Counter(t_list)
        # converted      query number -> list_of_query_terms       into      query number -> dict('term', count)

    print ("exqdict_with_term_count created")
    print (datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    print ("doc_term_dict")
    # print (doc_term_dict)
    print ("*"*100)
    print ("expnd_query_term_dict")
    #print (expnd_query_term_dict)
    print ("*"*100)
    print ("exqdict_with_term_count")
    # print (exqdict_with_term_count)
    #print ()


    for qnum, orig_q_terms in query_term_dict.items():
        orig_q_terms = orig_q_terms.split()
        #print qnum
        #print orig_q_terms
        if orig_q_terms.__contains__(""):
            orig_q_terms.remove("")
        #print orig_q_terms
        #print orig_q_terms.__len__()
        q_len = orig_q_terms.__len__()
        h_limit = math.ceil(q_len + 5)
        #print (str(qnum) + " : " + " qlen -> " + str(q_len) + " hlim -> " + str(h_limit))

        #print qnum
        each_query_term_count = collections.Counter(orig_q_terms)

        print ("*"*100)
        print ("each_query_term_count")
        # print (each_query_term_count)
        print ("here")
        #new_exqdict_with_term_count = each_query_term_count + exqdict_with_term_count
        print ("passed")

        # all_terms = []
        # all_terms = orig_q_terms + exqdict_with_term_count[str(qnum)].keys()
        # new_query_term_dict[qnum] = copy.copy(orig_q_terms)

        # rocchio_value = {}
        # alpha = 24.0
        # beta = 16.0
        # gamma = 4.0

        # alpha qj
        # for each_term in each_query_term_count:
        #     rocchio_value[each_term] = 0
        # # print(exqdict_with_term_count.keys())
        # # print(exqdict_with_term_count)
        # # print(qnum)
        # for e_term in exqdict_with_term_count[str(qnum)]:
        #     rocchio_value[e_term] = 0
        # print ("initialized rocchio")

        # for e_term1 in each_query_term_count:
        #     rocchio_value[e_term1] += alpha * each_query_term_count[e_term1]

        # print ("*"*100)
        # print ("rocchio after query terms")
        # print (rocchio_value)

        # for every_term in exqdict_with_term_count[str(qnum)]:
        #     #print (every_term)
        #     #print (exqdict_with_term_count[every_term])
        #     #print("exqdict_with_term_count")
        #     #print (exqdict_with_term_count)
        #     rocchio_value[each_term] += beta * exqdict_with_term_count[str(qnum)][every_term]/(20.0*exqdict_with_term_count[str(qnum)].__len__())
        #     rocchio_value[each_term] -= gamma * exqdict_with_term_count[str(qnum)][every_term]/(3184.0*exqdict_with_term_count[str(qnum)].__len__())

        # print ("")
        # print ("rocchio values for query number -")
        # # print (qnum)
        # # print (rocchio_value)
        # print ("")

        # rntr = 1
        # new_query = []
        # for each_term in rocchio_value.keys():
        #     if rntr <= q_len:
        #         rntr += 1
        #         continue
        #     elif rntr >= h_limit:
        #         break
        #     else:
        #         new_query.append(each_term)
        #         rntr += 1

        # new_query_dict[qnum] = copy.copy(new_query)


        cntr = 1
        # print exqdict_with_term_count[qnum]
        for new_q_terms in exqdict_with_term_count[str(qnum)].keys():
            if cntr <= q_len:
                cntr += 1
                continue
            elif cntr >= h_limit:
                break
            else:
                orig_q_terms.append(new_q_terms)
                cntr += 1
        query_term_dict[qnum] = orig_q_terms



    print ("*"*100)
    print ("query_term_dict")
    # print (query_term_dict)

    file = open("new_queries.txt", "a")

    for qn, orig_q in query_term_dict.items():
        print qn
        print(orig_q)
        p = " ".join(orig_q)
        final_query_1[qn] = p
        file.write("\n")
        file.write(p)
        print p
        print orig_q.__len__()

    file.close()

    # for qn, orig_q in new_query_dict.items():
    #     print qn
    #     s = " ".join(orig_q)
    #     final_query[qn] = s
    #     print s
    #     print orig_q.__len__()

    # completeName = os.path.join(
    #                             "new_query_dict" + ".txt")
    # file1 = open(completeName, "wb")
    # pickle.dump(final_query, file1)

    #completeName = os.path.join("new_query_dict_2" + ".txt")
    completeName = os.path.join("lucence_new_query_dict_2" + ".txt")
    file1 = open(completeName, "wb")
    pickle.dump(final_query_1, file1)

if __name__ == "__main__":
    main()
