import pandas as pd
import matplotlib.pyplot as plt

pd.set_option('display.max_colwidth', -1)

df = pd.read_csv('jeopardy.csv')


# Renaming misformatted columns
df = df.rename(columns = {" Air Date": "Air Date", " Round" : "Round", " Category": "Category",
                                    " Value": "Value", " Question":"Question", " Answer": "Answer"})

#print(df['Answer'])

#Write a function that filters the dataset for questions that contains all of the words in a list of words. For example, when the list ["King", "England"] was passed to our function, the function returned a DataFrame of 152 rows. Every row had the strings "King" and "England" somewhere in its " Question".

#Note that in this example, we found 152 rows by filtering the entire dataset. You can download the entire dataset at
# the start or end of this project. The dataset used on Codecademy is only a fraction of the dataset so you won’t find as many rows.

#Test your function by printing out the column containing the question of each row of the dataset.


def filter_word(data, words):
    filtered = data[data['Question'].apply(lambda row: all(word.lower() in row.lower() for word in words))]
    return filtered

#filter_string = filter_word(df, ["King", "England"])

#We may want to eventually compute aggregate statistics, like .mean() on the " Value" column. But right now, the values in that column are strings. Convert the " Value" column to floats. If you’d like to, you can create a new column with the float values.

# Now that you can filter the dataset of question, use your new column that contains the float values of each question to find the “difficulty” of certain topics. For example, what is the average value of questions that contain the word "King"?
#
# Make sure to use the dataset that contains the float values as the dataset you use in your filtering function.


df['value_float'] = df['Value'].apply(lambda row: row[1:].replace(',', '') if row != 'None' else 0 )
df['value_float'] = df['value_float'].astype(float)
#print(df.head())

filtered_string = filter_word(df, ['King'])

average_value = filtered_string['value_float'].mean()
#print(average_value)

#Write a function that returns the count of the unique answers to all of the questions in a dataset. For example,
# after filtering the entire dataset to only questions containing the word "King", we could then find all of the unique answers to those questions. The answer “Henry VIII” appeared 3 times and was the most common answer.

def unique_ans():
    ans_count = filtered_string['Answer'].value_counts()
    return ans_count
#print(unique_ans())
#unique_ans_count = unique_ans()
#print(type(unique_ans_count))

# Investigate the ways in which questions change over time by filtering by the date. How many questions from the 90s use the word "Computer" compared to questions from the 2000s?

df["Air Date"] = pd.to_datetime(df["Air Date"]) # convert the date column to pd datetime

# checking the number of time they used the word "Computer" during the 90s
def word_computer_90s(date, word):
    #filter the df date column with the argument date and check if the date is less or equal to 2000-01-01
    # because if the argument date is 2000 that means we are checking for 90s then check the statement for less
    # condition but if the argument date is less than 2000-01-01 then check the statement for greater than the argument
    f_date = df[df["Air Date"].apply(lambda x: x < pd.Timestamp(date)if date >= '2000-01-01' else
    x>pd.Timestamp(date))]
    #f_date = df[df["Air Date"] < pd.Timestamp(date)] # old line of code

    # Check the "Question" column if it contains the word argument
    filter_comp_90s = f_date[f_date["Question"].map(lambda x:x if type(x) != str else x.lower()).str.contains(
        word.lower(

    )) ==
                         True]
    return  filter_comp_90s

filtered_comp_90s = word_computer_90s('2000-01-01', "Computer")
#print(filtered_comp_90s['Question'])
num_of_computer_90s = len(filtered_comp_90s['Question']) # number of questions that used the word computer in 90s

# This function check for the use of the word computer during 2000s
def word_computer_2000s(date, word):
    filter_w_2000s = word_computer_90s(date, word) # calling the previous function
    return filter_w_2000s

filtered_2000s = word_computer_2000s('1999-12-31', 'Computer')

num_of_computer_2000s = len(filtered_2000s['Question']) # number of questions with the word computer in 2000s

num_of_computers_used = [num_of_computer_90s, num_of_computer_2000s] # list of the various numbers
labels = ['Use of Word Computer 90s', 'Use of Word Computer 2000s']
plt.pie(num_of_computers_used, labels=labels, autopct='%0.1f%%')
plt.axis('equal')
plt.legend(["used in 90s", "used in 2000s"])
plt.title("Comparing the use of the word Computer in 90s and in 2000s")
#plt.show()

# Is there a connection between the round and the category? Are you more likely to find certain categories, like "Literature" in Single Jeopardy or Double Jeopardy?

rounds = ['Jeopardy!', 'Double Jeopardy!', 'Final Jeopardy!', 'Tiebreaker'] # list of the different rounds in the df

# This loop will loop through the rounds list and use the name of each round to filter the round column of the df
# and then count the unique values categories associated to that round
for round in rounds:
    new_df = df[df.Round == round]
    unique_category = new_df['Category'].value_counts().to_dict()
    #unique_category = new_df[new_df['Category'] == 'LITERATURE']
    # print(round)
    # print(unique_category)
    # print("\n")

# Build a system to quiz yourself. Grab random questions, and use the input function to get a response from the user. Check to see if that response was right or wrong. Note that you can’t do this on the Codecademy platform — to do this, download the data, and write and run the code on your own computer!

def q_a ():
    random_question = df['Question'].sample() # sample() is used to sample a random row from question column

    quest_as_list = random_question.tolist() #convert the question column to a list
    string_q = " " # declare and empty string which will be use to collect the question as a string
    return (string_q.join(quest_as_list)) # returning the empty string join with the list question
question = q_a()
print("Question: " + question)
response = input("Enter Your Answer Here: ")

# function to check the answer against the user response
def check_answer():
    filter_df = df[df["Question"] == question] # filter the df to find the randomly generated question
    price_won = filter_df["Value"].to_string(index=False) #since the df has been filter, we take the row in the Value
    # column and convert it to string

    # this check the response of the user against the answer value in the answer column to see if they match
    confirm_ans = filter_df["Answer"].apply(lambda row: "Very Good, You Got the Answer Right, you won"+
        price_won if
    row.lower(

    ) ==
                                                                                                 response.lower() else
    "You entered the wrong "
                                                                                         "answer ").to_string(index=False)
    return confirm_ans
print(check_answer())

#Thanks, You can use this code as much as you want and also you can add more features to this code in this repository