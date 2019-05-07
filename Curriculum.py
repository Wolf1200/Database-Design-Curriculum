import mysql.connector

# Global variables
mydb = ""
mycursor = ""
results = ""


# Function to get curriculum coverage
def findcoverage(currname):
    # Define variables
    global mycursor
    requnitsum = 0
    optunitsum = 0
    iscovered = 0
    level_1_reqcoveredsum = 0
    level_2_reqcoveredsum = 0
    level_3_reqcoveredsum = 0
    level_2_optcoveredsum = 0

    # Get list of topicID in curriculum
    query = "select topicID, level, units from curriculum.curriculumtopics where curriculumName='" + currname + "'"

    # Get result set
    mycursor.execute(query)
    res = mycursor.fetchall()

    # For each topicID, find the courses that cover it
    for i in res:
        query = "select units, courseName from curriculum.coursetopics where curriculumName='" + currname + "' " \
                "and topicID='" + str(i[0]) + "'"
        mycursor.execute(query)
        courseres = mycursor.fetchall()

        # Calculate if coverage is met or not
        for j in courseres:
            query = "select optional from curriculum.curriculumcourses where curriculumName='" + currname + "' and " \
                    "courseName='" + str(j[1]) + "'"
            mycursor.execute(query)
            optcourse = mycursor.fetchall()

            # If course is required, add to req sum, else add to optional sum
            if optcourse[0][0] == 0:
                requnitsum += j[0]
            else:
                optunitsum += j[0]

        # If coverage is met, set bool value
        if requnitsum >= i[2]:
            if i[1] == 1:
                level_1_reqcoveredsum += 1
            if i[1] == 2:
                level_2_reqcoveredsum += 1
            if i[1] == 3:
                level_3_reqcoveredsum += 1
        if optunitsum + requnitsum >= i[2] and i[1] == 2:
            level_2_optcoveredsum += 1

        requnitsum = 0
        optunitsum = 0

    # Get count of all topics from each level
    query = "select count(*) from curriculum.curriculumtopics where level=1"
    mycursor.execute(query)
    level1count = mycursor.fetchall()
    level1count = level1count[0][0]

    query = "select count(*) from curriculum.curriculumtopics where level=2"
    mycursor.execute(query)
    level2count = mycursor.fetchall()
    level2count = level2count[0][0]

    query = "select count(*) from curriculum.curriculumtopics where level=3"
    mycursor.execute(query)
    level3count = mycursor.fetchall()
    level3count = level3count[0][0]

    # Compare cover count to level count and decide coverage
    if level_1_reqcoveredsum >= level1count and level_2_reqcoveredsum >= level2count \
            and level_3_reqcoveredsum >= level3count / 2:
        return "Extensive"
    elif level_1_reqcoveredsum >= level1count and level_2_reqcoveredsum >= level2count:
        return "Inclusive"
    elif level_1_reqcoveredsum >= level1count and (level_2_reqcoveredsum / 2) + level_2_optcoveredsum >= level2count:
        return "Basic-plus"
    elif level_1_reqcoveredsum >= level1count and level_2_reqcoveredsum / 2 >= level2count:
        return "Basic"
    elif level_1_reqcoveredsum >= level1count:
        return "Unsatisfactory"
    else:
        return "Substandard"


# Function to get a count of the required and optional courses to a curriculum
def getrequiredcount(currname):
    # Define variables
    global mycursor
    query = "select count(*) from course a, curriculum.curriculumcourses b where b.curriculumName='" + currname + "'" \
            " and b.courseName = a.name and b.optional=0"

    # Execute query for count of required
    mycursor.execute(query)

    # Get result set from query
    res = mycursor.fetchall()

    # Get count of req courses from result set
    reqcount = res[0]

    # Query for getting count of optional courses in curriculum
    query = "select count(*) from course a, curriculum.curriculumcourses b where b.curriculumName='" + currname + "'" \
            " and b.courseName = a.name and b.optional=1"

    # Execute query for count of optional
    mycursor.execute(query)

    # Get result set from query
    res = mycursor.fetchall()

    # Get count of optional courses from result set
    opcount = res[0]

    # Make a set to return counts
    retset = [reqcount, opcount]

    return retset


