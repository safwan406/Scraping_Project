from configparser import ConfigParser

config = ConfigParser()
config.read("Configurations.ini")

server = config.get("Server","kafka_server")

medscape_link = config.get("Medscape", "url")
medscape_pages = config.getint("Medscape", "pages")

medical_news_1 = config.get("Medical_News_Today", "cancer")
medical_news_2 = config.get("Medical_News_Today", "breast_cancer")
medical_news_3 = config.get("Medical_News_Today", "leukemia")

webmd_1 = config.get("Webmd", "cancer")
webmd_pages_1 = config.getint("Webmd", "cancer_pages")
webmd_2 = config.get("Webmd", "breast_cancer")
webmd_pages_2 = config.getint("Webmd", "breast_cancer_pages")
