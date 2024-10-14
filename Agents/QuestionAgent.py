from .Core import Agent
from typing import Dict, Any
import json

class QuestionAgent(Agent):
    """
    Agent to generate the next question
    """
    agentType: str = "QuestionAgent"

    def __init__(self, model_name:str, prompt:Dict[str,Any]):
        super().__init__(model_name=model_name, prompt=prompt)

    def fetch_output(self, **kwargs:dict[Any,Any]) -> dict:
        response: dict = self.generate_response(**kwargs)

        response_body: str = response['text']
        output = eval(response_body)
        return output
