import os
from flask import request, Flask, make_response
import json
from flask_cors import CORS

class IO:
    def promptAction():
        """
        Method prompts one of the 3 operations and returns some indication
        """
        userAction = input("Enter the index of your action\n"
            "1. Create\n"
            "2. Delete\n"
            "3. get\n"
            "4. getAll\n")
        if not userAction in ['1', '2', '3', '4']:
            print("Enter a valid choice\n")
    
        return userAction
                
        
    def promptStudentInfo(name, age):
        """
        Method prompts student name and age and returns them if valid
        """
        
        if name == "" or name.isspace():
            return "BAD NAME"
        
        
        if not age.isdecimal() or age == "":
            return "BAD AGE"
        
            
        return "GOOD"

    def promptStudentID(id):
        """
        Method prompts id and returns it if valid
        """
        if id == "" or not id.isdecimal():
            return "BAD ID"
            
        return "GOOD"

        
    def showStudent(student):
        """
        Method formats then displays student info retrieved from the database
        """
                
        print("Student name: " + str(student.getName()))
        print("Student age: " + str(student.getAge()))
        print("Student ID: " + str(student.getId())+'\n')
        
        

class StudentMapper:
    __slots__ = ['__student']
    def __init__(this, student):
        """
        All mappers require a Student object stored inside to be able to function
        """
        this.__student = student
        
    
    def save(this):
        """
        saves the student object in the database
        """
        path = os.path.join(os.getcwd(), "students")
        
        if(not os.path.exists(path)):
            os.mkdir(path)
        
        path = os.path.join(path, str(this.__student.getId()) + ".student")
        
        if(os.path.exists(path)):
            return "ID already exists"
            
        with open(path, 'w') as file:
            file.write(this.__student.getName())
            file.write("\n")
            file.write(this.__student.getAge())
            
        return "GOOD"
        
    def get(this):
        """
        loads student info from database and creates then returns a student object
        """
        path = os.path.join(os.getcwd(), "students")
        path = os.path.join(path, str(this.__student.getId()) + ".student")

        if(not os.path.exists(path)):
            print("ID doesn't exist \n")
            return False

        with open(path, 'r') as file:
            this.__student.setName(file.readline().strip("\n"))
            this.__student.setAge(file.readline())
            
        return this.__student
        
    def delete(this):
        """
        deletes the student object from the database
        """
        path = os.path.join(os.getcwd(), "students")
        path = os.path.join(path, str(this.__student.getId()) + ".student")
        print(path)
        if(not os.path.exists(path)):
            print("ID doesn't exist")
            return False
        
        os.remove(path)
        
        print("Student was deleted successfully \n")
        
    def getAll():
        students = []
        print(os.getcwd())
        for student in os.scandir('students'):
            if student.is_file():
                with open(student.path, 'r') as file:
                    temp = {}
                    temp['id'] = student.name.split('.')[0]
                    temp['name'] = file.readline().strip("\n")
                    temp['age'] = file.readline()
                    students.append(temp)
        return students
        

class Student():
    __slots__ = ['__id', '__name', '__age']
    def __init__(this, id):
        """
        All students must have ids same as their ids in the database.
        New students carry id equals 0 as they have no files in the database yet
        """
        this.__id = id
        

    #getters and setters
    def getId(this):
        return this.__id
    
    def getName(this):
        return this.__name
    
    def getAge(this):
        return this.__age
    
    def setName(this, name):
        this.__name = name
        
    def setAge(this, age):
        this.__age = age
        
        
        

app = Flask(__name__)
cors = CORS(app, resources={r'/*':{'origins':'*'}}, supports_credentials=False)

@app.route("/getAll", methods=['GET', 'OPTIONS'])
def getAll():
    return StudentMapper.getAll()


@app.route("/delete", methods=['POST', 'OPTIONS'])
def delete():
    if(request.method == 'OPTIONS'):
        return "welcome"
    if(request.method == 'POST'):
        id = eval(request.data.decode('UTF-8'))['id']
        checkId = IO.promptStudentID(id)
        if(checkId != "GOOD"):
            return checkId
        student = Student(id)
        student = StudentMapper(student).delete()
        return "GOOD"
    
    
    
@app.route("/create", methods=['POST', 'OPTIONS'])
def create():
    if(request.method == 'OPTIONS'):
        return "welcome"
    if(request.method == 'POST'):
        data = eval(request.data.decode('UTF-8'))
        print(data)
        name, age, id = data['name'], data['age'], data['id']
        checkInfo = IO.promptStudentInfo(name, age)
        if(checkInfo != "GOOD"):
            return checkInfo
        
        checkId = IO.promptStudentID(id)
        if(checkId != "GOOD"):
            return checkId
        
        student = Student(id)
        student.setName(name)
        student.setAge(age)
        return StudentMapper(student).save()
        
        


if __name__ == '__main__':
    app.run(debug=True, port=8080)



# action = IO.promptAction()
# if action == '1':
#     name , age = IO.promptStudentInfo()
#     if(not name):
#         exit()
#     id = IO.promptStudentID()
#     if(not id):
#         exit()
#     student = Student(id)
#     student.setName(name)
#     student.setAge(age)
#     StudentMapper(student).save()
    
# elif action == '2':  
#     id = IO.promptStudentID()
#     if(not id):
#         exit()
#     student = Student(id)
#     student = StudentMapper(student).delete()
        
        
# elif action == '3':
#     id = IO.promptStudentID()
#     if(not id):
#         exit()
#     student = Student(id)
#     student = StudentMapper(student).get()
#     if(student == False):
#         exit()
    
#     IO.showStudent(student)

