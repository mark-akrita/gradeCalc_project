import json
import sys

workFile = "students.json"

try:
    with open(workFile) as data_file:
        data = json.load(data_file)
    assert len(data) != 0
except AssertionError:
    data = {"students":  []}
except json.decoder.JSONDecodeError:
    data = {"students": []}
with open("gc_setup.json") as data_file:
    gc_setup = json.load(data_file)

def dataSaver(data):
    try:
        file = open(workFile, "w")
        file.write(json.dumps(data))
    finally:
        file.close()

def askStudentID():
    students = data["students"]
    studentID = input("Enter your ID(by name_surname format): ")
    for i in range(len(students)):
        if students[i]["id"] == studentID:
            student = data["students"][i]["id"]
            break
    else:
        student = studentID
        new_student = {"id": studentID, "courses": []}
        data["students"].append(new_student)
        dataSaver(data)
    return student

def addCourses(student):
    students = data["students"]
    for i in range(len(students)):
         if students[i]["id"] == student:
             courses = students[i]["courses"]
    curr_courses = []
    try:
        print("Your courses..")
        for i in range(len(courses)):
            curr_courses.append(courses[i]["course"])
            print(courses[i]["course"])
        assert len(curr_courses) != 0
    except AssertionError:
        print("You don't have courses yet")
    except (UnboundLocalError, KeyError):
        print("You don't have courses yet")
    while True:
        print("If you want to know grades of a course, type course name")
        print("If You want to add course type 'add'")
        print("If You want to update grades type 'update'")
        print("If You're done, press 'Enter'")
        step = input()
        if step in curr_courses:
            for i in range(len(courses)):
                if courses[i]["course"] == step:
                    for key in courses[i]["grades"]:
                        print(key + ": " + courses[i]["grades"][key])
        elif step == 'add':
            add = input("Add course code: ")
            #courses.append({"course": add, "grades": {}})
            for i in range(len(data["students"])):
                if data["students"][i]["id"] == student:
                    data["students"][i]["courses"].append({"course": add, "grades": {}})
            dataSaver(data)
            course = add
            break
        elif step == 'update':
            update = input("Which course: ")
            for i in range(len(courses)):
                if update == courses[i]["course"]:
                    course = courses[i]["course"]
            break
        elif step == '':
            calculateGPA(student)
            sys.exit()
            break
        else:
            print("Invalid input, try again")
    return course

def loadSetupData():
    grades = gc_setup["course_setup"]["grade_breakdown"]
    return grades

def askForAssignmentMarks(grades, student, course):
    current_grades = {}
    for i in range(len(data["students"])):
        if data["students"][i]["id"] == student:
            for j in range(len(data["students"][i]["courses"])):
                if data["students"][i]["courses"][j]["course"] == course:
                    current_grades = data["students"][i]["courses"][j]["grades"]
    for key in grades:
        question = ("What is your Current Grade for " + key + ". Please insert -1 if you don't have a grade yet.")
        print("Weight percent in final grade for", key, "is", str(grades[key]) + '%.')
        try:
            if float(current_grades[key]) > -1:
                print("Your current grade is", current_grades[key],'.')
                print("If you want to update, enter new grade, if not just press 'Enter'")
                step = input()
                while step.isalpha():
                    if step == '':
                        break
                    step = input("Enter number or just 'Enter'")
                if step == '':
                    current_grades[key] = current_grades[key]
                elif float(step) > 100:
                    while int(step) > 100:
                        step = input("Number between [0:100]")
                        if step == '':
                            break
                else:
                    current_grades[key] = step
            else:
                print("You don't have grade for", key, "yet.")
                current_grades[key] = input(question)
        except KeyError:
            current_grades[key] = input(question)
        except json.decoder.JSONDecodeError:
            current_grades = {"grades": {}}
            current_grades[key] = input(question)
    return current_grades

def saveGrades(current_grades):
    print ("Your grades...") #json.dumps(current_grades))
    for key in current_grades:
        print(key + ':', current_grades[key])
    dataSaver(data)

def calculateGrades(grades, current_grades):
    curr_grade = 0
    for key in current_grades:
        if current_grades[key] != -1:
            calc_grade = float(current_grades[key]) * grades[key] / 100
            curr_grade = curr_grade + calc_grade
    return curr_grade

def stringConverter(curr_grade):
    marks = gc_setup["course_setup"]["conv_matrix"]
    for i in range(len(marks)):
        if curr_grade >= marks[i]["min"] and curr_grade <= marks[i]["max"]:
            mark = marks[i]["mark"]
    return mark

def printCurrentGrade(mark, curr_grade):
    print()
    print("Your calculated grade is: %3.2f" % curr_grade)
    print()
    print("The final mark for course:", mark + ".")

def saveLetterMark(mark, curr_grade, student, course):
    for i in range(len(data["students"])):
        if data["students"][i]["id"] == student:
            for j in range(len(data["students"][i]["courses"])):
                if data["students"][i]["courses"][j]["course"] == course:
                    data["students"][i]["courses"][j]["final_grade"] = curr_grade
                    data["students"][i]["courses"][j]["mark"] = mark
    dataSaver(data)

def calculateGPA(student):
    marks = []
    calc_GPA = 0
    course_count = 0
    print("Your GPA for courses:")
    for i in range(len(data["students"])):
        if data["students"][i]["id"] == student:
            for j in range(len(data["students"][i]["courses"])):
                print(data["students"][i]["courses"][j]["course"] + ':', \
                      data["students"][i]["courses"][j]["final_grade"], \
                      data["students"][i]["courses"][j]["mark"])
                marks.append(data["students"][i]["courses"][j]["mark"])
                course_count += 1
    for mark in marks:
        calc_GPA += gc_setup["course_setup"]["letter_mark"][mark]
    GPA = calc_GPA/course_count
    print("GPA: %3.2f" % GPA)
    return GPA

def main():
    student = askStudentID()
    course = addCourses(student)
    grades = loadSetupData()
    current_grades = askForAssignmentMarks(grades, student, course)
    saveGrades(current_grades)
    curr_grade = calculateGrades(grades, current_grades)
    mark = stringConverter(curr_grade)
    printCurrentGrade(mark, curr_grade)
    saveLetterMark(mark, curr_grade, student, course)
    GPA = calculateGPA(student)

main()
