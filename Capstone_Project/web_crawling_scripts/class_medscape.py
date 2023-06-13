from class_soup import Soup
from class_kafka_producer import Producer


class WebMedscape():
    """ This class is used to scrape data from Web Medscape """
    
    def __init__(self):
        self.__obj_soup = Soup()
        self.__obj_producer = Producer()
    
    def url_extracting(self, path):
        """ 
        This function is used to extract data from provided URL 
        
        Args:
            path (str): URL to extract data
        """

        soup = self.__obj_soup.soup_maker(path)
        
        try:
            all = soup.find_all("a", {"class", "title"})

            for i in range(len(all)):
                link = "https://" + (str(all[i]).split('href="//')[1]).split('">')[0]
                news, header = self.article_extracting(link, all[i])

                x = {"heading": header, "url": link, "news": news}

                self.__obj_producer.into_kafka(x, 'Medscape')
        except:
            print("error occured")


    def article_extracting(self, path, element):
        """
        This function is used to extract content from provided URL and tag
        
        Args:
            path (str): URL to extract data
            element (bs4.element.Tag): tag in which data is to be extracted
        
        Returns:
            news (str): scraped article
            header (str): heading of article
        """

        extracted_url = self.__obj_soup.soup_maker(path)

        try:
            header = element.text
            news = extracted_url.find_all("div", {"class", "article-content-wrapper"})[0].text.split("Credit")[0]
            news = " ".join(news.split())

        except:
            news = 'empty'
            header = element.text
        
        return news, header
