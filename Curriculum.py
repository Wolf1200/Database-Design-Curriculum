import mysql.connector


def initdatabase():
    # Define variables
    results = ""
    found = 0

    # Open DB connection
    mydb = mysql.connector.connect(user='testUser', password='SicEmBears',
                                   host='127.0.0.1')
    mycursor = mydb.cursor()

    mycursor.execute("CREATE DATABASE IF NOT EXISTS Curriculum")

    mydb = mysql.connector.connect(user='testUser', password='SicEmBears',
                                   host='127.0.0.1', database='Curriculum')

    mycursor = mydb.cursor()

    # If no tables exist, create the tables we need
    mycursor.execute("create table IF NOT EXISTS curriculum (name varchar(25) not null, headID bigint, totCredits int, maxUnits int, "
                     "coverage varchar(25), numGoals int, constraint curriculum_pk primary key (name))")

    mycursor.execute("create table IF NOT EXISTS curriculumTopics (curriculumName varchar(25) not null, topicID int not null, "
                     "level int, subjectArea varchar(25), units float, constraint curriculumTopics_pk "
                     "primary key (curriculumName, topicID))")

    mycursor.execute("create table goal (id int not null, description text, curriculum varchar(25) not null, "
                     "constraint goal_pk primary key (id, curriculum))")

    mycursor.execute("create table IF NOT EXISTS courseTopics (subCode varchar(25) not null, courseNumber int not null,"
                     " curriculumName varchar(25) not null, topicID int not null, units float,"
                     "constraint courseTopics_pk primary key (subCode, courseNumber, curriculumName, topicID))")

    mycursor.execute("create table IF NOT EXISTS topics (id int not null, name varchar(25), "
                     "constraint topics_pk primary key (id))")

    mycursor.execute("create table IF NOT EXISTS course (name varchar(25), subCode varchar(25) not null, courseNumber int not null,"
                     " creditHours int, description text, constraint course_pk primary key (subCode, courseNumber))")

    mycursor.execute("create table IF NOT EXISTS courseGoals (curriculumName varchar(25) not null, subCode varchar(25) not null, "
                     "courseNumber int not null, goalID int not null, "
                     "constraint courseGoals_pk primary key (curriculumName, subCode, courseNumber, goalID))")

    mycursor.execute("create table IF NOT EXISTS curriculumCourses (curriculumName varchar(25) not null, subCode varchar(25)"
                     " not null, courseNumber int not null, optional bool,"
                     "constraint curriculumCourses_pk primary key (curriculumName, subCode, courseNumber))")

    mycursor.execute("create table IF NOT EXISTS studentGrades (semester varchar(25) not null, year year not null, sectionID int "
                     "not null, subCode varchar(25) not null, courseNumber int not null, numAP int, numA int, "
                     "numAM int, numBP int, numB int, numBM int, numCP int, numC int, numCM int, numDP int, "
                     "numD int, numDM int, numF int, numW int, numI int,"
                     "constraint studentGrades_pk primary key (semester, year, sectionID, subCode, courseNumber))")

    mycursor.execute("create table IF NOT EXISTS courseSections (semester varchar(25) not null, year year not null, sectionID int "
                     "not null, subCode varchar(25) not null, courseNumber int not null, enrolled int, comment1 text, "
                     "comment2 text, constraint courseSections_pk primary key "
                     "(semester, year, sectionID, subCode, courseNumber))")

    mycursor.execute("create table IF NOT EXISTS goalGrades (semester varchar(25) not null, year year not null, sectionID int "
                     "not null, subCode varchar(25) not null, courseNumber int not null, goalID int not null, "
                     "goalGrade varchar(25),"
                     "constraint goalGrades_pk primary key (semester, year, sectionID, subCode, courseNumber, goalID))")
