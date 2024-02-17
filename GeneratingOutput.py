from os import environ
import csv
import time
import openai

#You will enter your OpenAI API Key here. This will likely be in the format "sk-................."
openai.api_key = "sk-......";


#This part will be standard. You can change the model. For most outputs, we used GPT-3.5. 
#You may plug in any model supported by OpenAI's API
def analyze(prompt):
	while True:
		try:
			chat = openai.ChatCompletion.create(
				model="gpt-3.5-turbo", messages=[{"role": "user", "content": prompt}]
			)
#This code to indicate if you reached the rate limit. This part does not need to be changed. 
			response = chat.choices[0].message.content
			return response
		except openai.error.RateLimitError:
			print("Rate limit exceeded. Sleeping for 100 seconds...")
			time.sleep(31)
		except:
			print("Some other error occured. Sleeping for 100 seconds and trying again...")
			time.sleep(31)

#these are the columns in the input/output. We had a column of the medical condition
fields = ['Condition'] 

# number of fields (TO BE SET BY USER) Change the number of prompts to how many different prompts you have. 
# For ease, these columns can be called P1, P2, P3, etc. until your number of prompts. For this code, your input file
#should have the conditions as the first column. Then, you may use excel or google sheets to create your 
# various prompts. In excel, you can complete each prompt such that it includes the condition. In other words, each 
#cell of your input file should have the complete input you want to plug into the LLM. i.e Explain acne to a 5th grader. 
num_prompts = 36
for i in range(1,num_prompts+1):
	fields.append("P" + str(num_prompts))

# TO BE SET BY USER
# This is the first row of the CSV to start generating output from. In most cases this will be 0
#However, if you stopped your run you may restart at a different row. Remember to save the python script before 
#starting again.
starting_row = 0

# If the starting row is 0, then it deletes and/or creates a new CSV. If it isn't then it appends to the existing file
# User does not have to worry about this. 
output_type = 'a'
if starting_row == 0:
	output_type = 'w'

#it opens this input file
with open('medicalinputs.csv', newline='') as csvfile:
	reader = csv.DictReader(csvfile)
	#then it creates this output file. If it already exists it deletes then overwrites.
	with open('medicaloutputs.csv', output_type) as csvfile: 
		csvwriter = csv.writer(csvfile) 
		i = 0
		#It writes the columns as the first row. 
		if (output_type == 'w'):
			csvwriter.writerow(fields) 
			
		#This goes through each line in the input file
		for row in reader:
			if i >= starting_row:
				print("ROW: " + str(i) + " -----------------------------------")
				condition = row['Condition']	
				output_row = [
					condition, 
				]


				#we are outputing how ever many columns that are listed in the input (ex: P1 - P36). 

				for k in range(1,num_prompts+1):
					prompt = row['P' + str(k)]
					output_row.append(prompt)

					output = analyze(prompt)

					if ("error" in output): 
						print("ERROR")
					else:
						print("GENERATED")

					output_row.append(output)				
				
				csvwriter.writerow(output_row)

			#This is the row number. This be printing in the terminal 
			i+=1

