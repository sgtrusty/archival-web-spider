#!/usr/bin/env python
import core as archiver
import argparse, sys

def parseArgs():
    parser = argparse.ArgumentParser(description = "Example description here")
    parser.add_argument("-o", "--Output", help = "enabling special output mode")
    parser.add_argument("-v", "--Verbose", help = "enabling verbose mode", action='store_true')
    args, unkn = parser.parse_known_args()
    
    if args.Output:
        print (("enabling special output mode (%s)") % (args.Output))
        
    if args.Verbose:
        print ("verbose enabled")
        
def main():
    parseArgs()
    
    siteurl = len(sys.argv) > 1 and not sys.argv[-1] in ("-o", "-v", "--Output", "--Verbose") and sys.argv[-1] or "http://books.toscrape.com"
    print("Crawling site: " + siteurl)
    archiver.crawl(siteurl)
    print("Done crawling " + siteurl)

# https://www.analyticsvidhya.com/blog/2015/10/beginner-guide-web-scraping-beautiful-soup-python/
# siteurl = "https://www.pythoncentral.io/execute-python-script-file-shell/"

if __name__ == '__main__':
    main()
