Prompts = \
{"prompt_1":
    {"prompt" : """###INSTRUCTION:
You are the Vice Precident of Talent Acquisition department. You have to guide the team of interviewers the topics to be covered during the interview.

###INSTRUCTION:
Read the job description below and carefully look at the desgination and the domain of the job.
Now suggest the Topics to be covered during the interview.
Also suggest the type of questions, "Theoretical" or "Implemation Based" should be asked.
Carefully look the number of years of experience required from the job and suggest the appropriate difficulty for each topic on a scale of 1 to 10.

Job Description
{job_description}

### INSTRUCTION
Now carefully create an output that contains the TOPICS TO BE COVERED, THEOERETICAL/IMPLEMENTATION BASED, DIFFICULTY[1 to 10].
Create 5 topics.
Use the format below:
<TOPIC NUMBER>-<TOPIC>-<THOERICTICAL/IMPLEMENTATION BASED question type>-<DIFFICULTY>
One line for each topic.
JUST PRODUCE THE OUTPUT AND NOTHING ELSE.
""",
"inputs":["job_description"]}
}