# Function to get a list of courses in a range
def getrangecourses(currname, startsem, endsem, startyear, endyear):
    # Define variables
    global mycursor
    query = "select a.name, c.semester, c.year from course a, curriculum.curriculumcourse b, curriculum.coursesections c where " \
            "b.curriculumName='" + currname + "' and b.courseName = a.name and " \
            "c.courseName = a.name and c.year between '" + startyear + "' and '" + endyear + "' order by c.year"

    # Execute query
    mycursor.execute(query)

    betweenyears = mycursor.fetchall()
    validcourses = [None] * len(betweenyears)
    i = 0
    for course in betweenyears:
        if course[2] == startyear:
            if startsem == "Fall":
                if course[1] == "Fall":
                    validcourses[i] = course
            else:
                validcourses[i] = course
        elif course[2] == endyear:
            if endsem == "Spring":
                if course[1] == "Spring":
                    validcourses[i] = course
            else:
                validcourses[i] = course
        else:
            validcourses[i] = course

        i += 1

    # Return result set
    return validcourses


def getcurriculumcourses(curr):
    global mycursor
    query = "select courseName from curriculumcourses where curriculumName = '" + curr + "'"

    mycursor.execute(query)
    return mycursor.fetchall()


def getcurriculumcredits(curr):
    global mycursor
    query = "select b.creditHours from curriculumcourses a, course b where a.curriculumName = '" \
            + curr + "' and a.courseName = b.name"

    mycursor.execute(query)
    hourstemp = mycursor.fetchall()
    hours = 0
    for hour in hourstemp:
        hours += int(hour[0])
    return hours


def getcoursesections(course):
    global mycursor
    query = "select * from studentgrades where courseName = '" + course + "'"

    mycursor.execute(query)
    return mycursor.fetchall()


def getyears():
    global mycursor
    query = "select year from coursesections group by year"
    mycursor.execute(query)
    return mycursor.fetchall()


# Function to insert curriculum
def insertcurriculum(array):
    # Define variables
    global mydb
    global mycursor

    query = "insert into curriculum (name, headID, headName, totCredits, maxUnits, coverage, numGoals) values " \
            "(%s, %s, %s, %s, %s, %s, %s)"

    # Execute query and commit db
    mycursor.execute(query, array)
    mydb.commit()


# Function to get curriculum
def getcurriculum(name):
    # Define variables
    global mycursor
    query = "select * from curriculum where name='" + name + "'"

    # Execute query
    mycursor.execute(query)

    # Return result set
    return mycursor.fetchall()


# Function to edit a curriculum
def editcurriculum(array, currname):
    # Define variables
    global mycursor
    global mydb

    query = "update curriculum.curriculum set name='" + array[0] + "', headID='" + array[1] + "', " \
            "headName='" + array[2] + "', totCredits='" + array[3] + "', maxUnits='" + array[4] + "', " \
            "coverage='" + array[5] + "', numGoals='" + array[6] + "' where (name='" + currname + "')"

    # Execute edit and commit
    mycursor.execute(query)
    mydb.commit(query)


def getcurriculumhead(curriculum):
    global mycursor
    query = "select headName from curriculum where name = '" + curriculum + "'"
    mycursor.execute(query)

    return mycursor.fetchall()


def getcurrentcurriculums():
    global mycursor
    query = "select name from Curriculum"

    mycursor.execute(query)

    ret = mycursor.fetchall()
    return ret


def getcurrentcourses():
    global mycursor
    query = "select name from Course"

    mycursor.execute(query)

    ret = mycursor.fetchall()
    return ret


def getcoursecurriculum(course):
    global mycursor
    query = "select curriculumName from curriculumcourses where courseName = '" + course + "'"

    mycursor.execute(query)

    return mycursor.fetchall()


