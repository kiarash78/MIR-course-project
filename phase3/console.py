import numpy as np
import sys

from logic import (
        clear_index,
        add_data,
        add_pagerank,
        query, 
        calc_hits,
        get_doc_count,
        )
from spider import crawl

def crawl_menu():
    print('Enter number of start links')
    n = int(input())
    li = []
    for i in range(n):
        print(f'enter link number {i}')
        li.append(input())
    print('enter number of docs')
    count = int(input())
    print('enter output path')
    path = input()
    print('are you sure you want to crawl? it might take a few minutes (enter yes for crawling, anything else for stopping)')
    should_crawl = input().lower() == 'yes'
    if not should_crawl:
        return
    crawl(li, crawl_limit=count, output_path=path)
    print('finished crawling!')

def clear_index_menu():
    print('enter address in the following format: address:port')
    print('Example input:')
    print('localhost:9200')
    address = input()
    clear_index(address)

def add_data_menu():
    print('enter address in the following format: address:port')
    print('Example input:')
    print('localhost:9200')
    address = input()
    print('enter data path')
    path = input()
    add_data(address, path)

def add_pagerank_menu():
    print('enter address in the following format: address:port')
    print('Example input:')
    print('localhost:9200')
    address = input()
    print('enter alpha')
    alpha = float(input())
    if alpha <= 0 or alpha >= 1:
        print('alpha should be in (0, 1)')
        return
    add_pagerank(address, alpha=alpha)

def search_menu():
    print('enter address in the following format: address:port')
    print('Example input:')
    print('localhost:9200')
    address = input()
    print('enter title')
    title = input()
    print('enter abstract')
    abstract = input()
    print('enter date')
    date = input()
    print('enter title weight')
    w_title = float(input())
    print('enter abstract weight')
    w_abstract = float(input())
    print('enter date weight')
    w_date = float(input())
    print('should we use page rank? (enter yes for using)')
    use_page_rank = input().lower() == 'yes'
    ans = query(address, title, abstract, date, use_page_rank, w_title, w_abstract, w_date)
    print('summary:')
    keys = 'title', 'date', 'page_rank'
    summary = list(map(lambda x: tuple([x.get(key) for key in keys]), ans))
    print('\n'.join(map(str, summary)))
    print('Do you want the full thing? (enter yes for yes!)')
    full = input().lower() == 'yes'
    if full:
        print(ans)

def calc_hits_menu():
    print('enter address in the following format: address:port')
    print('Example input:')
    print('localhost:9200')
    address = input()
    print('enter number of authors')
    top_k = int(input())
    hits = calc_hits(address, top_k)
    print(hits)

def get_doc_count_menu():
    print('enter address in the following format: address:port')
    print('Example input:')
    print('localhost:9200')
    address = input()
    print(get_doc_count(address))

def exit_function():
    sys.exit(0)

commands = {
        'crawl': crawl_menu,
        'get_doc_count': get_doc_count_menu,
        'clear_index': clear_index_menu,
        'add_data': add_data_menu,
        'add_pagerank': add_pagerank_menu,
        'search': search_menu,
        'get_HITS': calc_hits_menu,
        'exit': exit_function,
        }

while True:
    print('++++++++++++++++')
    print('Possible commands: ')
    print(', '.join(commands.keys()))
    text = input().lower()
    if text not in commands.keys():
        print('invalid command')
        continue
    commands[text]()
