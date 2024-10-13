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
3) Decide if you want to ask a followup question or a new question.
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

"input_variables":['job_description','topics','question_history','previous_question','previous_answer', 'current_question']
}
}