import sqlite3

# Connect to the SQLite database
connection = sqlite3.connect('student.db')

# Create a cursor object
cursor = connection.cursor()

# Create a table if it does not exist
cursor.execute('''
CREATE TABLE IF NOT EXISTS students
(NAME VARCHAR(25), CLASS VARCHAR(25), SECTION VARCHAR(25), AGE INTEGER)
''')

# Define a dictionary with student data
students = {
    'John': {'grade': '5', 'class': 'A', 'age': 18},
    'Jane': {'grade': '4', 'class': 'B', 'age': 17},
    'Tom': {'grade': '3', 'class': 'C', 'age': 19},
    'Alice': {'grade': '6', 'class': 'A', 'age': 20},
    'Bob': {'grade': '2', 'class': 'B', 'age': 16},
    'Charlie': {'grade': '7', 'class': 'C', 'age': 21},
    'Daisy': {'grade': '1', 'class': 'A', 'age': 22},
    'Ethan': {'grade': '8', 'class': 'B', 'age': 15}
}

# Insert data into the students table
for name, details in students.items():
    student_tuple = (name, details['grade'], details['class'], details['age'])
    cursor.execute('INSERT INTO students VALUES (?,?,?,?)', student_tuple)

# Commit the changes to the database
connection.commit()

# Output success message
print('Data inserted successfully')

# Retrieve and print all records from the students table
print('Student table:')
data = cursor.execute('SELECT * FROM students').fetchall()
for row in data:
    print(row)

# Close the database connection
connection.close()
