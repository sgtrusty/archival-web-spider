#!/usr/bin/env python

# TODO: https://www.thepythoncode.com/article/using-threads-in-python
# TODO: look into using CSS selectors which is, generally, a more concise way to locate the elements. For example, you can replace table = soup.find('table', {'class': 'tablesorter'}) with table = soup.select_one('table.tablesorter'). Or, you can replace:
#links = []
#for anchor in soup.findAll('a', href=True):
#    if 'imported' in anchor['href']:
#        links.append('link' + anchor['href'])
# CHANGE WITH:
#links = ['link' + anchor['href'] for anchor in soup.select("a[href*=imported]")]
#src: https://codereview.stackexchange.com/questions/89956/using-beautifulsoup-to-scrape-various-tables-and-combine-in-a-csv-file
#src: https://www.scrapingbee.com/blog/python-web-scraping-beautiful-soup/
# TODO: StudlyCaps for classes, camelCase only to conform to pre-existing conventions
# https://en.wikipedia.org/wiki/Comment_(computer_programming)#Tags
# https://www.reddit.com/r/Python/comments/mkes7/how_do_you_keep_track_of_todos/
# TODO: HACK: startswith for http:// url refix / or alternatively, use CSS slc
# TODO: identify *nix and propose Chromium/Chrome/Firefox default driver dir (or accept runtime variable)
# TODO: urllib.request AND requests ???
# TODO: ad-revenue and re-visits help some sites. consider header() javascript if there is internet aval
# XXX: can mass CSS @ https://stackoverflow.com/questions/32962474/how-can-i-create-a-stylesheet-external-link-using-beautifulsoup

# notes:
## options:
### deduplicating script cont
### external script as means of memory storage (elastic mapping)
### inline styles

import sys
import urllib.request
import requests
import os
from tqdm import tqdm
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin, urlparse, quote_plus
from selenium import webdriver
from os.path import splitext as split_text

global_dom = None
FOLDERNAME = 'output'

#Also the script that check if the directory exists, if it don't exist create it.
#DIRECTORY_FOLDER = os.path.dirname(os.path.realpath(__file__)) + '/' + FOLDERNAME + '/'
DIRECTORY_FOLDER = FOLDERNAME + '/'
DIRECTORY_IMAGES = 'images/'
DIRECTORY_SCRIPT = 'script/'
DIRECTORY_STYLE = 'style/'
DIRECTORY_ICONS = 'icons/'

def relative_to_static(url, elem):
    # make the URL absolute by joining domain with the URL that is just extracted
    elem_url = urljoin(url, elem)
    try:
        pos = elem_url.index("?") # make sure it doesnt include urlvars
        elem_url = elem_url[:pos]
    except ValueError:
        pass

    # finally, if the url is valid
    if is_valid(elem_url):
        return elem_url

    return None

def is_valid(url):
    """
    Checks whether `url` is a valid URL.
    """
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)

# https://www.thepythoncode.com/article/download-web-page-images-python
# also scrapingbee 101 for socket manual

def download(url, pathname):
    """
    Downloads a file given an URL and puts it in the folder `pathname`
    """

    # if path doesn't exist, make that path dir
    if not os.path.exists(DIRECTORY_FOLDER + pathname) and not os.path.isdir(DIRECTORY_FOLDER + pathname):
        os.makedirs(DIRECTORY_FOLDER + pathname)

    # download the body of response by chunk, not immediately
    response = requests.get(url, stream=True)
    # get the total file size
    file_size = int(response.headers.get("Content-Length", 0))
    # get the file name
    filename = os.path.join(pathname, url.split("/")[-1])  # todo: custom filenames
    if(filename == pathname):
        url = quote_plus(url)
        url = (url[:255]) if len(url) > 255 else url
        filename = filename + url
    
    # progress bar, changing the unit to bytes instead of iteration (default by tqdm)
    text = "Downloading {filename}".format(filename=filename)
    progress = tqdm(response.iter_content(1024), total=file_size, unit="B", unit_scale=True, unit_divisor=1024, desc=text)
    
    # added DIRECTORY_FOLDER instead for relative `filename` reading
    with open(DIRECTORY_FOLDER + filename, "wb") as f:
        for data in progress:
            # write data read to the file
            f.write(data)
            # update the progress bar manually
            progress.update(len(data))

    return filename

