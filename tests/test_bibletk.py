#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from builtins import *

"""
test_bibletk
----------------------------------

Tests for `bibletk` module.
"""

import unittest

import re
from bibletk import bibletk

class TestBibletk(unittest.TestCase):

    def test_candidate_filter(self):
        context = "約翰福音5:3-8 創世記三18 利8:1 民四:19"
        results = [m.group(0) for m in bibletk.candidate_filter(context)]
        wanted = ['約翰福音5:3-8',
                  '創世記三18',
                  '利8:1',
                  '民四:19']
        self.assertEqual(results, wanted)

    def test_translate_number(self):
        number = '三百五十六'
        wanted = 356
        result = bibletk.translate_number(number)
        self.assertEqual(result, wanted)
        
        number = '廿一'
        wanted = 21
        result = bibletk.translate_number(number)
        self.assertEqual(result, wanted)
        
        number = '卅'
        wanted = 30
        result = bibletk.translate_number(number)
        self.assertEqual(result, wanted)
        
        number = '二十八'
        wanted = 28
        result = bibletk.translate_number(number)
        self.assertEqual(result, wanted)
        
    def test_spliter(self):
        pattern = r'(?P<book>\D+)(?P<locator>\d+)'
        m = re.match(pattern, 'abc123')
        result = bibletk.spliter(m)
        wanted = ('abc', '123')
        self.assertEqual(result, wanted)
        
    def test_parse_range(self):
        range_text = '3-4'
        wanted = [3, 4]
        result = bibletk.parse_range(range_text)
        self.assertEqual(result, wanted)
        
        range_text = '6'
        wanted = [6]
        result = bibletk.parse_range(range_text)
        self.assertEqual(result, wanted)
    
    def test_parse_locator(self):
        locator = '一5'
        wanted = (1, [5])
        result = bibletk.parse_locator(locator)
        self.assertEqual(result, wanted)
        
        locator = '5:2-3'
        wanted = (5, [2, 3])
        result = bibletk.parse_locator(locator)
        self.assertEqual(result, wanted)
        
        locator = '十八章10-12'
        wanted = (18, [10, 11, 12])
        result = bibletk.parse_locator(locator)
        self.assertEqual(result, wanted)
    
    def test_get_bucket(self):
        pattern = r'(?P<book>.*?)!(?P<locator>.*)'
        m = re.match(pattern, '約翰福音!一章3-4')
        result = bibletk.get_bucket(m)
        wanted = [
                    ('Jhn', 1, 3),
                    ('Jhn', 1, 4),
                 ]
        self.assertEqual(result, wanted)
        
    def test_get_context(self):
        book = 'Jhn'
        chapter = 1
        pharse = 1
        wanted = '太初有道、道與\u3000神同在、道就是\u3000神。'
        result = bibletk.get_context(book, chapter, pharse)
        self.assertEqual(result, wanted)
        
        