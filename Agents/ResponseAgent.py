from .Core import Agent
from typing import Dict, Any

class ResponseAgent(Agent):
    def __init__(self, model_name:str, prompt:Dict[str,Any]) -> None:
        super().__init__(model_name=model_name, prompt=prompt)
    
    def fetch_output(self, **kwargs:Dict[Any,Any]) -> Dict:
        response: Dict = self.generate_response(**kwargs)

        response_body: str = response['text']
        output: Dict = eval(response_body)
        return output


if __name__ == "__main__":
    pass