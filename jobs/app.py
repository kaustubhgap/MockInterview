import os
import sys

module_path = os.path.abspath(os.path.join('.'))
sys.path.append(module_path)

os.environ['OPENAI_API_KEY'] = open('api.txt').read()

from Agents import InitAgent, QuestionAgent, ResponseAgent
from Agents.templates import InitTemplate, InterviewTemplate, ResponseTemplate
from Logger import Logger

from helpers import make_token, convert_to_string, speak
from configparser import ConfigParser

from datetime import datetime

import pyttsx3
import whisper
import pyaudio
import numpy as np
import torch
from load_whisper import transcribe, load_stt

config = ConfigParser()
config.read("config.ini")

# setup variables for db path
ROOT_DIR:str = config["USERDB"]["url"]
USER_MAP:str = config["USERDB"]["users_hash"]
SESSION_MAP:str = config["USERDB"]["sessions_hash"]

# setup variables for job description path
JOB_DESCRIPTION_ROOT: str = config["JOB_DESCRIPTIONS"]["url"]
JOB_DESCRIPTION_FILE: str = config["JOB_DESCRIPTIONS"]["filename"]

# setup variables for prompt path
PROMPT_ROOT: str = config["PROMPTS"]["url"]
INIT_PROMPT_NAME: str = config["PROMPTS"]["init_prompt"]
INTERVIEW_PROMPT_NAME: str = config["PROMPTS"]["interview_prompt"]
RESPONSE_PROMPT_NAME: str = config["PROMPTS"]["response_prompt"] # temporary to mimic human

# model names
INIT_MODEL_NAME: str =  config["MODELS"]["init_model"]
QUESTION_MODEL_NAME: str =  config["MODELS"]["question_model"]

# load prompts and a job description
JOB_DESCRIPTION: str = open(os.path.join(JOB_DESCRIPTION_ROOT, JOB_DESCRIPTION_FILE), 'r').read()
INIT_PROMPT: str = InitTemplate.Prompts[INIT_PROMPT_NAME]
INTERVIEW_PROMPT: str = InterviewTemplate.Prompts[INTERVIEW_PROMPT_NAME]
RESPONSE_PROMPT: str = ResponseTemplate.Prompts[RESPONSE_PROMPT_NAME] # temporary to mimic human

# load STT parameters
STT_MODEL_PATH: str = config["TEXT_TO_SPEECH"]["model_path"]
STT_FS: int = int(config["TEXT_TO_SPEECH"]["fs"])
STT_CHUNK: int = int(config["TEXT_TO_SPEECH"]["chunk"])
STT_SECONDS: int = int(config["TEXT_TO_SPEECH"]["seconds"])

stt_model = load_stt(STT_MODEL_PATH)

# setup TTS engine
TTS_ENGINE = pyttsx3.init()
# Set properties (optional)
TTS_ENGINE.setProperty('rate', 150)    # Speed of speech
TTS_ENGINE.setProperty('volume', 1)

if __name__ == "__main__":
    # get username
    # USERNAME: str = input("Please enter your username: ")
    USERNAME = "kaustubh"
        
    # fetch session id
    SESSION_ID: str = make_token()

    # SESSION_ID = "fhXwAcd7SqVWz-clgx5Kbw"

    interview = {}
    interview['start_time'] = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    interview['conversation'] = []

    # setup logger
    logger = Logger(root_dir = ROOT_DIR)
    logger.instantiate(user_id=USERNAME, session_id=SESSION_ID)

    # setup init_agent
    init_agent = InitAgent(model_name=INIT_MODEL_NAME, prompt=INIT_PROMPT)
    question_agent = QuestionAgent(model_name=QUESTION_MODEL_NAME, prompt=INTERVIEW_PROMPT)

    # setup answer agent: temporary to mimic a candidate
    answer_agent = ResponseAgent(model_name=QUESTION_MODEL_NAME, prompt=RESPONSE_PROMPT)

    # init variables
    init_vars = init_agent.fetch_output(job_description=JOB_DESCRIPTION)
    logger.update_session('init_vars', 'topics', value = init_vars)

    # all topics: used in the interview prompt
    all_topics = convert_to_string(init_vars, connector="|")
    all_topics = "|" + all_topics

    question_number = 1
    question_history = ''
    previous_question = 'None'
    previous_answer = 'None'
    
    conversation = interview['conversation']
    topics = []
    # chatbot flow: S1
    for init_var in init_vars:
        # new topic available : YES
        topic_conversation = {}

        current_topic = init_var[1]
        current_question_type = init_var[2]
        current_difficulty = init_var[3]

        
        topic_conversation['topic_name'] = current_topic
        topic_conversation['start_time'] = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        topic_conversation['questions'] = []
        questions = topic_conversation['questions']

        # chatbot flow: S2
        while True:
            question_count = len(questions)
            generated_question = question_agent.fetch_output(job_description=JOB_DESCRIPTION, 
                                                              topics=all_topics,
                                                              current_topic=current_topic,
                                                              question_history=question_history,
                                                              previous_question=previous_question,
                                                              previous_answer=previous_answer
                                                              )
            
            current_question_dict = {'question':{}}
            current_question_dict['start_time'] = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
            current_question_dict['question']['start_time'] = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")

            current_question = generated_question['question']
            current_feedback = generated_question['feedback']
            current_question_type = generated_question['question_type']
            switch_topic = generated_question['switch_topic']

            user_preference = input(f"Current topic being questioned is {current_topic}.\nDo you wish to continue with the same topic or switch to a different one?") if question_count else switch_topic
            if user_preference.lower() == "yes":
                break

            question_history += f"{current_topic} - {current_question}\n"
            current_question_dict['question']['text'] = current_question
            current_question_dict['question']['type'] = current_question_type
            current_question_dict['question']['end_time'] = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
            print("feedback",current_feedback)
            print("\n")
            print("next_question",current_question)
            print("\n")

            current_question_dict['answer'] = {}
            current_question_dict['answer']['start_time'] = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
            # generated_answer = answer_agent.fetch_output(job_description=JOB_DESCRIPTION,
            #                                                   question=current_question)

            speak(current_question, engine=TTS_ENGINE)
            answer_transcript = transcribe(stt_model)
            print(answer_transcript)
            generated_answer = {'answer':answer_transcript}
            print("my answer", generated_answer['answer'])

            current_answer = generated_answer['answer']
            current_question_dict['answer']['text'] = current_answer
            current_question_dict['answer']['end_time'] = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")

            previous_question = current_question
            previous_answer = current_answer
            
            if len(questions):
                questions[-1]['feedback'] = current_feedback
            print("current topic: ", current_topic)
            questions.append(current_question_dict)
            
        conversation.append(topic_conversation)

    logger.update_session("interview", value=interview)
    print("Thanks for interviewing")