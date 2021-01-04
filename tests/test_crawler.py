#!/usr/bin/env python
from archival import core as archiver

# first test

def test_mytest():
    assert archiver.crawl("http://books.toscrape.com", test_scenario = True) == True

# second test

def func(x):
    return x + 1

def test_answer():
    assert func(3) == 4
