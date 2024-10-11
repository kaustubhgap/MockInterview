from langchain import PromptTemplate, LLMChain
from Bots.templates import ExtractTopicsTemplate2 as et
from Bots.templates import InterviewTemplate as it
import regex as re
import json


class DataScience(object):
    class PromptInstructionType1():
        def __init__(self):
            self.prompt = et.prompt_instruction_type_1['prompt']
            self.inputs = et.prompt_instruction_type_1['input_variables']
            self._called = False
            self._response = None

        def __call__(self, llm, **input_kwargs):
            response = LLMChain(
                prompt = PromptTemplate(template=self.prompt, input_variables=self.inputs),
                llm=llm).invoke(input_kwargs)
            self._called = True
            self._response = response
            return response
            

        def extract_response(self):
            if self._response:

                lines = self._response['text'].split("\n")
                lines = [
                    re.split(string=j.strip(), pattern=r"[ ]*-[ ]*")
                             for j in lines]

                return lines


class Interviewer(object):
    class FirstInterviewer():
        def __init__(self):
            self.prompt = it.ask_question_1['prompt']
            self.inputs = it.ask_question_1['input_variables']
            self._called = False
            self._response = None
        
        def __call__(self, llm, **input_kwargs):
            response = LLMChain(
                prompt = PromptTemplate(template=self.prompt, input_variables=self.inputs),
                llm=llm).invoke(input_kwargs)
            self._called = True
            self._response = response
            return response
        
        def extract_response(self, llm=None):
            try:
                return json.loads(self.response)
            except:
                return None