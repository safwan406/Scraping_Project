from configparser import ConfigParser

config = ConfigParser()
config.read("configuration.ini")

address = config.get("Datalake", "address")
port = config.getint("Datalake", "port")

model = config.get("Summary", "model")

bio_nlp = config.get("NER", "bio_nlp")
sci_bert = config.get("NER", "sci_bert")

icd10 = config.get("ICD10", "file")
ndc = config.get("NDC", "file")

uri = config.get("MongoDB", "uri")
db = config.get("MongoDB", "db")
collection = config.get("MongoDB", "collection")

directory1 = config.get("TopicName", "website1")
directory2 = config.get("TopicName", "website2")
directory3 = config.get("TopicName", "website3")