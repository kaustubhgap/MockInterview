from .Core import Agent
from typing import Dict, Any

class FeedbackBot(Agent):
    def __init__(self, model_name:str, prompt:Dict[str,Any]):
        super().__init__(model_name=model_name, prompt=prompt)