# Function to insert course
def insertcourse(array):
    # Define variables
    global mycursor
    global mydb

    # # Get values from user
    # name = input("Enter the name of the course: ")
    # subcode = input("Enter the subcode: ")
    # coursenum = input("Enter the course number: ")
    # credithrs = input("Enter the credit hours of the course: ")
    # desc = input("Enter the course description: ")
    #
    # # Verify no null values in key
    # while subcode == "" or coursenum == "":
    #     if subcode == "":
    #         print("You need to enter a value for subcode.")
    #         subcode = input("Enter the subcode: ")
    #     if coursenum == "":
    #         print("You need to enter a value for subcode.")
    #         coursenum = input("Enter the course number: ")

    # Insert tuple
    query = "insert into course (name, subCode, courseNumber, creditHours, description) values (%s, %s, %s, %s, %s)"

    # Execute query and commit to db
    mycursor.execute(query, array)
    mydb.commit()


# Function to get course
def getcourse(coursename):
    # Define variables
    global mycursor
    query = "select * from course where name='" + coursename + "'"

    # Execute query
    mycursor.execute(query)

    # Return results of query
    return mycursor.fetchall()


# Function to edit course
def editcourse(array, name, subcode, coursenum):
    # Define variables
    global mycursor
    global mydb
    query = "update curriculum.course set name=%s, subCode=%s, courseNumber=%s, creditHours=%s, description=%s" \
            "where (name='" + name + "') and (subCode='" + subcode + "') and (courseNumber='" + coursenum + "')"

    # Execute query and commit db
    mycursor.execute(query, array)
    mydb.commit()


# Function to insert topics
def inserttopics(array):
    # Define variables
    global mycursor
    global mydb

    # # Get input from user
    # topicid = input("Enter the topic id: ")
    # name = input("Enter the topic name: ")
    #
    # # Ensure id is not null
    # while topicid == "":
    #     print("You need to enter in a topic id.")
    #     topicid = input("Enter the topic id: ")

    query = "insert into topics (id, name) values (%s, %s)"

    mycursor.execute(query, array)
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


def getcurriculumtopics(curr):
    global mycursor
    query = "select topicID from curriculumtopics where curriculumName = '" + curr + "'"
    mycursor.execute(query)

    return mycursor.fetchall()


# Function to edit topics
def edittopics(array, oldid):
    # Define variables
    global mycursor
    global mydb
    query = "update curriculum.topics set id=%s, name=%s where (id='" + oldid + "')"

    # Execute query and commit db
    mycursor.execute(query, array)
    mydb.commit()


# Function to get all topics by key
def getcurrenttopics():
    global mycursor
    query = "select id from curriculum.topics"

    mycursor.execute(query)

    ret = mycursor.fetchall()
    return ret


# Function to insert goal
def insertgoal(array):
    # Define variables
    global mydb
    global mycursor

    # # Get values from user
    # goalid = input("Enter the goal id: ")
    # desc = input("Enter the goal description: ")
    # curr = input("Enter the goal curriculum: ")
    #
    # # Verify key won't be null
    # while goalid == ""  or curr == "":
    #     if goalid == "":
    #         print("You need to enter a goal id.")
    #         goalid = input("Enter the goal id: ")
    #     if curr == "":
    #         print("You need to enter a curriculum.")
    #         curr = input("Enter the goal curriculum: ")

    # Create query to execute
    query = "insert into goal (id, description, curriculum) values (%s, %s, %s)"

    # Execute query and commit db
    mycursor.execute(query, array)
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


# Function to edit goal
def editgoal(array, oldid):
    # Define variables
    global mycursor
    global mydb
    query = "update curriculum.goal set id=%s, description=%s, curriculum=%s where (id='" + oldid + "')"

    # Execute query and commit db
    mycursor.execute(query, array)
    mydb.commit()


def getcurrentgoals():
    global mycursor
    query = "select id from curriculum.goal"

    mycursor.execute(query)

    ret = mycursor.fetchall()
    return ret


