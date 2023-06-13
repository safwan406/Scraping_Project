from kafka import KafkaProducer
import variables
import json
import time

class Producer():
    """ This class is used to send data to Kafka Producer """

    def __init__(self):
        """ This function is used to create a Producer Instance """

        def __json_serializer(data):
            """ 
            This function is used to create a serialize the data 
            
            Args:
                data (str): data that is sent to Kafak Producer

            Returns:
                serialized data
            """
            
            return json.dumps(data).encode("utf-8")
        
        self.__producer = KafkaProducer(
            # bootstrap_servers = '172.16.19.75:9092',
            bootstrap_servers = variables.server,
            value_serializer = __json_serializer
        )


    def into_kafka(self, data, topic):
        """ 
        This function is used for downstream process 
        
        Args:
            data (dict): data to be pushed into Kafka Topic
            topic (str): name after which topic is to be made
        """

        start_time = time.time()
        self.__producer.send(f'new_{topic}', data)
        stop_time = time.time()
        print(f"Pushed message into {topic}' in {stop_time - start_time} sec")
