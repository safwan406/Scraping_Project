from class_soup import Soup
from class_kafka_producer import Producer

class WebNewsToday():
    """ This class is used to scrape data from Web News Today """

    def __init__(self):
        self.__obj_soup = Soup()
        self.__obj_producer = Producer()

    def url_extracting(self, path):
        """ 
        This function is used to extract data from provided URL 
        
        Args:
            path (str): URL to extract data
        """

        sp = self.__obj_soup.soup_maker(path)
        
        try:
            all = sp.find_all("li", {"class", "css-1ib8oek"})
            itr = len(all)
            # itr = 4
            for i in range(itr):
                link = 'https://www.medicalnewstoday.com' + (str(all[i])).split('href="')[1].split('"')[0]
                news, header = self.article_extracting(link)
                x = {"heading": header, "url": link, "news": news}
                self.__obj_producer.into_kafka(x, 'News_Today')
        except:
            print("error occured")


    def article_extracting(self, path):
        """
        This function is used to extract content from provided URL 
        
        Args:
            path (str): URL to extract data
        
        Returns:
            news (str): scraped article
            header (str): heading of article
        """

        extracted_url = self.__obj_soup.soup_maker(path)

        try:
            news = extracted_url.find_all("article", {"class", "article-body css-d2znx6 undefined"})[0].text
            news = " ".join(news.split())
            header = extracted_url.find_all("h1", {"class", "css-0"})[0].text
        except:
            try:
                news = extracted_url.find_all("article", {"class", "article-body css-d2znx6 css-16tt818"})[0].text
                news = " ".join(news.split())
                header = extracted_url.find_all("h1", {"class", "css-0 css-16tjikm"})[0].text
            except:
                news = 'empty'
                header = 'empty'

        return news, header
