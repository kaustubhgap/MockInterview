import os
from configparser import ConfigParser
import json
from json import JSONDecodeError
from shutil import rmtree

config = ConfigParser()
config.read("config.ini")

ROOT_DIR:str = config["USERDB"]["url"]
USER_MAP:str = config["USERDB"]["users_hash"]
SESSION_MAP:str = config["USERDB"]["sessions_hash"]


class Logger(object):
    def __init__(self, root_dir) -> None:
        self.root_dir:str = root_dir
        
    
    def instantiate(self, user_id, session_id):
        self.create_user(user_id)
        self.create_session(user_id, session_id)


    @staticmethod
    def read_json(file: str) -> dict:
        try:
            with open(file, 'r') as f:
                current_users:dict = json.load(f)
        except JSONDecodeError:
             current_users:dict = {}

        return current_users
    
    
    @staticmethod
    def write_json(data:dict, file: str) -> dict:
        with open(
                os.path.join(ROOT_DIR, USER_MAP),
                "w"
            ) as f:
                json.dump(data, f)
    

    def create_session(self, user_id, session_id) -> None:

        user_sessions:dict = self.read_json(os.path.join(ROOT_DIR, self.user_hash[user_id], SESSION_MAP))
        
        # if session id already being tracked do nothing
        if session_id not in user_sessions:
            # add current session id to the sessions
            user_sessions[session_id] = f'{session_id}.json'
            
            # dump the latest session_hash for the user
            with open(
                os.path.join(ROOT_DIR, self.user_hash[user_id], SESSION_MAP),
                'w') as f:
                json.dump(user_sessions, f)
            open(os.path.join(ROOT_DIR, self.user_hash[user_id], user_sessions[session_id]),
                'w')

        self.user_sessions = user_sessions

        self.current_session = self.read_json(os.path.join(ROOT_DIR, self.user_hash[user_id], self.user_sessions[session_id]))
        

    def create_user(self, user_id) -> None:
        
        # fetch the current users from a json file
        current_users:dict = self.read_json(os.path.join(ROOT_DIR, USER_MAP))

        # if user already exists, do nothing
        if user_id not in current_users:
            # add the path of the sessions for the new user
            current_users[user_id] = user_id
            self.write_json(current_users, os.path.join(ROOT_DIR, USER_MAP))

            # create a new location for the user
            os.mkdir(os.path.join(ROOT_DIR, user_id))
            # create the sessions mapping file for the new user
            open(os.path.join(ROOT_DIR,user_id,f"{SESSION_MAP}"), "w")
            
        self.user_hash = current_users

    
    def update_session(self,*keys, value):
        session = self.current_session.copy()
        head = session
        for key in keys[:-1]:
            if key in session:
                session = session[key]

            else:
                session[key] = {}
                session = session[key]
        session[keys[-1]] = value

        self.current_session = head
    
    
    def remove_user(self, user_id=None) -> None:
        user_hash = self.read_json(os.path.join(ROOT_DIR, USER_MAP))

        if user_id in user_hash:
            user_dir =  user_hash[user_id]
            del user_hash[user_id]

            self.write_json(user_hash, os.path.join(ROOT_DIR, USER_MAP))
            rmtree(os.path.join(ROOT_DIR, user_dir))


if __name__ == "__main__":
    user_id = input("enter your username: ")
    session_id = input("enter the session id: ")
    logger = Logger(root_dir = ROOT_DIR)
    logger.instantiate(user_id=user_id, session_id=session_id)
    logger.update_session("domain", value="data science")
    logger.update_session("topics", value=["lr", "dl", "ai"])
    logger.update_session("interview","question", "question_text", value="what is linear regression")
    print(logger.current_session)
    move = input(":")
    logger.remove_user("kaustubh")