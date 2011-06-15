# -*- encoding: utf-8 -*-
from progressbar import Percentage, Bar, RotatingMarker, ETA, FileTransferSpeed, ProgressBar
from commands import getoutput
import re

def filter_articles(art_file, imp_file, out_file):
    widgets = ['Parsing %s: ' % imp_file.name, Percentage(), ' ', 
               Bar(marker=RotatingMarker()), ' ', ETA(), 
               ' ', FileTransferSpeed()]
    pbar = ProgressBar(widgets=widgets, maxval=int(getoutput("wc -l %s" % imp_file.name).split()[0])).start()
    important = []
    i = 0
    for line in imp_file:
        important.append(line.rstrip("\n"))
        pbar.update(i)
        i += 1
    pbar.finish()
    article = ""
    title = ""
    imp_title = ""
    widgets[0] = 'Parsing %s' % art_file.name
    pbar = ProgressBar(widgets=widgets, maxval=int(getoutput("wc -l %s" % art_file.name).split()[0])).start()
    i = 0
    for line in art_file:
        if line.startswith("##TITLE##"):
            title = line.lstrip("##TITLE##").rstrip("\n").strip()
            if title in important:
                imp_title = title
                if article:
                    out_file.write(article)
                    article = ""
            else:
                imp_title = ""
        if imp_title:
            article += line
        pbar.update(i)
        i += 1
    if article:
        out_file.write(article)
    pbar.finish()
    
def read_morfologik(morfologik_file):
    morfo = {}
    widgets = ['Parsing %s: ' % morfologik_file.name, Percentage(), ' ', 
               Bar(marker=RotatingMarker()), ' ', ETA(), 
               ' ', FileTransferSpeed()]
    pbar = ProgressBar(widgets=widgets, maxval=int(getoutput("wc -l %s" % morfologik_file.name).split()[0])).start()
    i = 0
    for line in morfologik_file:
        l = line.split("\t")
        l[0] = l[0].decode('iso-8859-2').encode('utf-8')
        l[1] = l[1].decode('iso-8859-2').encode('utf-8')
        morfo[l[0]] = morfo.setdefault(l[0], []) + [l[1]]
        i += 1
        pbar.update(i)
    pbar.finish()
    return morfo
                
def parse_articles(art_file, morfologik_object):
    """
        Returns a dictionary mapping title => set_of_base_words_in_article with frequencies
        Returns a df dictionary mapping base_word => document frequency
    """
    
    def get_bases_stats(article, df):
        tf = {}
        words_list = regex.findall(article) + regex.findall(article)
        for word in words_list:
            base_forms = morfologik_object.get(word, [])
            if word.istitle():
                base_forms += morfologik_object.get(word.lower(), [])
            if not base_forms:
                base_forms = [word]
                if word.istitle():
                    base_forms += [word.lower()]
            for base in base_forms:
                tf[base] = tf.setdefault(base, 0) + 1
        for base in tf.keys():
            df[base] = df.setdefault(base, 0) + 1
        return tf
                    
    widgets = ['Parsing %s: ' % art_file.name, Percentage(), ' ', 
               Bar(marker=RotatingMarker()), ' ', ETA(), 
               ' ', FileTransferSpeed()]
    pbar = ProgressBar(widgets=widgets, maxval=int(getoutput("wc -l %s" % art_file.name).split()[0])).start()
    i = 0
    regex = re.compile("[a-zA-Z0-9_ąśćęźżółń]+")
    article = ""
    title = ""
    res = {}
    df = {}
    for line in art_file:
        if line.startswith("##TITLE##"):
            new_title = line.lstrip("##TITLE##").rstrip("\n").strip()
            if article:
                res[title] = get_bases_stats(article, df)
                article = ""
            title = new_title
        else:
            article += line
        pbar.update(i)
        i += 1
    res[title] = get_bases_stats(article, df)
    pbar.finish()
    return (res, df)           
