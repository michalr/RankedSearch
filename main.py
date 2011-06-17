# -*- encoding: utf-8 -*-
from tools.file_parsing import parse_articles, read_morfologik
from index.creation import create_index
from index.searching import search_phrase

import marshal
import sys


if __name__ == '__main__':
    if len(sys.argv) < 4:
        print "Provide file with queries, file with articles, morfologik file"
        sys.exit()
    query_file = open("%s" % sys.argv[1], "rt")
    articles_no = marshal.load(open("articles_no", "rb"))
    page_rank = marshal.load(open("page_rank", "rb"))
    input = open("%s" % sys.argv[2], "rt")
    morfologik_file = open("%s" % sys.argv[3], "rt")
    morfologik_object = read_morfologik(morfologik_file)
    morfologik_file.close()
    art_dict, df = parse_articles(input, morfologik_object)
    indexed_articles = len(art_dict.keys())
    input.close()
    index = create_index(art_dict, df)
    #import ipdb
    #ipdb.set_trace()
    for line in query_file:
        print "QUERY: %s" % line.strip()
        result = search_phrase(line.strip(), 
                               index, morfologik_object, 
                               df, indexed_articles, 
                               articles_no, page_rank)
        for res in result:
            print res
        print "\n"