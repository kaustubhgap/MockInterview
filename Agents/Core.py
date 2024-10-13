from abc import ABC
from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain
from langchain_core.prompts import PromptTemplate
from typing import Any, Dict

class Agent(ABC):
    def __init__(self, model_name:str, prompt:Dict[str,Any]) -> None:
        self.model_name = model_name
        self.model = ChatOpenAI(model=model_name)
        self.prompt = prompt

    def generate_response(self, **kwargs:Dict[str,Any]) -> Dict[str,Any]:
        response = LLMChain(
                prompt = PromptTemplate(template=self.prompt["prompt"], input_variables=self.prompt["inputs"]),
                llm=self.model).invoke(kwargs)
        return response
    