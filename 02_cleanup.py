import os

# Path to the .txt files
directory = r'C:\Users\ohakimu\OneDrive - Perkins and Will\Desktop\IAAC\Semester 3\Gen AI\LLM\LLM-Finetuning\scrape_data'
txt_files = [filename for filename in os.listdir(directory) if filename.endswith('.txt')]

# Choose how many projects to use for finetuning
txt_files = txt_files[:50]

# Cleanup text
merged_text = []
for filename in txt_files:
    filepath = os.path.join(directory, filename)
    with open(filepath, 'r', encoding='utf-8') as file:  # Specify encoding
        lines = file.readlines()
        non_empty_lines = [line.strip() for line in lines if line.strip()]
        file_content = '\n'.join(non_empty_lines)
        merged_text.append(file_content)

# Export to txt file
output_file = r'C:\Users\ohakimu\OneDrive - Perkins and Will\Desktop\IAAC\Semester 3\Gen AI\LLM\LLM-Finetuning\dataset\clean_text.txt'
with open(output_file, 'w', encoding='utf-8') as file:  # Specify encoding
    for content in merged_text:
        file.write(content + '\n\n')

print(f"Saved {output_file}")
