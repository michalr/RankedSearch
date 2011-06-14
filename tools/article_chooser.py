# -*- encoding: utf-8 -*-
from progressbar import Percentage, Bar, RotatingMarker, ETA, FileTransferSpeed, ProgressBar
from commands import getoutput

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
                
            