def setup_browser(driver_path):
    """Returns a Chrome browser instance."""

    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--incognito')
    options.add_argument('--headless')
    return webdriver.Chrome(driver_path, options=options)

def crawl(url, *positional_parameters, **keyword_parameters):
    global global_dom
    #Query the website and return the html to the variable 'page'
    # page = urllib.request.urlopen(siteurl) #For python 2 use urllib2.urlopen(wiki)
    # raw = page.read()

    #Parse the html in the 'page' variable, and store it in Beautiful Soup format
    driver_path = None
    if('driver' in keyword_parameters):
        driver_path = keyword_parameters['driver']
    else:
        try:
            driver_path = os.environ["CHROME_DRIVER_PATH"] # base port was /usr/lib/chromium/chromedriver
        except KeyError as e:
            raise KeyError("Expect CHROME_DRIVER_PATH as environment variable")
        
    driver = setup_browser(driver_path)
    driver.get(url)

    #read raw and out to BeautifulSoup
    global_dom = driver.page_source

    if not os.path.exists(DIRECTORY_FOLDER):
        os.makedirs(DIRECTORY_FOLDER)
        os.makedirs(DIRECTORY_FOLDER + DIRECTORY_IMAGES)
        os.makedirs(DIRECTORY_FOLDER + DIRECTORY_SCRIPT)
        os.makedirs(DIRECTORY_FOLDER + DIRECTORY_STYLE)
        os.makedirs(DIRECTORY_FOLDER + DIRECTORY_ICONS)

    #Check if image directory is ready TODO: add to prev if
    #DIRECTORY_IMAGES = os.path.dirname(os.path.realpath(__file__)) + '/' + FOLDERNAME + '/images/'
    #if not os.path.exists(DIRECTORY_IMAGES):
        #os.makedirs(DIRECTORY_IMAGES)

    # get website
    soup = bs(global_dom, "html.parser")

    fetchedUris = []
    for elem in tqdm(soup.find_all(["img", "script", "link"]), "Extracting ico, css, image and js"):
        type = ""
        elem_url = elem.attrs.get("src") or elem.attrs.get("href") or None
        if(elem.name == "link" and (elem.attrs.get("type") == "text/css" or (elem["rel"] and elem["rel"][0] == "stylesheet"))):
            type = "css"
        elif(elem.name == "script"):
            type = "script"
        else:
            if(elem.name != "img"):
                type = "ico"
            else:
                type = "img"
#        else:
#            continue

        if(type == "css"): # TODO: add `optionalCrossOriginAllow` or something here
            if("integrity" in elem.attrs):
                elem.attrs.pop("integrity")
            if("crossorigin" in elem.attrs):
                elem.attrs.pop("crossorigin")
        
        if(not elem_url):
            # if elem does not contain src or href attribute, just skip
            continue

        elem_url = relative_to_static(url, elem_url);
        if(not elem_url or elem in fetchedUris):
            continue
            
        fetchedUris.append(elem_url)
    
        options = {
            "img": DIRECTORY_IMAGES,
            "css" : DIRECTORY_STYLE,
            "script" : DIRECTORY_SCRIPT, # TODO: data-src, integrity, crossorigin
            "ico" : DIRECTORY_ICONS
        }
        pathname = options[type]
            
        file_dl = download(elem_url, pathname)
        # todo: custom filenames
        if(type=="css"):
            elem.attrs["href"] = file_dl
        else:
            elem.attrs["src"] = file_dl
    
    # change all a hrefs
    for elem in tqdm(soup.find_all("a"), "Fixing links"): #FIXME: why using `soup` instead of `newdom` here? "standardize" x3 say it with me
        elem_url = elem.attrs.get("href") or None
        if(not elem_url or url == elem_url or elem_url + "/index.html" == url or elem_url == "/" or elem_url == "index.html"): # FIXME: not properly impl
            continue

        elem_url_static = relative_to_static(url, elem_url);
        print("Fixing url from " + elem_url + " to " + elem_url_static)
        elem.attrs["href"] = elem_url_static
        
    with open(DIRECTORY_FOLDER + "index.html", "w") as f:
        print(soup.prettify(), file=f)
    return
    
