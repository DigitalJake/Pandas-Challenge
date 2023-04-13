# Dependencies and Setup
import pandas as pd
from pathlib import Path

# File to Load (Remember to Change These)
school_data_to_load = Path("Resources/schools_complete.csv")
student_data_to_load = Path("Resources/students_complete.csv")

# Read School and Student Data File and store into Pandas DataFrames
school_data = pd.read_csv(school_data_to_load)
student_data = pd.read_csv(student_data_to_load)

# Combine the data into a single dataset.  
school_data_complete = pd.merge(student_data, school_data, how="left", on=["school_name", "school_name"])
school_data_complete.head()

# Calculate the total number of unique schools
unique_school_names = school_data_complete["school_name"].unique()
print("Unique School Names:")
for name in unique_school_names:
    print(name)
num_unique_schools = len(unique_school_names)
print("Number of Unique School Names:", num_unique_schools)

# Calculate the total number of students
student_count = total_students = len(school_data_complete['Student ID'])
print("Total number of students:", total_students)

# Calculate the total budget
total_budget = school_data['budget'].sum()
print("Total budget of the dataset:", total_budget)

average_math_score = school_data_complete['math_score'].mean()
print("Average math score:", average_math_score)

average_reading_score = school_data_complete['reading_score'].mean()
print("Average reading score:", average_reading_score)

passing_math_count = school_data_complete[(school_data_complete["math_score"] >= 70)].count()["student_name"]
passing_math_percentage = passing_math_count / float(student_count) * 100
passing_math_percentage

passing_reading_count = school_data_complete[(school_data_complete["reading_score"] >= 70)].count()["student_name"]
passing_reading_percentage = passing_reading_count / float(student_count) * 100
passing_reading_percentage

passing_math_reading_count = school_data_complete[
    (school_data_complete["math_score"] >= 70) & (school_data_complete["reading_score"] >= 70)
].count()["student_name"]
overall_passing_rate = passing_math_reading_count /  float(student_count) * 100
overall_passing_rate

# Create a district summary DataFrame
district_summary = pd.DataFrame({
    "Total Schools": [len(school_data)],
    "Total Students": [total_students],
    "Total Budget": [total_budget],
    "Average Math Score": [average_math_score],
    "Average Reading Score": [average_reading_score],
    "% Passing Math": [passing_math_percentage],
    "% Passing Reading": [passing_reading_percentage],
    "% Overall Passing Rate": [overall_passing_rate]})

# Formatting
district_summary["Total Students"] = district_summary["Total Students"].map("{:,}".format)
district_summary["Total Budget"] = district_summary["Total Budget"].map("${:,.2f}".format)
district_summary["% Passing Math"] = district_summary["% Passing Math"].map("{:.2f}%".format)
district_summary["% Passing Reading"] = district_summary["% Passing Reading"].map("{:.2f}%".format)
district_summary["% Overall Passing Rate"] = district_summary["% Overall Passing Rate"].map("{:.2f}%".format)


# Display the DataFrame
print(district_summary)



# create school summary DataFrame
school_type = school_data.set_index('school_name')['type']
total_student = school_data.set_index('school_name')['size']
total_school_budget = school_data.set_index('school_name')['budget']
budget_per_student = total_school_budget/total_student

student_data = student_data.rename(columns={"school_name": "School Name"})
average_math_score = student_data.groupby('School Name')['math_score'].mean()
average_reading_score = student_data.groupby('School Name')['reading_score'].mean()

pass_math = student_data[student_data['math_score'] >= 70].groupby('School Name')['Student ID'].count()/total_student*100
pass_read = student_data[student_data['reading_score'] >= 70].groupby('School Name')['Student ID'].count()/total_student*100
overall_pass = student_data[(student_data['reading_score'] >= 70) & (student_data['math_score'] >= 70)].groupby('School Name')['Student ID'].count()/total_student*100

school_summary = pd.DataFrame({
    "School Type": school_type,
    "Total Students": total_student,
    "Per Student Budget": budget_per_student,
    "Total School Budget": total_school_budget,
    "Average Math Score": average_math_score,
    "Average Reading Score": average_reading_score,
    '% Passing Math': pass_math,
    '% Passing Reading': pass_read,
    "% Overall Passing": overall_pass
})

# munging
school_summary = school_summary[['School Type', 
                                 'Total Students', 
                                 'Total School Budget', 
                                 'Per Student Budget', 
                                 'Average Math Score', 
                                 'Average Reading Score',
                                 '% Passing Math',
                                 '% Passing Reading',
                                 '% Overall Passing']]

# formatting
school_summary.style.format({'Total Students': '{:,}',
                              "Total School Budget": "${:,.2f}",
                              "Per Student Budget": "${:.2f}",
                              'Average Math Score': "{:.2f}", 
                              'Average Reading Score': "{:.2f}", 
                              "% Passing Math": "{:.2f}", 
                              "% Passing Reading": "{:.2f}",
                              "% Overall Passing": "{:.2f}"})


# creates grade level average math scores for each school 
ninth_math = student_data.loc[student_data['grade'] == '9th'].groupby('School Name')["math_score"].mean()
tenth_math = student_data.loc[student_data['grade'] == '10th'].groupby('School Name')["math_score"].mean()
eleventh_math = student_data.loc[student_data['grade'] == '11th'].groupby('School Name')["math_score"].mean()
twelfth_math = student_data.loc[student_data['grade'] == '12th'].groupby('School Name')["math_score"].mean()

math_scores = pd.DataFrame({
        "9th": ninth_math,
        "10th": tenth_math,
        "11th": eleventh_math,
        "12th": twelfth_math
})
math_scores = math_scores[['9th', '10th', '11th', '12th']]
math_scores.index.name = "School Name"

# show and format
math_scores.style.format({'9th': '{:.2f}', 
                           "10th": '{:.2f}', 
                           "11th": "{:.2f}", 
                           "12th": "{:.2f}"})


# creates grade level average reading scores for each school
ninth_reading = student_data.loc[student_data['grade'] == '9th'].groupby('School Name')["reading_score"].mean()
