import requests
from bs4 import BeautifulSoup
import urllib3
from selenium import webdriver

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class Soup():
    """ This class is used to send request to page and get html data """

    def __init__(self):
        pass
    
    def loader(self, path):
        """
        This function is used to scrape content from provided URL by opening a headless browser
        
        Args:
            path (str): URL to extract data
            
        Returns:
            soup (bs4.BeautifulSoup): complete document which trying to scrape
        """

        chrome_options = webdriver.ChromeOptions()
        chrome_prefs = {"profile.managed_default_content_settings.images": 2}
        chrome_options.add_argument('--ignore-certificate-errors')
        chrome_options.add_argument('--ignore-ssl-errors')
        chrome_options.add_experimental_option("prefs", chrome_prefs)
        driver = webdriver.Chrome(chrome_options=chrome_options)
        driver.get(path)
        c = driver.page_source
        soup = BeautifulSoup(c, "html.parser")
        driver.close()
        return soup
    
    def soup_maker(self, path):
        """
        This function is used to scrape content from provided URL by sending request
        
        Args:
            path (str): URL to extract data
            
        Returns:
            soup (bs4.BeautifulSoup): complete document which trying to scrape
        """

        r = requests.get(path, verify=False)
        c = r.content
        soup = BeautifulSoup(c, "html.parser")
        if 'access denied' in soup.title.text.lower():
            soup = self.loader(path)
            return soup
        else:
            return soup
