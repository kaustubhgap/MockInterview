from abc import ABC
from typing import Any, Dict

from langchain.chains import LLMChain
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI


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


if __name__ == "__main__":
    import os
    from configparser import ConfigParser

    from Agents.templates import InterviewTemplate as IT
    
    config = ConfigParser()
    config.read("config.ini")

    os.environ["OPENAI_API_KEY"] = open("api.txt", encoding="UTF-8").read()
    
    model_name = config['MODELS']['init_model']

    prompt = IT['prompt_2']
    
    while True:
        agent = Agent(model_name=model_name, prompt=prompt)
        response = agent.generate_response()
        print(response)
        prompt['prompt'] += response['text'] + "\n\n"
        user_response = input("please provide the answer:")
        prompt['prompt'] += "\nCandidate: " + user_response + "\n\nInterviewer: "

        print(prompt['prompt'])