from langchain import PromptTemplate, LLMChain
from Bots.templates import ResponseTemplate as rt


class AnsweringBot(object):
    class AnsweringBot1():
        def __init__(self):
            self.prompt = rt.answer_template_1['prompt']
            self.inputs = rt.answer_template_1['input_variables']
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
            pass
