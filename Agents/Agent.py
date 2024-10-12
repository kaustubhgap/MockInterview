from abc import ABC
from langchain_openai import ChatOpenAI
from langchain import PromptTemplate, LLMChain
from typing import Json, Any, Dict

class Agent(ABC):
    def __init__(self, model_name:str, prompt:Json) -> None:
        self.model_name = model_name
        self.model = ChatOpenAI(model=model_name)
        self.prompt = prompt

    def generate_response(self, **kwargs:Dict[str,Any]) -> Dict[str,Any]:
        response = LLMChain(
                prompt = PromptTemplate(template=self.prompt["text"], input_variables=self.prompt["inputs"]),
                llm=self.model).invoke(kwargs)
        return response
    