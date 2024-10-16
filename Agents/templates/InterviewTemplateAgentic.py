JUDGE_ANSWER = {"PROMPT":\
"""###INSTRUCTIONS
You are judging a candidate sitting for an interview.

STEPS TO PERFORM:
1. Assess the conversation history.
2. Read the the answer provided to the current question.

CONVERSATION HISTORY:
{conversation_history}

CURRENT QUESTION: 
{current_question}
CURRENT ANSWER:
{current_answer}

Now provide a feedback for the answer in the following format:
{{"feedback":<your feedback>}}

- The feedback should be consise bullet points.
- If the CURRENT_ANSWER does not contain any information, put "REPEAT QUESTION" in the feedback so that i can repeat the question.

Remember, based on your feedback I will decide what should be the next question to be asked.
If you think there are some points missing from the answer, mention it in the feedback.
"""}

ASK_QUESTION = {}

DECIDE_QUESTION_TYPE = {}

DECIDE_NEXT_TOPIC = {}

