from dotenv import load_dotenv
from openai import OpenAI
import os
import json
import time

load_dotenv()

OpenAI_API = os.getenv("AIML_API")

client = OpenAI(
    base_url="https://api.aimlapi.com/v1",
    api_key=OpenAI_API,
)

response = client.chat.completions.create(
    model="google/gemma-3-4b-it",
    messages=[
        {
  "role": "user",
  "content": """write clear 4 test questions about history of Kazakhstan, return it like dict in python, you have to return 3 dictionarys with 4 questions, 16 possible_answers and 4 indexes of correct answers in possible_answers, exactly like in this example
  
    questions = {"question #1": question,"question #2": question,"question #3": question,"question #4": question,}
                
    possible_answers = {"question #1": [answer #1, answer #2, answer #3, answer #4],"question #2": [answer #1, answer #2, answer #3, answer #4],"question #3": [answer #1, answer #2, answer #3, answer #4],"question #4": [answer #1, answer #2, answer #3, answer #4]}
    
    correct_answers = {"question #1": index of correct answer in possible_answer,"question #2": index of correct answer in possible_answer,"question #3": index of correct answer in possible_answer,"question #4": index of correct answer in possible_answer}
    
  """
}
    ],
    temperature=0.1,
    frequency_penalty=1,
    max_tokens=500
)


message = response.choices[0].message.content



mess = message.replace("```","").replace("python","").split("\n\n")
mess1 = []
for dictionary in mess:
    mess1.append(dictionary.replace("\n","").replace("    ",""))

main = []
for i in mess1[:3]:
    main.append(json.loads(i[i.find("{"):]))
    
    

questions = main[0]
answers = main[1]
correct = main[2]



score = 0
for i in range(1,5):
    print(questions[f"Question #{i}"])
    for j,answer in enumerate(answers[f"Question #{i}"]):
        print(f"{j}: {answer}")
    user_answer = int(input("your answer: "))
    if user_answer == correct[f"Question #{i}"]:
        score += 1
        print("Correct")
    else:
        print("Incorrect")
    time.sleep(1)
print(f"your score is {score/4*100}%") 