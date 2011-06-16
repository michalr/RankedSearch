# -*- encoding: utf-8 -*-
from tools.file_parsing import parse_articles, read_morfologik
from index.creation import create_index
from index.searching import search_phrase

if __name__ == '__main__':
    input = open("wikipedia_short.txt", "rt")
    morfologik_file = open("morfologik.txt", "rt")
    morfologik_object = read_morfologik(morfologik_file)
    morfologik_file.close()
    art_dict, df = parse_articles(input, morfologik_object)
    indexed_articles = len(art_dict.keys())
    input.close()
    index = create_index(art_dict, df)
    result = search_phrase("mistrz klawiatury", index, morfologik_object, df, indexed_articles)
    print result