# Function to insert goal/grade relationship
def insertgoalgrade(array):
    # Define variable
    global mydb
    global mycursor

    # # Get user input
    # semester = input("Enter the semester: ")
    # year = input("Enter the year (YYYY): ")
    # secid = input("Enter the section id: ")
    # subcode = input("Enter the subcode: ")
    # coursenum = input("Enter the course number: ")
    # goalid = input("Enter the goal id: ")
    # goalgrade = input("Enter the goal grade: ")
    #
    # # Verify key will not be null
    # while semester == "" or year == "" or secid == "" or subcode == "" or coursenum == "" or goalid == "":
    #     if semester == "":
    #         print("You need to enter a semester.")
    #         semester = input("Enter the semester: ")
    #     if year == "":
    #         print("You need to enter a year.")
    #         year = input("Enter the year (YYYY): ")
    #     if secid == "":
    #         print("You need to enter a section id.")
    #         secid = input("Enter the section id: ")
    #     if subcode == "":
    #         print("You need to enter a subcode.")
    #         subcode = input("Enter the subcode: ")
    #     if coursenum == "":
    #         print("You need to enter a course number.")
    #         coursenum = input("Enter the course number: ")
    #     if goalid == "":
    #         print("You need to enter the goal id.")
    #         goalid = input("Enter the goal id: ")

    # Define query to insert
    query = "insert into goalgrades (semester, year, sectionID, subCode, courseNumber, goalID, goalGrade) values " \
            "(%s, %s, %s, %s, %s, %s, %s)"

    # Execute query and commit db
    mycursor.execute(query, array)
    mydb.commit()


# Function to get goal/grade
def getgoalgrade(semester, year, secid, courseName, goalid):
    # Define variables
    global mycursor
    query = "select * from goalgrades where semester='" + semester + "' and year='" + year + "' and sectionID='"\
            + secid + "' and courseName = '" + courseName + "' and goalID='" + goalid + "'"

    # Execute query
    mycursor.execute(query)

    # Return result set
    return mycursor.fetchall()


# Function to edit goalgrade
def editgoalgrade(array, semester, year, secid, coursename, goalid):
    # Define variables
    global mycursor
    global mydb
    query = "update curriculum.goalgrades set semester=%s, year=%s, sectionID=%s, subCode=%s, courseNumber=%s, goalID" \
            "=%s goalGrade=%s where (semester='" + semester + "') and (year='" + year + "') and (sectionID=" \
            "'" + secid + "') and (courseName='" + coursename + "') and (goalID='" + goalid + "')"

    # Execute query and commit db
    mycursor.execute(query, array)
    mydb.commit()


def getcurrentgoalgrades():
    global mycursor
    query = "select * from curriculum.goalgrades"

    mycursor.execute(query)

    ret = mycursor.fetchall()
    return ret


# Function to insert Curriculum/Topics
def insertcurriculumtopics(array):
    # Define variables
    global mydb
    global mycursor

    query = "insert into curriculumtopics (curriculumName, topicID, level, subjectArea, units) values " \
            "(%s, %s, %s, %s, %s)"

    # Execute query and commit db
    mycursor.execute(query, array)
    mydb.commit()


# Function to get Curriculum/Topics
def getcurriculumtopic(currname, topicid):
    # Define variables
    global mycursor
    query = "select * from curriculumtopics where curriculumName='" + currname + "' and topicID='" + topicid + "'"

    # Execute query
    mycursor.execute(query)

    # Return result set
    return mycursor.fetchall()


# Function to edit curriculumtopic
def editcurriculumtopics(array, currname, topicid):
    # Define variables
    global mycursor
    global mydb
    query = "update curriculum.curriculumtopics set curriculumName=%s, topicID=%s, level=%s, subjectArea=%s, " \
            "units=%s where (curriculumName='" + currname + "') and (topicID='" + topicid + "')"

    # Execute query and commit db
    mycursor.execute(query, array)
    mydb.commit()


def getcurrentcurrtopics():
    global mycursor
    query = "select curriculumName, topicID from curriculum.curriculumtopics"

    mycursor.execute(query)

    ret = mycursor.fetchall()
    return ret


