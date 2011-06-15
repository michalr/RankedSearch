# -*- encoding: utf-8 -*-
from math import sqrt
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

def search_phrase(phrase, index, morfologik_object):
    bases = parse_phrase(phrase, morfologik_object)
    res = bases[0]
    for base_forms in bases[1:]:
        next = []
        for elem in res:
            for base in base_forms:
                next.append(elem + [base])
        res = next
    vectors_to_rank = []
    for elem in res:
        vectors_set = set(index[elem[0]])
        for base in elem[1:]:
            vectors_set &= index[base]
        vectors_to_rank += [(elem, vectors_set)]
    ranking = []
    for vector_set in vectors_to_rank:
        local_results = []
        for vec in vector_set[1]:
            local_results.append((vec[0], vectors_sim(vector_set[0], vec[1])))
        ranking.extend(local_results)
    return [article[0] for article in sorted(ranking, key = lambda res: res[1], reverse = True)]
        