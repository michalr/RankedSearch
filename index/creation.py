# -*- encoding: utf-8 -*-
from math import log10

def create_index(art_dict, df):
    index = {}
    articles = len(art_dict.keys())
    for article, base_forms_freq in art_dict.iteritems():
        tf_idf_vector = {}
        for base, freq in base_forms_freq.iteritems():
            tf_idf_vector[base] = freq * log10(articles / df[base])
        for base in base_forms_freq.keys():
            index[base] = index.setdefault(base, []) + [(article, tf_idf_vector)]
    return index