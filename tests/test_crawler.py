#!/usr/bin/env python
from archival import core as archiver

def test_mytest():
    siteurl = "http://books.toscrape.com"
    archiver.crawl(siteurl)

def func(x):
    return x + 1

def test_answer():
    assert func(3) == 4
