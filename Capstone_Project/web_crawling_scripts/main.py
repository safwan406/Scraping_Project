import variables
from class_news_today import WebNewsToday
from class_medscape import WebMedscape
from class_webmd import WebMD
import multiprocessing
import os


obj1 = WebNewsToday()
obj2 = WebMedscape()
obj3 = WebMD()

def news_today_crawler(path):
    """ 
        This function is used to extract data from provided URL 
        
        Args:
            path (str): URL to extract data
    """
    
    print('process id:', os.getpid())
    obj1.url_extracting(path)
    print(path)


def medscape_crawler(path):
    """ 
        This function is used to extract data from provided URL 
        
        Args:
            path (str): URL to extract data
    """

    print('process id:', os.getpid())
    for i in range(variables.medscape_pages):
        main_site = path + f'{i}'
        obj2.url_extracting(main_site)
        print(main_site)


def webmd_crawler(path, pages):
    """ 
        This function is used to extract data from provided URL 
        
        Args:
            path (str): URL to extract data
            pages (int): page number of website to which data needs to be scraped
    """

    print('process id:', os.getpid())
    for i in (page + 1 for page in range(pages)):
        main_site = path + f'{i}'
        obj3.url_extracting(main_site)
        print(main_site)


if __name__ == "__main__":
    t1 = multiprocessing.Process(target = medscape_crawler, args = (variables.medscape_link,), name = 't1')
    t2 = multiprocessing.Process(target = news_today_crawler, args = (variables.medical_news_1,), name = 't2')
    t3 = multiprocessing.Process(target = news_today_crawler, args = (variables.medical_news_2,), name = 't3')
    t4 = multiprocessing.Process(target = news_today_crawler, args = (variables.medical_news_3,), name = 't4')
    t5 = multiprocessing.Process(target = webmd_crawler, args = (variables.webmd_1, variables.webmd_pages_1,), name = 't5')
    t6 = multiprocessing.Process(target = webmd_crawler, args = (variables.webmd_2, variables.webmd_pages_2,), name = 't6')
    
    t1.start()
    t2.start()
    t3.start()
    t4.start()
    t5.start()
    t6.start()

    t1.join()
    t2.join()
    t3.join()
    t4.join()
    t5.join()
    t6.join()

    # all processes finished 
    print("All processes finished execution!")
