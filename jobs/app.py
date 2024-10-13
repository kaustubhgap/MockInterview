import os
import sys

module_path = os.path.abspath(os.path.join('.'))
sys.path.append(module_path)

os.environ['OPENAI_API_KEY'] = open('api.txt').read()

from Agents import InitAgent, QuestionAgent
from Agents.templates import InitTemplate, InterviewTemplate
from Logger import Logger

from helpers import make_token
from configparser import ConfigParser

config = ConfigParser()
config.read("config.ini")

USERNAME: str = input("Please enter your username: ")
SESSION_ID: str = make_token()

ROOT_DIR:str = config["USERDB"]["url"]
USER_MAP:str = config["USERDB"]["users_hash"]
SESSION_MAP:str = config["USERDB"]["sessions_hash"]

JOB_DESCRIPTION_ROOT: str = config["JOB_DESCRIPTIONS"]["url"]
JOB_DESCRIPTION_FILE: str = config["JOB_DESCRIPTIONS"]["filename"]

PROMPT_ROOT: str = config["PROMPTS"]["url"]
INIT_PROMPT_NAME: str = config["PROMPTS"]["init_prompt"]
INTERVIEW_PROMPT_NAME: str = config["PROMPTS"]["interview_prompt"]

INIT_MODEL_NAME: str =  config["MODELS"]["init_model"]
QUESTION_MODEL_NAME: str =  config["MODELS"]["question_model"]

JOB_DESCRIPTION: str = open(os.path.join(JOB_DESCRIPTION_ROOT, JOB_DESCRIPTION_FILE), 'r').read()
INIT_PROMPT: str = InitTemplate.Prompts[INIT_PROMPT_NAME]
INTERVIEW_PROMPT: str = InterviewTemplate.Prompts[INTERVIEW_PROMPT_NAME]

if __name__ == "__main__":
    
    logger = Logger(root_dir = ROOT_DIR)
    logger.instantiate(user_id=USERNAME, session_id=SESSION_ID)

    init_agent = InitAgent(model_name=INIT_MODEL_NAME, prompt=INIT_PROMPT)
    question_agent = QuestionAgent(model_name=QUESTION_MODEL_NAME, prompt=INTERVIEW_PROMPT)

    init_vars = init_agent.fetch_output(job_description=JOB_DESCRIPTION)
    
    
