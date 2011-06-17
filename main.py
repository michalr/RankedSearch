# -*- encoding: utf-8 -*-
from tools.file_parsing import parse_articles, read_morfologik, filter_articles, parse_links, filter_links
from index.creation import create_index, create_page_rank_matrix, compute_page_rank
from index.searching import search_phrase

import marshal


if __name__ == '__main__':
    #filter_articles(open("wikipedia_dla_wyszukiwarek.txt", "rt"), open("interesujace_artykuly.txt", "rt"), open("wikipedia_short2.txt", "wt"))
    #filter_links(open("wikilinki.txt", "rt"), open("interesujace_artykuly.txt", "rt"), open("wikilinki_short.txt", "wt"))
    """
    links_dict = parse_links(open("wikilinki_short.txt", "rt"))
    matrix, zero_rows, articles_no = create_page_rank_matrix(links_dict)
    page_rank = compute_page_rank([1.0 / len(matrix) for i in range(len(matrix))], matrix, zero_rows)
    marshal.dump(articles_no, open("articles_no", "wb"))
    marshal.dump(page_rank, open("page_rank", "wb"))
    """
    input = open("wikipedia_short2.txt", "rt")
    morfologik_file = open("morfologik.txt", "rt")
    morfologik_object = read_morfologik(morfologik_file)
    morfologik_file.close()
    art_dict, df = parse_articles(input, morfologik_object)
    indexed_articles = len(art_dict.keys())
    input.close()
    index = create_index(art_dict, df)
    print "Index built"
    result = search_phrase("mistrz klawiatury", index, morfologik_object, df, indexed_articles)
    print "QUERY: mistrz klawiatury"
    print result
    result = search_phrase("asnyk", index, morfologik_object, df, indexed_articles)
    print "QUERY: asnyk"
    print result
    result = search_phrase("kostium kąpielowy", index, morfologik_object, df, indexed_articles)
    print "QUERY: kostium kąpielowy"
    print result