# Function to insert Course/Topics
def insertcoursetopics(array):
    # Define variables
    global mydb
    global mycursor

    # Define insert query
    query = "insert into coursetopics (courseName, curriculumName, topicID, units) values " \
            "(%s, %s, %s, %s)"

    # Execute query and commit db
    mycursor.execute(query, array)
    mydb.commit()


# Function to get Course/Topics
def getcoursetopics(coursename, currname, topicid):
    # Define variables
    global mycursor
    query = "select * from coursetopics where courseName = '" + coursename + "' and " \
            "curriculumName='" + currname + "' and topicID='" + topicid + "'"

    # Execute query
    mycursor.execute(query)

    # Return result set
    return mycursor.fetchall()


# Function to edit coursetopics
def editcoursetopics(array, coursename, currname, topicid):
    # Define variables
    global mycursor
    global mydb
    query = "update curriculum.coursetopics set courseName=%s, curriculumName=%s, topicID-%s, units=%s where " \
            "(courseName='" + coursename + "') and (curriculumName='" + currname + "') and " \
            "(topicID='" + topicid + "')"

    # Execute query and commit db
    mycursor.execute(query, array)
    mydb.commit()


def getcurrentcoursetopics():
    global mycursor
    query = "select courseName, curriculumName, topicID from curriculum.coursetopics"

    mycursor.execute(query)

    ret = mycursor.fetchall()
    return ret


# Function to insert Course/Goals
def insertcoursegoals(array):
    # Define variables
    global mydb
    global mycursor

    # Define query to insert
    query = "insert into coursegoals (curriculumName, courseName, goalID) values (%s, %s, %s)"

    # Execute query and commit db
    mycursor.execute(query, array)
    mydb.commit()


# Function to get Course/Goals
def getcoursegoals(currname, courseName, goalid):
    # Define variables
    global mycursor
    query = "select * from coursegoals where curriculumName='" + currname + "' and courseName = '" + courseName + \
            "' and goalID='" + goalid + "'"

    # Execute query
    mycursor.execute(query)

    # Return result set
    return mycursor.fetchall()


# Function to edit coursegoals
def editcoursegoals(array, currname, coursename):
    # Define variables
    global mycursor
    global mydb
    query = "update curriculum.coursegoals set curriculumName=%s, courseName=%s, goalID=%s where (curriculumName=" \
            "'" + currname + "') and (courseName='" + coursename + "')"

    # Execute query and commit db
    mycursor.execute(query, array)
    mydb.commit()


def getcurrentcoursegoals():
    global mycursor
    query = "select curriculumName, courseName from curriculum.coursegoals"

    mycursor.execute(query)

    ret = mycursor.fetchall()
    return ret


# Function to insert Curriculum/Courses
def insertcurriculumcourses(array):
    # Define variables
    global mydb
    global mycursor

    # Define query to insert
    query = "insert into curriculumcourses (curriculumName, courseName, optional) " \
            "values (%s, %s, %s)"

    # Execute query and commit db
    mycursor.execute(query, array)
    mydb.commit()


# Function to get Curriculum/Course
def getcurriculumcourse(currname, coursename):
    # Define variables
    global mycursor
    query = "select * from curriculumcourses where curriculumName='" + currname + "' and courseName = '" + \
            coursename + "'"

    # Execute query
    mycursor.execute(query)

    # Return result set
    return mycursor.fetchall()


# Function to edit curriculumcourse
def editcurriculumcourse(array, currname, coursename):
    # Define variables
    global mycursor
    global mydb
    query = "update curriculum.curriculumcourses set curriculumName=%s, courseName=%s, optional=%s where " \
            "(curriculumName='" + currname + "') and (courseName='" + coursename + "')"

    # Execute query and commit db
    mycursor.execute(query, array)
    mydb.commit()


def getcurrentcurrcourses():
    global mycursor
    query = "select curriculumName, courseName from curriculum.curriculumcourses"

    mycursor.execute(query)

    ret = mycursor.fetchall()
    return ret


