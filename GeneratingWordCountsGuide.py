import pandas as pd

# Load the CSV file
file_path = 'your_file_path_here.csv'  # Replace with your actual file path
df = pd.read_csv(file_path)

# Define a function to count words in a string
def word_count(text):
    return len(str(text).split())

# Initialize a new DataFrame to store word counts
word_count_df = pd.DataFrame()

# Include the non-P columns if needed (e.g., 'Type', 'Condition')
word_count_df['Type'] = df['Type']
word_count_df['Condition'] = df['Condition']

# Calculate word counts for columns P1-P36 and store them in the new DataFrame
for col in df.columns[2:38]:  # Adjust the range according to your DataFrame structure
    word_count_df[col + '_word_count'] = df[col].apply(word_count)

# Save the word counts DataFrame to a new CSV file
new_file_path = 'word_counts_file_path_here.csv'  # Replace with your desired new file path
word_count_df.to_csv(new_file_path, index=False)

print(f"Word counts CSV saved to: {new_file_path}")
