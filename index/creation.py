# -*- encoding: utf-8 -*-
from math import log10
from searching import vectors_sim_list
from progressbar import Percentage, Bar, RotatingMarker, ETA, FileTransferSpeed, ProgressBar
from commands import getoutput

ALFA = 0.1
TRESHOLD = 0.99

def create_index(art_dict, df):
    index = {}
    articles = len(art_dict.keys())
    widgets = ['Creating index: ' , Percentage(), ' ', 
               Bar(marker=RotatingMarker()), ' ', ETA(), 
               ' ', FileTransferSpeed()]
    pbar = ProgressBar(widgets=widgets, maxval=articles).start()
    i = 0
    for article, base_forms_freq in art_dict.iteritems():
        tf_idf_vector = {}
        for base, freq in base_forms_freq.iteritems():
            tf_idf_vector[base] = freq * log10(articles / df[base])
        for base in base_forms_freq.keys():
            index[base] = index.setdefault(base, []) + [(article, tf_idf_vector)]
        pbar.update(i)
        i += 1
    pbar.finish()
    return index

def create_page_rank_matrix(links_dict):
    articles = links_dict.keys()
    for key in links_dict.keys():
        articles.extend(links_dict[key])
    articles = list(set(articles))
    columns = [[] for i in range(len(articles))]
    for i in range(len(articles)):
        for j in range(len(articles)):
            if articles[j] in links_dict.get(articles[i], []):
                columns[j].append(1)
            else:
                columns[j].append(0)
    zeroes_only = []
    new_columns = [{} for i in range(len(articles))]
    for i in range(len(articles)):
        ones_in_row = 0
        for j in range(len(articles)):
            if columns[j][i] == 1:
                ones_in_row += 1
        if ones_in_row == 0:
            zeroes_only.append(i)
        if ones_in_row > 0:
            for j in range(len(articles)):
                if columns[j][i] == 1:
                    new_columns[j][i] = (1.0 - ALFA) / ones_in_row
    articles_no = {}
    for i in range(len(articles)):
        articles_no[articles[i]] = i
    return (new_columns, zeroes_only, articles_no)

def vector_matrix_multiply(vector, matrix, zero_rows):
    res = []
    zeros_value = 0
    for row in zero_rows:
        zeros_value += vector[row]
    zeros_value /= len(vector)
    for i in range(len(vector)):
        yi = zeros_value + ALFA / len(vector)
        for key, value in matrix[i].iteritems():
            yi += vector[key] * value
        res.append(yi)
    return res

def compute_page_rank(init_vector, matrix, zero_rows):
    prev_vector = init_vector
    next_vector = vector_matrix_multiply(prev_vector, matrix, zero_rows)
    while vectors_sim_list(prev_vector, next_vector) < TRESHOLD:
        prev_vector = next_vector
        next_vector = vector_matrix_multiply(prev_vector, matrix, zero_rows)
    return next_vector
        