# -*- encoding: utf-8 -*-
from tools.article_chooser import filter_articles

if __name__ == '__main__':
    wikipedia = open("wikipedia_dla_wyszukiwarek.txt", "rt")
    important = open("interesujace_artykuly.txt", "rt")
    output = open("wikipedia_short.txt", "wt")
    filter_articles(wikipedia, important, output)
    wikipedia.close()
    important.close()
    output.close()