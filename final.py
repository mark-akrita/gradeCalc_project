import json
import sys

print("BARLUS")

with open("students.json") as data_file:
        data = json.load(data_file)
with open("gc_setup.json") as data_file:
    gc_setup = json.load(data_file)

def askStudentID():
    students = data["students"]
    studentID = input("Enter your ID(by name_surname format): ")
    for ind in range(len(students)):
        if students[ind]["id"] == studentID:
            student = data["students"][ind]["id"]
            break
    else:
        student = {"id": studentID, "courses": [{}]}
        data["students"].append(student)
        file = open("students.json", "w")
        file.write(json.dumps(data))
        file.close()
    return student

def addCourses(student):
    students = data["students"]
    for ind in range(len(students)):
         if students[ind]["id"] == student:
             courses = students[ind]["courses"]
    print("Your courses..")
    curr_courses = []
    for ind in range(len(courses)):
        try:
            curr_courses.append(courses[ind]["course"])
            print(courses[ind]["course"])
            #for key in courses[ind]["grades"]:
                #print(key + ": " + courses[ind]["grades"][key])
        except KeyError:
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
                        print(key + ": " + courses[ind]["grades"][key])
        elif step == 'add':
            add = input("Add course: ")
            courses.append({"course": add, "grades": {}})
            file = open("students.json", "w")
            file.write(json.dumps(data))
            file.close()
            course = add
            break
        elif step == 'update':
            update = input("Which course: ")
            for ind in range(len(courses)):
                if update == courses[ind]["course"]:
                    course = courses[ind]["course"]
            break
        elif step == '':
            calculateGPA(student)
            sys.exit()
            break
        else:
            print("Invalid input, again")
    return course

def loadSetupData():
    grades = gc_setup["course_setup"]["grade_breakdown"]
    return grades

def askForAssignmentMarks(grades, student, course):
    current_grades = {}
    for ind in range(len(data["students"])):
        if data["students"][ind]["id"] == student:
            for jnd in range(len(data["students"][ind]["courses"])):
                if data["students"][ind]["courses"][jnd]["course"] == course:
                    current_grades = data["students"][ind]["courses"][jnd]["grades"]
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
    data["students"][ind]["courses"][jnd]["grades"] = current_grades
    return current_grades

def saveGrades(current_grades):
    print ("Your grades...") #json.dumps(current_grades))
    for key in current_grades:
        print(key + ':', current_grades[key])
    file = open("students.json", "w")
    file.write(json.dumps(data))
    file.close()

def calculateGrades(grades, current_grades):
    curr_grade = 0
    for key in current_grades:
        if current_grades[key] != -1:
            calc_grade = float(current_grades[key]) * grades[key] / 100
            curr_grade = curr_grade + calc_grade
    return curr_grade

def stringConverter(curr_grade):
    marks = gc_setup["course_setup"]["conv_matrix"]
    for ind in range(len(marks)):
        if curr_grade >= marks[ind]["min"] and curr_grade <= marks[ind]["max"]:
            mark = marks[ind]["mark"]
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
    file = open("students.json", "w")
    file.write(json.dumps(data))
    file.close()

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
