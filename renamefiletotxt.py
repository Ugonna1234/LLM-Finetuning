import os

# Directory containing the files
directory = r'C:\Users\ohakimu\OneDrive - Perkins and Will\Desktop\IAAC\Semester 3\Gen AI\LLM\LLM-Finetuning\scrape_data'

# List all files in the directory
files = os.listdir(directory)

# Rename files to have '.txt' extension
for filename in files:
    if not filename.endswith('.txt'):
        # Construct the old and new file paths
        old_filepath = os.path.join(directory, filename)
        new_filename = os.path.splitext(filename)[0] + '.txt'
        new_filepath = os.path.join(directory, new_filename)
        # Rename the file
        os.rename(old_filepath, new_filepath)
        print(f"Renamed: {old_filepath} to {new_filepath}")
    else:
        print(f"File {filename} already has a '.txt' extension")

print("Renaming complete.")
