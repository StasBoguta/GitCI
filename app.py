from flask import Flask
from flask import request
from flask import jsonify
import uuid
import pymongo
import json
import redis

myclient = pymongo.MongoClient("mongodb://mongohost:27017/")
mydb = myclient["mydatabase"]
mycol = mydb["customers"]

app = Flask(__name__)

r = redis.Redis(host="redishost", port=6379)


def to_obj(name, surname, course):
    obj = {
        "name": name,
        "surname": surname,
        "course": course,
        "id": str(uuid.uuid4())
    }
    return obj


@app.route("/")
def hello():
    return r.get("A")

students = []

@app.route("/addStudent", methods=['POST'])
def addStudent():
    body = request.json
    student = to_obj(body["name"], body["surname"], body["course"])
    student_id = student["id"]
    mycol.insert_one(student)
    out = mycol.find_one({"id": student_id},{ "_id": 0, "name": 1, "surname": 1, "course": 1, "id":1 })
    return jsonify(out)


@app.route("/getStudents", methods=['GET'])
def getStudents():
    out = []
    for x in mycol.find({},{ "_id": 0, "name": 1, "surname": 1, "course": 1, "id":1 }):
        out.append(x)
    print(out)
    response = {"students": out}
    return jsonify(response)

@app.route("/getStudentById", methods=['GET'])
def getStudent():
    request_id = str(request.json["id"])
    student = r.get(request_id)
    if student is None:
        out = mycol.find_one({"id": request_id},{ "_id": 0, "name": 1, "surname": 1, "course": 1, "id":1 })
        r.set(request_id, str(out))
        out = {"type": "from database", "student": [out]}
        return jsonify(out)
    student = student.decode()
    student = student.replace("'", "\"")
    student = json.loads(student)
    return jsonify({"type":"from cache", "student":[student]})


def some_method_for_test(n):
    return n*2

@app.route("/deleteAll", methods=['DELETE'])
def deleteAll():
    mycol.delete_many({})
    return "Deleted"

if __name__ == '__main__':
    app.run()