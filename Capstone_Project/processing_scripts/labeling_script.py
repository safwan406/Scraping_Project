import multiprocessing
import variables
from class_datalake import Datalake
from configparser import ConfigParser
from class_ner import NER
from class_icd import ICD
from class_database import Mongo
from class_ndc import NDC
import time

config = ConfigParser()
config.read("Configurations.ini")

diagnosticObj = ICD(variables.icd10)
dbObj = Mongo(variables.uri, variables.db, variables.collection)
prescriptionObj = NDC(variables.ndc)

def creating_codes(diseases):
    """ 
    This creates codes against parsed disease names 
    
    Args: 
        diseases (str): name of disease against which codes need to be extracted

    Returns:
        codes (list): list of ICD10 codes
        descriptions (list): list of description of codes
    """
    
    codes = []
    descriptions = []
    for disease in diseases:
        codes = codes + diagnosticObj.classifier_for_code(disease)
        codes = list(dict.fromkeys(codes))
        descriptions = descriptions + diagnosticObj.classifier_for_description(disease)
        descriptions = list(dict.fromkeys(descriptions))
    return codes, descriptions


def labelling(name):
    """ 
    This function is used to label the scraped data 
    
    Args:
        name(str): name of directory from which data is to be read
    """

    lakeObj = Datalake()
    nerObj = NER(variables.bio_nlp)
    data = lakeObj.reader(name) # ==> reading data from rawzone
    startTime = time.time()
    if data != None:
        length = len(data)
        for index in range(length):
            data[index]['diseases'] = nerObj.named_entity_recognizing(data[index]['news'])
            data[index]['ICD10'], data[index]['ICD10_Description'] = creating_codes(data[index]['diseases'])
            data[index]['NDC'], data[index]['product'] = prescriptionObj.classifier_for_code(data[index]['news'].lower())
            dbObj.update(data[index])
        
    else:
        print("Path was not found!")
    elapesedTime = time.time() - startTime
    print(f"Time required for computation was {elapesedTime/60} min")


if __name__ == "__main__":
    t1 = multiprocessing.Process(target = labelling, args = (variables.directory1,), name = 't1')
    t2 = multiprocessing.Process(target = labelling, args = (variables.directory2,), name = 't2')
    t3 = multiprocessing.Process(target = labelling, args = (variables.directory3,), name = 't3')

    t1.start()
    t2.start()
    t3.start()

    t1.join()
    t2.join()
    t3.join()
