import torch
from transformers import pipeline
from class_ner import NER

class Encapsulator():
    """ This class is used to generate summary """

    def __init__(self, model):
        """ 
        This function runs the pre-trained model
        
        Args:
            model (str): name of pre-trained model
        """

        self.summarizer = pipeline(
            "summarization",
            model,
            device = 0 if torch.cuda.is_available() else -1,
        )
        self.obj_ner = NER()

    def summary_generator(self, article):
        """ 
        This function runs a pre-trained model and return the name of diseases from text
        
        Args:
            content (str): scraped article

        Return:
            summary (str): summary of passed content
        """

        result = self.summarizer(article)
        summary = result[0]["summary_text"]
        return summary
