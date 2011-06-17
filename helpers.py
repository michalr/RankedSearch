from tools.file_parsing import filter_articles, filter_links, parse_links
from index.creation import create_page_rank_matrix, compute_page_rank
import sys
import marshal

if __name__ == '__main__':
    if len(sys.argv) < 6:
        print "Provide full wikipedia file, interesting articles file, wikilinks file, output filtered wikipedia, output filtered wlikilinks"
        sys.exit() 
    filter_articles(open(sys.argv[1], "rt"), open(sys.argv[2], "rt"), open(sys.argv[4], "wt"))
    filter_links(open(sys.argv[3], "rt"), open(sys.argv[2], "rt"), open(sys.argv[5], "wt"))
    links_dict = parse_links(open(sys.argv[5], "rt"))
    matrix, zero_rows, articles_no = create_page_rank_matrix(links_dict)
    page_rank = compute_page_rank([1.0 / len(matrix) for i in range(len(matrix))], matrix, zero_rows)
    marshal.dump(articles_no, open("articles_no", "wb"))
    marshal.dump(page_rank, open("page_rank", "wb"))