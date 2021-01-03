#!/usr/bin/env python
import core as archiver
import argparse, sys

#def exec(args):

def main():
    print("Are we starting to crawl yet?")
    siteurl = len(sys.argv) > 1 and sys.argv[1] or "http://books.toscrape.com"

    # Initialize parser
    parser = argparse.ArgumentParser(description = "Example description here")
    parser.add_argument("-o", "--Output", help = "enabling special output mode")
    parser.add_argument("-v", "--Verbose", help = "enabling verbose mode")
    args = parser.parse_args()
    
    if args.Output:
        print (("enabling special output mode (%s)") % (args.Output))
    
    archiver.crawl(siteurl)
    print("Done crawling " + siteurl)

# https://www.analyticsvidhya.com/blog/2015/10/beginner-guide-web-scraping-beautiful-soup-python/
# siteurl = "https://www.pythoncentral.io/execute-python-script-file-shell/"

if __name__ == '__main__':
    main()
