import json
import requests
import os
import json
from keys import *
from config import *
os.environ["TOKENIZERS_PARALLELISM"] = "false"

# Readme: This script will create pairs for the collected paragraphs and label them for finetuning.
# Outputs a structured_dataset.json

# Dataset format:
# instruction - what the llm needs to perform
# input - what we input to the llm during inference
# output - what the llm should respond

# Point to the collected text ("the output")
text_path = r"C:\Users\ohakimu\OneDrive - Perkins and Will\Desktop\IAAC\Semester 3\Gen AI\LLM\LLM-Finetuning\dataset\summary_text.txt"

# Define the LLM task (the "instruction")
instruction = "Further develop the concept for the restaurant by developing a detailed description of the restaurant."

# Define the LLM task
task = (
    "You are an API that converts bodies of text into a single instruction object. "
    "Each JSON should include only an 'instruction' field. "
    "Create an instruction asking for the design of a restaurant, framing your instruction in such a way that it relates to the idea behind the concept of the restaurant. "
    "You should only fill in the instruction field with one sentence and it should begin in this format: 'Imagine a restaurant that...' "
    "Never directly refer to the name of the restaurant or specific details of the context of the design in your instruction. "
    "Only respond in the JSON format and no additional text.\n"
)

# Get instruction pair from LLM (the "input")
def generate_completion(task, paragraph):
    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
        {"role": 
            "system", 
            "content": task},
        {"role": 
            "user", 
            "content": paragraph}
        ],
        temperature=1.0,
        response_format={ "type": "json_object" },
        )
    result = response.choices[0].message.content
    return result

def is_json(data):
    try:
        json.loads(data)
        return True
    except ValueError:
        return False

# Check if the answer is a JSON object
def get_completion(task, paragraph):
        try:
            # print(f"TASK: \n{task}")
            # print(f"PARAGRAPH: \n{paragraph}")
            response = generate_completion(task, paragraph)
            if is_json(response):
                print(response)
                return json.loads(response)
            else:
                print(f"Request failed. Skipping this chunk.")
        except requests.exceptions.RequestException as e:
            return None

# Run
# Get our collected text
with open(text_path, 'r', encoding='latin-1') as file:
    summaries = file.read()

# Send each paragraph to the LLM to get the paired response
paragraphs = summaries.split('\n\n')
responses = []
for idx, paragraph in enumerate(paragraphs):
    response = get_completion(task, paragraph)
    print(f"{idx + 1}/{len(paragraphs)}")
    if response is not None:
        # Assemble into the right json format
        paired_response = {
            "instruction": instruction,
            "input": response['instruction'],
            "output": paragraph
        }
        responses.append(paired_response)

# Export JSON file
outpath = r'C:\Users\ohakimu\OneDrive - Perkins and Will\Desktop\IAAC\Semester 3\Gen AI\LLM\LLM-Finetuning\dataset\structured_dataset.json'
with open(outpath, 'w', encoding='utf-8') as f:
    json.dump(responses, f, indent=2, ensure_ascii=False)

print(f"Saved {outpath} containing {len(responses)} training examples.")
