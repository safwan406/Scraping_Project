from class_soup import Soup
from class_kafka_producer import Producer

class WebMD():
    """ This class is used to scrape data from WebMD """

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
            all = soup.find_all('body')
            content = all[0].find_all('ul',{"class","list"})
            head = content[0].find_all('span',{"class","title"})
            hrefs = content[0].find_all('a')

            for i in range(len(hrefs)):
                link = hrefs[i]['href']
                header = head[i].text
                news = self.article_extracting(link)

                x = {"heading": header, "url": link, "news": news}

                self.__obj_producer.into_kafka(x, 'WebMD')

        except:
            print("error occured")


    def article_extracting(self, path):
        """
        This function is used to extract content from provided URL 
        
        Args:
            path (str): URL to extract data
        
        Returns:
            news (str): scraped article
        """

        extracted_url = self.__obj_soup.soup_maker(path)
        data = extracted_url.find_all('body')
        try:
            news = data[0].find_all('div',{"class","article-page active-page"})[0].text
            news = " ".join(news.split())
        except:
            try:
                news = data[0].find_all('div',{"class","article-content"})[0].text
                news = " ".join(news.split())
            except:
                news = 'empty'
        return news
