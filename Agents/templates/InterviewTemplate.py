Prompts = {"prompt_1":{"prompt":"""###Instruction:
You will conduct an interview for your company.
You have the following tasks:
1) Ask questions one by one to the candidate and allow them to respond.
2) Analyze the response of the candidate and generate feedback. Decide if you need to ask any followup question or ask a new question.
3) Ask the question you have decided.

###Instruction: Look at the job description below and figure out the questions to ask.
###Job Description
{job_description}


###Instruction: Look at the topic below from which you must ask the questions.

|Topic|Thoerical or Implementation Based Questions|Difficulty Out of 10|
{topics}

The current topic is being tested is : {current_topic}

###Interview:
Questions asked so far:
{question_history}
Previous Question: {previous_question}
Previous Answer: {previous_answer}

###Now Do the following:
1) See if there is a previous answer and a question.
2) If yes, analyse the answer and provide bullet list of your feedback. Keep it short and concise for reference of the HR.
3) Decide if you want to ask a followup question or a new question. If the answer seems to miss some details ask a followup. 
4) Ask your question.
5) This is a one hour interview, so make sure to move on to a different topic if you have asked sufficient questions from the current topic.
6) Mention the topic you are going to test in the with the question you are going to ask 
7) If you think we can conclude the interview, set question_type to "greetings".

Format for your output:
{{"feedback":None|string,
"question_type":Literal["followup","new"],
"current_question_topic" : str,
"question":str}}

Now generate your question-
""",

"inputs":['job_description','topics','current_topic','question_history','previous_question','previous_answer']
},

"prompt_2": {"prompt":"""James: Hi Kevin, I need to ask you a favour.
Kevin: Sure James, happy to help.
James: I was in the middle of an interview with candidate for the following job description - 
{job_description}

Kevin: Okay, now how can I help?

James: I need to rush for a personal emergency and would really appreciate if you could continue this interview for me. Here is a list of topic I had decided to touch up on during this interview.
|Domain|Thoerical or Implementation Based Questions|Difficulty Out of 10|
{topics}
-------------------------------------------------------------------------
             
Kevin: This is a good list James, thanks for this.
             
James: This is the conversation history of the interview-
|Domain|Question|
{question_history}
---
The previous topic is being tested is : {current_topic}

This is the Previous Question I had asked: {previous_question}
Intent of the Prrevious Question: {question_intent}
This is the Previous Response from the candidate: {previous_answer}


Please continue this interview for me.
             
Kevin: Sure James, dont worry about the interview, I will take care of it.

James: Great. Please provide the following. Please provide a brief answer:
        1) Did the candidate understand the question correctly and has provided a relevant response?
            - Look at the answer by the candidate
            - Does the answer attend to every component of the question.
            - Even if the answer is factually correct does respond to every component of the question?
        1) Should I ask a followup question or move on to asking the next question or is it the beginning of the interview?
            - Look at the question history for this.
            - Look at the candidates response to assess this.
        2) Tell me how I should respond to the candidate now?
            - If the answer is None, skip this question
            - Check if the candiate answered the question being asked and did he do so accurately and completely.
            - See the level of detail the candidate has provided.
            - Include the next question to ask here if necessary.
        3) Should I move on to the next domain?
            - see the candidates response
            - Look at the Intent of the Previous Question
            - look at the question history and see how many questions have already been asked from one domain.
            - See if the candidate requested to switch the domain for some reason.
        4) What is the intent behind the response you suggest?
            - Would I switch domains if the candidate provides an incorrect response now?
            - Would I switch domain if the candidate is still unfamiliar or unable to answer?
            - How does your response help deciding the next topic or domain?
             
        Please answer the questions above.
        At the end also provide a json that looks like this:
        {{
            "response":Field(type=str, description:Exact response to display to the candidate. I will contain the new question as well.),
            "question_type":Field(type=Literal["followup","new"]),
            "switch_domain":Field(type=Literal["yes","no"]),
            "intent":Field(type=str, description = "Why did you suggest this response, what action should I take based on the answer from the cancdiate to your response")
            "feedback":Field(type=str, decription = "Consise bullet list feedback for the answer")
            
        }}
             
Kevin: """,
# Provide your response as a JSON with the following schema:
"inputs":['job_description','topics','current_topic','question_history','previous_question','question_intent','previous_answer']
}
}


if __name__ == "__main__":
    import os
    import sys

    module_path = os.path.abspath(os.path.join("."))
    sys.path.append(module_path)

    from configparser import ConfigParser

    import InitTemplate

    from Agents import InitAgent
    from Agents.Core import Agent
    from jobs.helpers import convert_to_string

    config = ConfigParser()
    config.read("config.ini")

    os.environ["OPENAI_API_KEY"] = open("api.txt", encoding="UTF-8").read()
    
    JOB_DESCRIPTION_ROOT: str = config["JOB_DESCRIPTIONS"]["url"]
    JOB_DESCRIPTION_FILE: str = config["JOB_DESCRIPTIONS"]["filename"]
    JOB_DESCRIPTION: str = open(
                                os.path.join(JOB_DESCRIPTION_ROOT, JOB_DESCRIPTION_FILE),
                                "r",
                                encoding="UTF-8",
                            ).read()

    model_name = config['MODELS']['init_model']
    
    init_prompt = InitTemplate.Prompts['prompt_1']
    interview_prompt = Prompts["prompt_2"]

    init_agent = InitAgent(model_name=model_name, prompt=init_prompt)

    init_vars = init_agent.fetch_output(job_description=JOB_DESCRIPTION)
    all_topics = convert_to_string(init_vars, connector="|")

    question_history = "|Image Processing and Computer Vision | Can you explain the difference between image classification and object detection in computer vision?|\n \
    |Image Processing and Computer Vision | I understand that image processing isn't your strong suit. Let's shift to another area. Can you explain how you would implement a neural network using PyTorch? What are some of the key components you would focus on?\n \
    |Deep Learning and Neural Networks |I understand that you're not familiar with implementing neural networks in PyTorch. Let's take a step back. Can you explain what a neural network is and describe its basic components?"
    previous_question = "I understand that this might not be your strong suit, but let's try a more basic question. Can you explain what an artificial neuron is and how it functions within a neural network?"
    previous_answer = "Sorry, I am not familiar with this topic"
    question_intent = """To assess the candidate's foundational knowledge of neural networks before deciding to switch domains. If they struggle again, I will consider moving to a different topic."""
    interview_agent = Agent(model_name=model_name, prompt=interview_prompt)

    response = interview_agent.generate_response(job_description=JOB_DESCRIPTION, topics=all_topics, current_topic=init_vars[1][1],
                                      question_history = question_history, previous_question=previous_question, question_intent=question_intent, previous_answer=previous_answer)
    
    print(response['text'])
