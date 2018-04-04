import json

def loadSetupData():
    with open('gc_setup.json') as data_file:
        course = json.load(data_file)

    grades = course["course_setup"]["grade_breakdown"]
    return grades

def askForAssignmentMarks(grades):
    #current_grades = {"mygrades": {}}
    with open('gc_grades.json') as data_file:
        try:
            current_grades = json.load(data_file)
        except json.decoder.JSONDecodeError:
            current_grades = {"mygrades": {}}
    for key in grades:
        question = ("What is your Current Grade for " + key + ". Please insert -1 if you don't have a grade yet.")
        print("Weight percent in final grade for", key, "is", str(grades[key]) + '%.')
        try:
            if int(current_grades["mygrades"][key]) > -1:
                print("Your current grade is", current_grades["mygrades"][key],'.')
                print("If you want to update, enter new grade, if not just press 'Enter'")
                step = input()
                """ 
                step = 'Enter'
                while step != "":
                    print("If you want to update, enter new grade, if not just press 'Enter'")
                    step = input()
                    try:
                        assert step == float(step)
                        step = float(step)
                        break
                    except AssertionError:
                        print("Invalid value input")
                        continue"""
                while step.isalpha():
                    if step == '':
                        break
                    step = input("Enter number or just 'Enter'")
                if step == '':
                    current_grades["mygrades"][key] = current_grades["mygrades"][key]
                else:
                    current_grades["mygrades"][key] = step
            else:
                print("You don't have grade for", key, "yet.")
                current_grades["mygrades"][key] = input(question)
        except KeyError:
            current_grades["mygrades"][key] = input(question)
        except json.decoder.JSONDecodeError:
            current_grades = {"mygrades": {}}
            current_grades["mygrades"][key] = input(question)

    return current_grades

def saveGrades(current_grades):
    print ("Your grades...") #json.dumps(current_grades))
    for key in current_grades["mygrades"]:
        print(key + ':', current_grades["mygrades"][key])
    file = open("gc_grades.json", "w")
    file.write(json.dumps(current_grades))
    file.close()

def calculateGrades(grades, current_grades):
    curr_grade = 0
    for key in current_grades["mygrades"]:
        if current_grades["mygrades"][key] != -1:
            calc_grade = int(current_grades["mygrades"][key]) * grades[key] / 100
            curr_grade = curr_grade + calc_grade
    return curr_grade

def stringConverter(curr_grade):
    with open('gc_setup.json') as data_file:
        course = json.load(data_file)
    marks = course["course_setup"]["conv_matrix"]
    for ind in range(len(marks)):
        if curr_grade >= marks[ind]["min"] and curr_grade <= marks[ind]["max"]:
            mark = marks[ind]["mark"]
    return mark

def printCurrentGrade(mark, curr_grade):
    print()
    print("Your calculated grade is: %3.2f" % curr_grade)
    print()
    print("The final mark for course:", mark + ".")

def main():
    grades = loadSetupData()
    current_grades = askForAssignmentMarks(grades)
    saveGrades(current_grades)
    curr_grade = calculateGrades(grades, current_grades)
    mark = stringConverter(curr_grade)
    printCurrentGrade(mark, curr_grade)

main()
