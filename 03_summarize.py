import os
from openai import OpenAI
from keys import OPENAI_API_KEY  # Ensure keys.py contains OPENAI_API_KEY variable

# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

os.environ["TOKENIZERS_PARALLELISM"] = "false"

# Readme: This script will take a clean_text.txt and create summaries of each paragraph.
# It will output a summary_text.txt

# Input
clean_text = r"C:\Users\ohakimu\OneDrive - Perkins and Will\Desktop\IAAC\Semester 3\Gen AI\LLM\LLM-Finetuning\dataset\clean_text.txt"

# Define the LLM task
task = ("You are an API that converts bodies of text into a single summary paragraph. "
        "Create a brief summary paragraph for a restaurant based on the provided review text. "
        "Reference key aspects such as the cuisine, atmosphere, service quality, notable dishes, location, and overall dining experience, etc. "
        "Capture the essence of the reviewer's opinion and highlight any unique features or concepts behind the restaurant's design and culinary approach. "
        "You should only respond with a summary paragraph and no additional text.")

# Get summaries from LLM
def generate_summary(task, chunk):
    response = client.completions.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": task},
            {"role": "user", "content": chunk}
        ],
        temperature=1.0,
    )
    
    result = response.choices[0]['message']['content']
    return result

# Run
with open(clean_text, 'r', encoding='utf-8') as file:  # Specify encoding
    content = file.read()

# Split into paragraphs
paragraphs = content.split('\n\n')

# Send to be summarized
summaries = []
for idx, chunk in enumerate(paragraphs):
    summary = generate_summary(task, chunk)
    print(f"{idx + 1}/{len(paragraphs)}")  # Properly format progress display
    if summary is not None:
        summaries.append(summary)
        print(summary)

# Export to txt file
output_file = r'C:\Users\ohakimu\OneDrive - Perkins and Will\Desktop\IAAC\Semester 3\Gen AI\LLM\LLM-Finetuning\dataset\summary_text.txt'
with open(output_file, 'w', encoding='utf-8') as file:  # Specify encoding
    for content in summaries:
        file.write(content + '\n\n')

print(f"Finished summarization, saved {output_file}.")
