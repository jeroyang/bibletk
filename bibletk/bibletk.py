#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import codecs
import argparse
import pyperclip
import os.path
import logging
import time
import sys
from functools import reduce
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.CRITICAL)

def load_bible_text(path='hb5.txt'):
    """
    Load the bible_text data
    """
    new_path = os.path.join(os.path.dirname(__file__), path)
    with codecs.open(new_path, encoding='big5', errors='ignore') as f:
        return f.read().strip()

def parse_bible(bible_text):
    """
    Parse the bible_text data
    """
    pharses = bible_text.split('\n')[1:]
    return pharses

def build_repository(pharses):
    """
    Build the bible repository as a dict from identifier to context
    Jhn 3:10 --> text in John chapter 3 pharse 10
    """
    repository = {}
    for pharse in pharses:
        book, _, other = pharse.partition(' ')
        locator, _, context = other.partition(' ')
        repository[' '.join([book, locator])] = context
    return repository

def load_bookmap_n_bookid2chinese(path='book_names.txt'):
    new_path = os.path.join(os.path.dirname(__file__), path)
    bookmap = {}
    bookid2chinese = {}
    with open(new_path, encoding='utf8') as f:
        for row in filter(lambda x: len(x)>3 and x[:4]!='中文卷名', f):
            chinese_long, chinese_short, engl_long, engl_short = row.strip().split('\t')
            the_map = {
                chinese_long: engl_short,
                chinese_short: engl_short,
                #engl_long: engl_short,
                #engl_short: engl_short
            }
            bookmap.update(the_map)
            bookid2chinese[engl_short] = chinese_long
    return bookmap, bookid2chinese
    
pharses = parse_bible(load_bible_text())
repository = build_repository(pharses)

book_map, bookid2chinese = load_bookmap_n_bookid2chinese()
book_names = book_map.keys()

def name_normalize(name):
    return book_map[name]

def candidate_filter(context):
    """
    Return the candidate from context
    """
    pattern = '(?s)((?P<out>.*?)(?P<book>加(拉太書)?|士(師記)?|(耶利米哀|雅)?歌|約(翰福音|翰貳書|翰壹書|書亞記|翰參書|伯記|珥書|拿書|三|二|一)?|耶(利米書)?|啟(示錄)?|申(命記)?|(帖撒羅尼迦前|帖撒羅尼迦後|提摩太後|撒迦利亞|提摩太前|哥林多前|俄巴底亞|哥林多後|哈巴谷|彼得後|以西結|彼得前|西番雅|阿摩司|腓利門|腓利比|歌羅西|瑪拉基|以弗所|但以理|以賽亞|希伯來|何西阿|雅各|哈該|羅馬|那鴻|彌迦|猶大|提多|傳道)?書|路(加福音|得記)?|(使徒行)?傳|民(數記)?|利(未記)?|創(世記)?|尼(希米記)?|詩(篇)?|箴(言)?|出(埃及記)?|彌|得|伯|提前|來|撒母耳記下|以斯拉記|但|何|太|拉|腓|以斯帖記|歷代志上|歷代志下|王上|徒|賽|羅|彼前|代上|門|該|拿|林後|彼後|番|帖前|撒上|撒母耳記上|哈|亞|摩|斯|帖後|俄|鴻|代下|撒下|列王紀上|馬太福音|馬可福音|列王紀下|弗|猶|王下|瑪|多|提後|可|哀|雅|結|西|珥|林前))(?P<locator>[〇一二三四五六七八九十廿卅百章\\d:\\-]+)節?'
    for m in re.finditer(pattern, context):
        yield m

number_map = {  '〇': 0,
                '一': 1, 
                '二': 2, 
                '三': 3, 
                '四': 4, 
                '五': 5, 
                '六': 6, 
                '七': 7, 
                '八': 8, 
                '九': 9, 
                '十': 10, 
                '廿': 20, 
                '卅': 30, 
                '百': 100, }

def multiple_replace(text, replace_pairs):
    return reduce(lambda t, item: t.replace(*item), replace_pairs, text)

def interpret_official(chinese_number):
    """
    Interpret chinese number less than 999 into int
    
    >>> interpret_official('一百八十二')
    182
    >>> interpret_official('廿三')
    23
    """
    pattern = r'((?P<hundred>.百)?)(?P<lesser_than_100>{})'.format('[一二三四五六七八九十廿卅]*')
    number = 0
    m = re.match(pattern, chinese_number)
    if m.group('hundred'):
        number += number_map[m.group('hundred')[0]] * 100
    lesser_than_100 = m.group('lesser_than_100')
    pattern = r'(?P<ten>.十)?(?P<one>.+)'
    m = re.match(pattern, lesser_than_100)
    if m.group('ten'):
        number += number_map[m.group('ten')[0]] * 10
    if m.group('one'):
        number += sum([number_map[char] for char in m.group('one')])
    return number

