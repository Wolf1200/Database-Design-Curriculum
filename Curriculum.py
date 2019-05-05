import mysql.connector

# Global variables
mydb = ""
mycursor = ""
results = ""


# Function to enter information about a curriculum and everything involved with it (courses, topics, etc)
def insertcurriculum():
    global mydb
    global mycursor


# Function to insert course
def insertcourse():
    # Define variables
    global mycursor
    global mydb

    # Get values from user
    name = input("Enter the name of the course: ")
    subcode = input("Enter the subcode: ")
    coursenum = input("Enter the course number: ")
    credithrs = input("Enter the credit hours of the course: ")
    desc = input("Enter the course description: ")

    # Verify no null values in key
    while subcode == "" or coursenum == "":
        if subcode == "":
            print("You need to enter a value for subcode.")
            subcode = input("Enter the subcode: ")
        if coursenum == "":
            print("You need to enter a value for subcode.")
            coursenum = input("Enter the course number: ")

    # Insert tuple
    query = "insert into course (name, subCode, courseNumber, creditHours, description) values (%s, %s, %s, %s, %s)"
    val = (name, subcode, coursenum, credithrs, desc)

    # Execute query and commit to db
    mycursor.execute(query, val)
    mydb.commit()


# Function to get course
def getcourse(subcode, coursenum):
    # Define variables
    global mycursor
    query = "select * from course where subCode='" + subcode + "' and courseNum='" + coursenum + "'"

    # Execute query
    mycursor.execute(query)

    # Return results of query
    return mycursor.fetchall()


# Function to insert topics
def inserttopics():
    # Define variables
    global mycursor
    global mydb

    # Get input from user
    topicid = input("Enter the topic id: ")
    name = input("Enter the topic name: ")

    # Ensure id is not null
    while topicid == "":
        print("You need to enter in a topic id.")
        topicid = input("Enter the topic id: ")

    query = "insert into topics (id, name) values (%s, %s)"
    val = (topicid, name)

    mycursor.execute(query, val)
    mydb.commit()


# Function to get topic
def gettopic(topicid):
    # Define variables
    global mycursor
    query = "select * from topics where id='" + topicid + "'"

    # Execute query
    mycursor.execute(query)

    # Return result set
    return mycursor.fetchall()


# Function to insert goal
def insertgoal():
    # Define variables
    global mydb
    global mycursor

    # Get values from user
    goalid = input("Enter the goal id: ")
    desc = input("Enter the goal description: ")
    curr = input("Enter the goal curriculum: ")

    # Verify key won't be null
    while goalid == ""  or curr == "":
        if goalid == "":
            print("You need to enter a goal id.")
            goalid = input("Enter the goal id: ")
        if curr == "":
            print("You need to enter a curriculum.")
            curr = input("Enter the goal curriculum: ")

    # Create query to execute
    query = "insert into goal (id, description, curriculum) values (%s, %s, %s)"
    val = (goalid, desc, curr)

    # Execute query and commit db
    mycursor.execute(query, val)
    mydb.commit()


# Function to get goal
def getgoal(goalid, curr):
    # Define variables
    global mycursor
    query = "select * from goal where id='" + goalid + "' and curriculum='" + curr + "'"

    # Execute query
    mycursor.execute(query)

    # Return result set
    return mycursor.fetchall()


# Function to insert 


# Function to initialize the database
def initdatabase():
    # Open DB connection
    global mydb
    mydb = mysql.connector.connect(user='testUser', password='SicEmBears',
                                   host='127.0.0.1')
    global mycursor
    mycursor = mydb.cursor()

    mycursor.execute("CREATE DATABASE IF NOT EXISTS Curriculum")

    mydb = mysql.connector.connect(user='testUser', password='SicEmBears',
                                   host='127.0.0.1', database='Curriculum')

    mycursor = mydb.cursor()

    # If some tables don't exist, create them
    mycursor.execute("create table IF NOT EXISTS curriculum (name varchar(25) not null, headID bigint, totCredits int, "
                     "maxUnits int, coverage varchar(25), numGoals int, constraint curriculum_pk primary key (name))")

    mycursor.execute("create table IF NOT EXISTS curriculumTopics (curriculumName varchar(25) not null, topicID int "
                     "not null, level int, subjectArea varchar(25), units float, constraint curriculumTopics_pk "
                     "primary key (curriculumName, topicID))")

    mycursor.execute("create table IF NOT EXISTS goal (id int not null, description text, curriculum varchar(25) "
                     "not null, constraint goal_pk primary key (id, curriculum))")

    mycursor.execute("create table IF NOT EXISTS courseTopics (subCode varchar(25) not null, courseNumber int not null,"
                     " curriculumName varchar(25) not null, topicID int not null, units float,"
                     "constraint courseTopics_pk primary key (subCode, courseNumber, curriculumName, topicID))")

    mycursor.execute("create table IF NOT EXISTS topics (id int not null, name varchar(25), "
                     "constraint topics_pk primary key (id))")

    mycursor.execute("create table IF NOT EXISTS course (name varchar(25), subCode varchar(25) not null, courseNumber "
                     "int not null, creditHours int, description text, constraint course_pk "
                     "primary key (subCode, courseNumber))")

    mycursor.execute("create table IF NOT EXISTS courseGoals (curriculumName varchar(25) not null, subCode varchar(25) "
                     "not null, courseNumber int not null, goalID int not null, "
                     "constraint courseGoals_pk primary key (curriculumName, subCode, courseNumber, goalID))")

    mycursor.execute("create table IF NOT EXISTS curriculumCourses (curriculumName varchar(25) not null, subCode "
                     "varchar(25) not null, courseNumber int not null, optional bool,"
                     "constraint curriculumCourses_pk primary key (curriculumName, subCode, courseNumber))")

    mycursor.execute("create table IF NOT EXISTS studentGrades (semester varchar(25) not null, year year not null, "
                     "sectionID int not null, subCode varchar(25) not null, courseNumber int not null, numAP int, "
                     "numA int, numAM int, numBP int, numB int, numBM int, numCP int, numC int, numCM int, numDP int, "
                     "numD int, numDM int, numF int, numW int, numI int,"
                     "constraint studentGrades_pk primary key (semester, year, sectionID, subCode, courseNumber))")

    mycursor.execute("create table IF NOT EXISTS courseSections (semester varchar(25) not null, year year not null, "
                     "sectionID int not null, subCode varchar(25) not null, courseNumber int not null, "
                     "enrolled int, comment1 text, comment2 text, constraint courseSections_pk primary key "
                     "(semester, year, sectionID, subCode, courseNumber))")

    mycursor.execute("create table IF NOT EXISTS goalGrades (semester varchar(25) not null, year year not null, "
                     "sectionID int not null, subCode varchar(25) not null, courseNumber int not null, goalID int "
                     "not null, goalGrade varchar(25), constraint goalGrades_pk primary key "
                     "(semester, year, sectionID, subCode, courseNumber, goalID))")
