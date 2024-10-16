import json
from typing import Any, Dict

import regex as re

from .Core import Agent


class QuestionAgent(Agent):
    """
    Agent to generate the next question
    """
    agentType: str = "QuestionAgent"

    def __init__(self, model_name:str, prompt:Dict[str,Any]):
        super().__init__(model_name=model_name, prompt=prompt)

    @staticmethod
    def extract_json_object(text):
        # Define the regex pattern
        pattern = r'json\s*(\{(?:[^{}]|(?R))*\})'
        
        try:
            # Compile the pattern (optional but can improve performance for repeated use)
            regex = re.compile(pattern)
            
            # Search for the pattern in the text
            match = regex.search(text)
            
            if match:
                # Return the JSON object (the part inside the parentheses in the pattern)
                return match.group(1)
            else:
                return "No JSON object found."
        except re.error as e:
            return f"Regex error: {e}"

    def fetch_output(self, **kwargs:dict[Any,Any]) -> dict:
        response: dict = self.generate_response(**kwargs)

        response_body: str = response['text']
        output = self.extract_json_object(response_body)
        output = eval(response_body)
        return output
