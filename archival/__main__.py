#!/usr/bin/env python
import core as archiver
import getopt, sys

def main():
    print("Are we starting to crawl yet?")
    siteurl = len(sys.argv) > 1 and sys.argv[1] or "http://books.toscrape.com"

    # read commandline arguments, first
    fullCmdArguments = sys.argv

    # - further arguments
    argumentList = fullCmdArguments[1:]

    unixOptions = "ho:v"
    gnuOptions = ["help", "output=", "verbose"]
    try:
        arguments, values = getopt.getopt(argumentList, unixOptions, gnuOptions)
    except getopt.error as err:
        # output error, and return with an error code
        print (str(err))
        sys.exit(2)

    for currentArgument, currentValue in arguments:
        if currentArgument in ("-v", "--verbose"):
            print ("enabling verbose mode")
        elif currentArgument in ("-h", "--help"):
            print ("displaying help")
        elif currentArgument in ("-o", "--output"):
            print (("enabling special output mode (%s)") % (currentValue))

    archiver.crawl(siteurl)
    print("Done crawling " + siteurl)


# https://www.analyticsvidhya.com/blog/2015/10/beginner-guide-web-scraping-beautiful-soup-python/
# siteurl = "https://www.pythoncentral.io/execute-python-script-file-shell/"

if __name__ == '__main__':
    main()
