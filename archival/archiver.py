from tqdm import tqdm
from bs4 import BeautifulSoup as bs
from utils import relative_to_static, setup_browser, download_asset

TEST_SCENARIO = False

def archive_links(soup, crawl_url, directory_style, directory_icon):
    fetchedUris = []
    for elem in tqdm(soup.find_all("link"), "Extracting links (css and ico)"):
        elem_url = elem.attrs.get("href") or None
        if(not elem_url):
            # if elem does not contain src or href attribute, just skip
            continue
            
        path_dir = directory_style
        if(elem.attrs.get("type") == "text/css" or (elem["rel"] and elem["rel"][0] == "stylesheet")):
            if("integrity" in elem.attrs):
                elem.attrs.pop("integrity")
            if("crossorigin" in elem.attrs):
                elem.attrs.pop("crossorigin")
        else:
            path_dir = directory_icon

        elem_url = relative_to_static(crawl_url, elem_url);
        if(not elem_url or elem in fetchedUris):
            continue
            
        fetchedUris.append(elem_url)
        file_dl = download_asset(elem_url, output_dir, path_dir, TEST_SCENARIO)
        elem.attrs["href"] = file_dl
    
    return True

def archive_scripts(soup, crawl_url, directory_script):
    fetchedUris = []
    for elem in tqdm(soup.find_all("script"), "Extracting scripts (js)"):
        elem_url = elem.attrs.get("src") or None
        if(not elem_url):
            # if elem does not contain src or href attribute, just skip
            continue

        elem_url = relative_to_static(crawl_url, elem_url);
        if(not elem_url or elem in fetchedUris):
            continue
            
        fetchedUris.append(elem_url)
        file_dl = download_asset(elem_url, output_dir, directory_script, TEST_SCENARIO)
        elem.attrs["src"] = file_dl
    
    return True

def archive_images(soup, crawl_url, directory_image):
    fetchedUris = []
    for elem in tqdm(soup.find_all("img"), "Extracting images (img)"):
        elem_url = elem.attrs.get("src") or None
        if(not elem_url):
            # if elem does not contain src or href attribute, just skip
            continue

        elem_url = relative_to_static(crawl_url, elem_url);
        if(not elem_url or elem in fetchedUris):
            continue
            
        fetchedUris.append(elem_url)
        file_dl = download_asset(elem_url, output_dir, directory_image, TEST_SCENARIO)
        elem.attrs["src"] = file_dl
    
    return True

def archive_urls(soup, crawl_url):
    # change all a hrefs
    for elem in tqdm(soup.find_all("a"), "Fixing links"): #FIXME: why using `soup` instead of `newdom` here? "standardize" x3 say it with me
        elem_url = elem.attrs.get("href") or None
        if(not elem_url or crawl_url == elem_url or elem_url + "/index.html" == crawl_url or elem_url == "/" or elem_url == "index.html"): # FIXME: not properly impl
            continue

        elem_url_static = relative_to_static(crawl_url, elem_url);
        print("Fixing url from " + elem_url + " to " + elem_url_static)
        elem.attrs["href"] = elem_url_static
        
    return True
    
def perform(driver_path, crawl_url, directory_image, directory_script, directory_style, directory_icon, test_scenario):
    driver = setup_browser(driver_path)
    driver.get(crawl_url)
    
    TEST_SCENARIO = test_scenario == True or False

    #read raw and out to BeautifulSoup
    global_dom = driver.page_source
    
    # get website
    soup = bs(global_dom, "html.parser")

    archive_links(soup, crawl_url, directory_style, directory_icon)
    archive_scripts(soup, crawl_url, directory_script)
    archive_images(soup, crawl_url, directory_image)
    archive_urls(soup, crawl_url)
        
    if(test_scenario != True):
        with open(output_dir + "index.html", "w") as f:
            print(soup.prettify(), file=f)
            
    return True