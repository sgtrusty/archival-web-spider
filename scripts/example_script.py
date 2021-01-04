#!/usr/bin/env python
import archival.core as archiver
import argparse, sys
import os

def parse_args():
    parser = argparse.ArgumentParser(description = "Example description here")
    parser.add_argument("-o", "--Output", help = "enabling special output mode")
    parser.add_argument("-v", "--Verbose", help = "enabling verbose mode", action='store_true')
    args, unkn = parser.parse_known_args()
    
    if args.Output:
        print (("enabling special output mode (%s)") % (args.Output))
        
    if args.Verbose:
        print ("verbose enabled")
        
def start_run(crawl_url): # TODO: add verbose option usage
    print("Crawling site: " + crawl_url)
    result = archiver.crawl(crawl_url, output_dir = os.path.dirname(os.path.realpath(__file__)) + "/output/")
    print("Done crawling " + crawl_url)
    return result

def __main__():
    parse_args()
    crawl_url = len(sys.argv) > 1 and not sys.argv[-1] in ("-o", "-v", "--Output", "--Verbose") and sys.argv[-1] or "http://books.toscrape.com"
    start_run(crawl_url)

if __name__ == '__main__':
    __main__()
