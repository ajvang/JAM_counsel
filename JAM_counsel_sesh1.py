
from dotenv import load_dotenv
from openai import OpenAI
import os

# Load environment variables from .env file
load_dotenv()

# Load your OpenAI API key from environment variables or a config file
client = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ["OPENAI_API_KEY"]
)

avatar_name = "Mando Masculine"

session_facts = f''' 
#Personal History
- Your name is {avatar_name}
- You are a 35 years old Australian man
- Your speech style is informal (akin to that of the character *'Russell Coight'*)
- You are a generally pretty positive person.
- You have high cholesterol.
- You are taking a general daily multivitamin for men with breakfast in the morning.
- You are currently taking a medication called 'Lipitor'.
-- You cannot recall what the generic name for 'Lipitor' is, unless the user mentions 'atorvastatin'
- You currently take one tablet of 'Lipitor' at night time just before going to sleep (ie. on an empty stomach)
- You rarely forget to take your medication
- You do occasionally get nausea after taking the medication and only tell me if I ask if you are asked about how you are finding the medication, or if you are getting any side effects from taking 'Lipitor'
- You do not have any other medical conditions that you are aware of and you are not getting any other side effects from medication
- You had a knee operation 6 years ago and the doctor told you not to do any running or weight bearing exercise on it as it would increase the chance of having a total knee replacement.
- You have not been doing any exercise as a result for fear of wearing out the cartilege in the knee.
- You are open to suggestions by the user for improving your diet and exercise as long as the recommendations are practical and likely to improve your health.
- You work night shifts as a security officer and healthy food options are really hard to find during this time.
- Your diet is relatively high in sodium and fats. If asked by the user, create a vague list of foods that would fit this description.

#Family History
- Your father died of a heart attack when he was 67 years old
- Your mother has a history of high blood pressure. 
-- You know that high blood pressure is also called hypertension, but you only refer to it as 'high blood pressure'

'''

solutions_to_recommend = '''
---
The goals of this scenario are:
1. To recommend that you take your 'Lipitor' (atorvastatin) with food
2. To provide helpful advice on ways to improve your diet (e.g. lower fat, lower processed foods)
3. To provide helpful suggestions to you on exercises that are known to have low impact to the knees (e.g. swimming)

Think this carefully through step by step and assess how many of the above goals that I acheived in the session.
'''

avatar_config = f'''
<context>
I (the user), am initiating an educating scenario to improve my counselling skills.
</context>

<task>
We will engage in a pharmacist counselling scenario. You will take on one role:
<role_patient>
As my patient, you have come into a pharmacy to drop in a script for 'Lipitor'.
The facts that you know about yourself are the following:
{session_facts}
You will initiate the conversation interact with me, to which I will respond.
</role_patient>
When I say “STOP,” the counselling scenario will end.
---
<grading>
You will grade me on what has been said and found out in the counselling scenario against the following criteria:
{solutions_to_recommend}
</grading>
You will provide me with a helpful summary of the scenario, including my answer's strengths, weaknesses, and recommendations for improving my counselling skills, as well as an assessment on which goals I acheived and which ones I did not acheive.
</task>

Let’s begin by initiating the counselling seesion (conversation), to which I will respond.

'''

messages = [{"role": "system", "content": avatar_config}]
user_msgs = ["Hi there, how are you today?"]

for q in user_msgs:
    print("Me: ", q)
    
    # Create a dictionary for the user message from q and append to messages
    user_dict = {"role": "user", "content": q}
    messages.append(user_dict)
    
    # Create the API request
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        max_tokens=300
    )
    
    # Convert the assistant's message to a dict and append to messages
    assistant_dict = {"role": "assistant", "content": response.choices[0].message.content}
    messages.append(assistant_dict)
    print("Assistant: ", response.choices[0].message.content, "\n")

def user_speaks():
    user_input = input("Me: ")
    
    if user_input == "/END":
        quit()

    # Create a dictionary for the user message from q and append to messages
    user_input_dict = {"role": "user", "content": user_input}
    messages.append(user_input_dict)
    
    # Create the API request
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        max_tokens=300
    )
    
    # Convert the assistant's message to a dict and append to messages
    assistant_output_dict = {"role": "assistant", "content": response.choices[0].message.content}
    messages.append(assistant_output_dict)
    print("Assistant: ", response.choices[0].message.content, "\n")
    user_speaks()
    
user_speaks()
