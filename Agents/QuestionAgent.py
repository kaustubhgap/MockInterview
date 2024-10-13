from .Core import Agent
from typing import Dict, Any

class QuestionAgent(Agent):
    """
    Agent to generate the next question
    """
    agentType: str = "QuestionAgent"

    def __init__(self, model_name:str, prompt:Dict[str,Any]):
        super().__init__(model_name=model_name, prompt=prompt)