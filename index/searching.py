# -*- encoding: utf-8 -*-
from math import sqrt, log10
import re

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
    den = sqrt(sum_of_squares(v1)) * sqrt(sum_of_squares(v2))
    return num / den

def parse_phrase(raw_phrase, morfologik_object):
    regex = re.compile("[a-zA-Z0-9_ąśćęźżółń]+")
    words_list = regex.findall(raw_phrase)
    bases = []
    for word in words_list:
        base_forms = morfologik_object.get(word, [])
        if word.istitle():
            base_forms += morfologik_object.get(word.lower(), [])
        if not base_forms:
            base_forms = [word]
            if word.istitle():
                base_forms += [word.lower()]
        bases.append(base_forms)
    return bases

def search_phrase(phrase, index, morfologik_object, df, indexed_articles):
    bases = parse_phrase(phrase, morfologik_object)
    res = [bases[0]]
    for base_forms in bases[1:]:
        next = []
        for elem in res:
            for base in base_forms:
                next.append(elem + [base])
        res = next
    vectors_to_rank = []
    for elem in res:
        vectors_set = index[elem[0]]
        for base in elem[1:]:
            keys = [article[0] for article in vectors_set]
            new_vectors_set = []
            for article in index[base]:
                if article[0] in keys:
                    new_vectors_set += [article]
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
    return [article[0] for article in sorted(ranking.iteritems(), key=lambda (k,v): (v,k))]
        