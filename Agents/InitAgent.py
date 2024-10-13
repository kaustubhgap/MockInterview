from .Core import Agent
from typing import Dict, Any


class InitAgent(Agent):
    def __init__(self, model_name:str, prompt:Dict[str,Any]):
        super().__init__(model_name=model_name, prompt=prompt)

    def fetch_output(self, **kwargs):
        response: dict = self.generate_response(**kwargs)

        response_body: str = response['text']

        topic_details = []
        for line in response_body.split('\n'):
            topic_details.append([
                j.strip() for j in line.split('-')
            ])

        return topic_details