# Function to insert StudentGrades
def insertstudentgrades(array):
    # Define variables
    global mydb
    global mycursor

    # Define query to insert
    query = "insert into studentgrades (semester, year, sectionID, courseName, numAP, numA, numAM, numBP," \
            " numB, numBM, numCP, numC, numCM, numDP, numD, numDM, numF, numW, numI) values " \
            "(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

    # Execute query and commit db
    mycursor.execute(query, array)
    mydb.commit()


# Function to get StudentGrades
def getstudentgrades(semester, year, secid, courseName):
    # Define variables
    global mycursor
    query = "select * from studentgrades where semester='" + semester + "' and year='" + year + "' and sectionID='" \
            + secid + "' and courseName = '" + courseName + "'"

    # Execute query
    mycursor.execute(query)

    # Return result set
    return mycursor.fetchall()


# Function to edit studentgrades
def editstudentgrades(array, semester, year, secid, coursename):
    # Define variables
    global mycursor
    global mydb
    query = "update curriculum.studentgrades set semester=%s, year=%s, sectionID=%s, courseName=%s, numAP=%s,numA=%s," \
            " numAM=%s, numBP=%s, numB=%s, numBM=%s, numCP=%s, numC=%s, numCM=%s, numDP=%s, numD=%s, numDM=%s, " \
            "numF=%s, numW=%s, numI=%s where (semester='" + semester + "') and (year='" + year + "') and (sectionID=" \
            "'" + secid + "') and (courseName='" + coursename + "')"

    # Execute query and commit db
    mycursor.execute(query, array)
    mydb.commit()


def getcurrentstudentgrades():
    global mycursor
    query = "select semester, year, sectionID, courseName from curriculum.studentgrades"

    mycursor.execute(query)

    ret = mycursor.fetchall()
    return ret


# Function to insert Course/Sections
def insertcoursesections(array):
    # Define variables
    global mydb
    global mycursor

    # Define query to insert
    query = "insert into coursesections (semester, year, sectionID, courseName) values " \
            "(%s, %s, %s, %s)"

    # Execute query and commit db
    mycursor.execute(query, array)
    mydb.commit()


# Function to get Course/Sections
def getcoursesection(semester, year, secid, courseName):
    # Define variables
    global mycursor
    query = "select * from coursesections where semester='" + semester + "' and year='" + year + "' and sectionID='" \
            + secid + "' and courseName = '" + courseName + "'"

    # Execute query
    mycursor.execute(query)

    # Return result set
    return mycursor.fetchall()


# Function to edit coursesection
def editcoursesection(array, semester, year, secid, coursename):
    # Define variables
    global mycursor
    global mydb
    query = "update curriculum.coursesections set semester=%s, year=%s, sectionID=%s, courseName=%s, enrolled=%s," \
            " comment1=%s, comment2=%s where (semester='" + semester + "') and (year='" + year + "') and (sectionID=" \
            "'" + secid + "') and (courseName='" + coursename + "')"

    # Execute query and commit db
    mycursor.execute(query, array)
    mydb.commit()


def getcurrentcoursesections():
    global mycursor
    query = "select semester, year, sectionID, courseName from curriculum.coursesections"

    mycursor.execute(query)

    ret = mycursor.fetchall()
    return ret


# Function to return all topics and courses related to a curriculum (names only)
def getallcoursestopics(currname):
    # Define variables
    global mycursor
    query = "select a.name, c.name from course a, curriculum.curriculumcourses b, topics c, curriculumtopics d where" \
            " b.curriculumName = '" + currname + "' and a.subCode = b.subCode and a.courseNumber = b.courseNumber " \
            "and d.curriculumName = '" + currname + "' and d.topicID = c.id"

    # Execute query
    mycursor.execute(query)

    # Return result set
    return mycursor.fetchall()


