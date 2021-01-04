from tqdm import tqdm
from bs4 import BeautifulSoup as bs
from .utils import relative_to_static, setup_browser, download_asset

class Archiver(object):
    def __init__(self,**kwargs):
        self.test_scenario = kwargs['test_scenario']
        
    def add_directory_base(self, directory_base):
        self.directory_base = directory_base
    def add_directory_image(self, directory_image):
        self.directory_image = directory_image
    def add_directory_script(self, directory_script):
        self.directory_script = directory_script
    def add_directory_style(self, directory_style):
        self.directory_style = directory_style
    def add_directory_icon(self, directory_icon):
        self.directory_icon = directory_icon

    def archive_links(self):
        fetchedUris = []
        for elem in tqdm(self.soup.find_all("link"), "Extracting links (css and ico)"):
            elem_url = elem.attrs.get("href") or None
            if(not elem_url):
                # if elem does not contain src or href attribute, just skip
                continue
                
            path_dir = self.directory_style
            if(elem.attrs.get("type") == "text/css" or (elem["rel"] and elem["rel"][0] == "stylesheet")):
                if("integrity" in elem.attrs):
                    elem.attrs.pop("integrity")
                if("crossorigin" in elem.attrs):
                    elem.attrs.pop("crossorigin")
            else:
                path_dir = self.directory_icon

            elem_url = relative_to_static(self.archival_url, elem_url);
            if(not elem_url or elem in fetchedUris):
                continue
                
            fetchedUris.append(elem_url)
            file_dl = download_asset(elem_url, self.directory_base, path_dir, self.test_scenario)
            elem.attrs["href"] = file_dl
        
        return True

    def archive_scripts(self):
        fetchedUris = []
        for elem in tqdm(self.soup.find_all("script"), "Extracting scripts (js)"):
            elem_url = elem.attrs.get("src") or None
            if(not elem_url):
                # if elem does not contain src or href attribute, just skip
                continue

            elem_url = relative_to_static(self.archival_url, elem_url);
            if(not elem_url or elem in fetchedUris):
                continue
                
            fetchedUris.append(elem_url)
            file_dl = download_asset(elem_url, self.directory_base, self.directory_script, self.test_scenario)
            elem.attrs["src"] = file_dl
        
        return True

    def archive_images(self):
        fetchedUris = []
        for elem in tqdm(self.soup.find_all("img"), "Extracting images (img)"):
            elem_url = elem.attrs.get("src") or None
            if(not elem_url):
                # if elem does not contain src or href attribute, just skip
                continue

            elem_url = relative_to_static(self.archival_url, elem_url);
            if(not elem_url or elem in fetchedUris):
                continue
                
            fetchedUris.append(elem_url)
            file_dl = download_asset(elem_url, self.directory_base, self.directory_image, self.test_scenario)
            elem.attrs["src"] = file_dl
        
        return True

    def archive_urls(self):
        # change all a hrefs
        for elem in tqdm(self.soup.find_all("a"), "Fixing links"):
            elem_url = elem.attrs.get("href") or None
            if(not elem_url or self.archival_url == elem_url or elem_url + "/index.html" == self.archival_url or elem_url == "/" or elem_url == "index.html"): # FIXME: not properly impl
                continue

            elem_url_static = relative_to_static(self.archival_url, elem_url);
            print("Fixing url from " + elem_url + " to " + elem_url_static)
            elem.attrs["href"] = elem_url_static
            
        return True
        
    def driver_start(self, driver_path):
        self.driver = setup_browser(driver_path)
        
    def perform(self, archival_url):
        self.archival_url = archival_url

        # start by browsing
        self.driver.get(self.archival_url)
        
        # read raw website through BeautifulSoup
        self.soup = bs(self.driver.page_source, "html.parser")

        # archive assets -- TODO: check if each dir has been added
        self.archive_links()
        self.archive_scripts()
        self.archive_images()
        self.archive_urls()
            
        if(self.test_scenario != True):
            with open(self.directory_base + "index.html", "w") as f:
                print(self.soup.prettify(), file=f)
                
        return True