# -*- encoding: utf-8 -*-
from math import sqrt, log10
import re
from tools.file_parsing import polish_lower

def vectors_sim(v1, v2):
    """
        computes vectors cosine similarity
    """
    num = 0.0
    for key in set(v1.keys()) & set(v2.keys()):
        num += (v1[key] * v2[key])
    def sum_of_squares(v):
        tmp = 0.0
        for key in v.keys():
            tmp += v[key] ** 2
        return tmp
    den = sqrt(sum_of_squares(v1)* sum_of_squares(v2))
    return num / den

def vectors_sim_list(l1, l2):
    num = 0.0
    for i in range(len(l1)):
        num += l1[i] * l2[i]
    def sum_of_squares(l):
        tmp = 0.0
        for elem in l:
            tmp += elem ** 2
        return tmp
    den = sqrt(sum_of_squares(l1)* sum_of_squares(l2))
    return num / den
    

def parse_phrase(raw_phrase, morfologik_object):
    regex = re.compile("[a-zA-Z0-9_ąśćęźżółń]+")
    words_list = [polish_lower(word) for word in regex.findall(raw_phrase)]
    bases = []
    for word in words_list:
        base_forms = morfologik_object.get(word, None)
        if not base_forms:
            base_forms = morfologik_object.get(word.capitalize(), None)
        if not base_forms:
            base_forms = [word]
        bases.append([polish_lower(w) for w in base_forms])
    return bases

def search_phrase(phrase, index, morfologik_object, df, indexed_articles, articles_no, page_rank):
    bases = parse_phrase(phrase, morfologik_object)
    res = [[b] for b in bases[0]]
    for base_forms in bases[1:]:
        next = []
        for elem in res:
            for base in base_forms:
                next.append(elem + [base])
        res = next
    vectors_to_rank = []
    for elem in res:
        try:
            vectors_set = index[elem[0]]
        except KeyError:
            return []
        for base in elem[1:]:
            keys = [article[0] for article in vectors_set]
            new_vectors_set = []
            try:
                for article in index[base]:
                    if article[0] in keys:
                        new_vectors_set += [article]
            except KeyError:
                return []
            vectors_set = new_vectors_set
            # create tf_idf vector for query
        elem_vector = {}
        for word in elem:
            elem_vector[word] = elem_vector.setdefault(word, 0) + 1
        for word in elem_vector.keys():
            elem_vector[word] *= log10((indexed_articles + 1) / (df[word] + 1))
        vectors_to_rank += [(elem_vector, vectors_set)]
    ranking = {}
    for vector_set in vectors_to_rank:
        for vec in vector_set[1]:
            vector_set[0]
            ranking[vec[0]] = max(ranking.setdefault(vec[0], -1), vectors_sim(vector_set[0], vec[1]))
    for article in ranking.keys():
        no = articles_no.get(article, -1)
        if no >= 0:
            ranking[article] += 10 * page_rank[no]
    return [article[0] for article in sorted(ranking.iteritems(), key=lambda (k,v): (v,k), reverse = True)]
        