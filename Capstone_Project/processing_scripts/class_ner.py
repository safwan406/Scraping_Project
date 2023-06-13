from transformers import pipeline
import unicodedata
import time

class NER():
    """ This class is used to extract disease names """

    def __init__(self, model):
        """ 
        This function runs the pre-trained model
        
        Args:
            model (str): name of pre-trained model
        """
        
        PRETRAINED = model
        self.__ner = pipeline(task="ner", model=PRETRAINED, tokenizer = PRETRAINED)


    def named_entity_recognizing(self, content):
        """ 
        This function runs a pre-trained model and return the name of diseases from text
        
        Args:
            content (str): scraped article

        Return:
            diseases (list): list of extracted diseases
        """
        
        startTime = time.time()
        key_words = self.__ner(content, aggregation_strategy="first") # ==> ner
        diseases = set()
        for index in range(len(key_words)):
            if key_words[index]['score'] >= 0.75:
                word = self.pruning(key_words[index]['word'])
                if len(word) == 0:
                    continue
                if 'cancer' in word or 'cancers' in word:
                    diseases.add(word)
                    word = self.phrasing(word)
                diseases.add(word)
        stopTime = time.time()
        elapsedTime = stopTime -startTime
        print(f'Time for extraction is {elapsedTime} sec')
        return list(diseases)


    def pruning(self, words):
        """ 
        This function is used to clean the extracted text
        
        Args:
            words (str): extracted words by running the model

        Return:
            cleaned_word (str): removing any punctuation and extra spaces
        """

        cleaned_word = unicodedata.normalize("NFKD", words)
        cleaned_word = cleaned_word.replace('disease', '')
        cleaned_word = cleaned_word.replace('diseases', '')
        cleaned_word = " ".join(cleaned_word.split())
        cleaned_word = cleaned_word.split('"')[0].split('.')[0].split(',')[0].split(';')[0].split(':')[0].lower()

        return cleaned_word


    def phrasing(self, words): # ==> for cancer only
        """ 
        This function is used to rephrase the word cancer
        
        Args:
            words (str): words that contain cancer

        Return:
            b (str): replaced word cancer with malignant neoplasm
        """

        if len(words.split()) > 1:
            splitedWord = words.split()
            for word in splitedWord:
                if 'cancer' in word:
                    replacedWord = word.replace("cancers", "cancer").replace("cancer", "malignant neoplasm")
            newWord = replacedWord + ' of ' + splitedWord[-2]
        else:
            newWord = "malignant neoplasm"
        return newWord