def interpret_sequential(chinese_number):
    """
    Interpret sequential chinese number into int
    
    >>> interpret_sequential('一〇二')
    102
    """
    replace_pair = [(key, str(number_map[key])) for key in '〇一二三四五六七八九']
    return int(multiple_replace(chinese_number, replace_pair))

def translate_number(chinese_number): 
    """
    Translate any kind of chinese numbers (less than 999) into int
    
    >>> translate_number('一百八十二')
    182
    >>> translate_number('一八二')
    182
    """
    if any(['十' in chinese_number, 
           '廿' in chinese_number,
           '卅' in chinese_number,
           '百' in chinese_number]):
        return interpret_official(chinese_number)
    else:
        return interpret_sequential(chinese_number)

def spliter(re_match_from_filter):
    """
    Split given re.match object from candidate filter into (book, locator) tuple 
    """
    book = re_match_from_filter.group('book')
    locator = re_match_from_filter.group('locator')
    return (book, locator)

def parse_range(range_text):
    """
    Split a range text such as '3-5' into [3, 4, 5]
    """
    
    sep = '-'
    if sep in range_text:
        start, end = (int(n) for n in range_text.split(sep))
        return list(range(start, end + 1))
    else:
        return [int(range_text)]
    
def parse_locator(locator):
    """
    Parse given locator such as '一5', '5章2-3'
    """
    pattern = r'(?:(?P<number>\d+)|(?P<chinese>[〇一二三四五六七八九十廿卅百]+))[章:]?(?P<pharse_range>[\d,\-]+)'
    m = re.match(pattern, locator)
    if m.group('number'):
        chapter = int(m.group('number'))
    else:
        chapter = translate_number(m.group('chinese'))
    range_text = m.group('pharse_range')
    pharse_list = parse_range(range_text)
    return chapter, pharse_list

def get_bucket(re_match_from_filter):
    """
    From given re.match object from candidate_filter, 
    return a bucket (a list) of bible identifiers (bookid, chapter, pharse)
    """
    book, locator = spliter(re_match_from_filter)
    chapter, pharse_list = parse_locator(locator)
    bucket = [(name_normalize(book), chapter, pharse) for pharse in pharse_list]
    return bucket

def get_context(book, chapter, pharse):
    """
    Given book, chapter, and pharse number, return the bible context.
    """
    try:
        context = repository['{} {}:{}'.format(book, chapter, pharse)]
        return context
    except KeyError:
        bookname = bookid2chinese[book]
        pharse_name = '{}{}:{}'.format(bookname, chapter, pharse)
        logging.warning('Cannot find this pharse:' + pharse_name)
        raise KeyError('Cannot find this pharse')
    
def format_bucket(bucket):
    bookids = [pharse[0] for pharse in bucket]
    assert len(set(bookids)) == 1
    bookid = bookids[0]
    bookname = bookid2chinese[bookid]
    chapters = [pharse[1] for pharse in bucket]
    assert len(set(chapters)) == 1
    chapter = chapters[0]
    header = '{}{}章'.format(bookname, chapter)
    body = ''.join(['{}{}'.format(p[2], get_context(*p)) for p in bucket])
    return header, body
    
def open_input(filename):
    """
    Read the inputfile, try big5 and utf8 codecs
    """
    try:
        with codecs.open(filename, mode='r', encoding='utf8') as f:
            text = f.read()
    except UnicodeDecodeError:
        with codecs.open(filename, mode='r', encoding='big5') as f:
            text = f.read()
    return text

def text_expand(context):
    """
    Give context, pick out the bible indexes, turn them into normalized scripture, and put the scripture back into the context
    """
    output = []
    end = 0
    for m in candidate_filter(context):
        output.append(m.group('out'))
        try:
            bucket = get_bucket(m)
            formated = format_bucket(bucket)
            output.extend(['《','：'.join(list(formated)), '》'])
        except KeyError:
            output.append(m.group(0))
        except AttributeError:
            output.append(m.group(0))
        except:
            logging.warning(print(context))
        end = m.end()
    output.append(context[end:])
    return ''.join(output)
    
########################

if __name__ == '__main__':
    import pyperclip
    cache = pyperclip.paste()
    start_flag = True
    while True:
        in_context = pyperclip.paste()
        if in_context == 'STOP' and not start_flag:
            sys.exit(0)
        elif in_context != cache:
            start_flag = False
            out_context = text_expand(in_context)
            pyperclip.copy(out_context)
            cache = out_context
        time.sleep(0.1)