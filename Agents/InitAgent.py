from .Core import Agent
from typing import Dict, Any


class InitAgent(Agent):
    def __init__(self, model_name:str, prompt:Dict[str,Any]):
        super().__init__(model_name=model_name, prompt=prompt)
        self.columns = ['topic', 'question_type', 'difficulty']

    def fetch_output(self, **kwargs:dict[Any,Any]):
        response: dict = self.generate_response(**kwargs)

        response_body: str = response['text']

        topic_details = []
        for line in response_body.split('\n'):
            topic_details.append([
                j.strip() for j in line.split('-')
            ])

        self.output = topic_details
        # topic_details = [
        #     {'topic':j[1], 'question_type':j[2], 'difficulty':j[3]} for j in topic_details
        # ]
        return topic_details