# Function to initialize the database
def initdatabase():
    # Open DB connection
    global mydb
    mydb = mysql.connector.connect(user='testUser', password='SicEmBears', host='127.0.0.1', database='Curriculum')
    global mycursor
    mycursor = mydb.cursor()

    # mycursor.execute("CREATE DATABASE IF NOT EXISTS Curriculum")

    # mycursor.execute("CREATE USER IF NOT EXISTS testUser@localhost IDENTIFIED BY 'SicEmBears';")
    # mycursor.execute("use curriculum")
    # mycursor.execute("GRANT all on curriculum.* to testUser@localhost")

    # mydb = mysql.connector.connect(user='testUser', password='SicEmBears',
                                   # host='127.0.0.1', database='Curriculum')

    mycursor = mydb.cursor()

    # If some tables don't exist, create them
    mycursor.execute("create table IF NOT EXISTS curriculum (name varchar(25) not null, headID bigint, headName varchar(25),"
                     "totCredits int, maxUnits float, coverage varchar(25), numGoals int, "
                     "primary key (name))")

    mycursor.execute("create table IF NOT EXISTS topics (id int not null, name varchar(25), "
                     "constraint topics_pk primary key (id))")

    mycursor.execute("create table IF NOT EXISTS curriculumTopics (curriculumName varchar(25) not null, topicID int "
                     "not null, level int, subjectArea varchar(25), units float, "
                     "primary key (curriculumName, topicID), foreign key (curriculumName) "
                     "references curriculum (name), foreign key (topicID) references topics (id))")

    mycursor.execute("create table IF NOT EXISTS goal (id int not null, description text, curriculum varchar(25) "
                     "not null, primary key (id, curriculum),"
                     "foreign key (curriculum) references curriculum (name))")

    mycursor.execute("create table IF NOT EXISTS course (name varchar(25) not null unique, subCode varchar(25) not null, "
                     "courseNumber int not null, creditHours int, description text, constraint course_pk "
                     "primary key (name, subCode, courseNumber))")

    mycursor.execute("create table IF NOT EXISTS courseTopics (courseName varchar(25) not null,"
                     " curriculumName varchar(25) not null, topicID int not null, units float,"
                     "primary key (courseName, curriculumName, topicID), foreign key (curriculumName, topicID) "
                     "references curriculumtopics (curriculumName, topicID),"
                     "foreign key (courseName) references course (name))")

    mycursor.execute("create table IF NOT EXISTS curriculumCourses (curriculumName varchar(25) not null,"
                     "courseName varchar(25) not null, optional bool,"
                     "primary key (curriculumName, courseName),"
                     "foreign key (curriculumName) references curriculum (name),"
                     "foreign key (courseName) references course(name))")

    mycursor.execute("create table IF NOT EXISTS courseGoals (curriculumName varchar(25) not null, "
                     "courseName varchar(25) not null, goalID int not null, "
                     "primary key (curriculumName, courseName, goalID),"
                     "foreign key (curriculumName, courseName) "
                     "references curriculumcourses (curriculumName, courseName),"
                     "foreign key (goalID) references goal (id))")

    mycursor.execute("create table IF NOT EXISTS courseSections (semester varchar(25) not null, year year not null, "
                     "sectionID int not null, courseName varchar(25) not null, "
                     "enrolled int, comment1 text, comment2 text, constraint courseSections_pk primary key "
                     "(semester, year, sectionID, courseName),"
                     "foreign key (courseName) references course (name))")

    mycursor.execute("create table IF NOT EXISTS studentGrades (semester varchar(25) not null, year year not null, "
                     "sectionID int not null, courseName varchar(25) not null, numAP int, "
                     "numA int, numAM int, numBP int, numB int, numBM int, numCP int, numC int, numCM int, numDP int, "
                     "numD int, numDM int, numF int, numW int, numI int,"
                     "primary key (semester, year, sectionID, courseName),"
                     "foreign key (semester, year, sectionID, courseName) "
                     "references coursesections (semester, year, sectionID, courseName))")

    mycursor.execute("create table IF NOT EXISTS goalGrades (semester varchar(25) not null, year year not null, "
                     "sectionID int not null, courseName varchar(25) not null, goalID int "
                     "not null, goalGrade varchar(25), constraint goalGrades_pk primary key "
                     "(semester, year, sectionID, courseName, goalID),"
                     "foreign key (semester, year, sectionID, courseName) "
                     "references coursesections (semester, year, sectionID, courseName))")
