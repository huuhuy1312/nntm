from datetime import datetime
import mysql.connector
from dal.DBContext import host,username,passwd,database
class Task:
    def __init__(self, id, id_user, time_receive, title,desciption,deadline,status,cancelReason):
        self.id=id
        self.id_user=id_user
        self.time_receive=time_receive
        self.title=title
        self.desciption = desciption
        self.deadline = deadline
        self.status = status
        self.cancelReason = cancelReason
    def to_dict(self):
        return{
            "id": self.id,
            "id_user": self.id_user,
            "time_receive": self.time_receive,
            "title": self.title,
            "description":self.desciption,
            "deadline": self.deadline,
            "status" : self.status,
            "cancelReason" : self.cancelReason
        }
def insertTask(data):

    db = mysql.connector.connect(
        host=host,
        user=username,
        passwd=passwd,
        database=database
    )
    myCursor = db.cursor()
    
    sql = "INSERT INTO iot.tasks (id_user, title, description, deadline,status) VALUES (%s , %s, %s, %s,%s)"
    deadline = datetime.strptime(data['deadline'], '%Y-%m-%dT%H:%M:%S.%fZ')
    task_data = (data['id_user'], data['title'], data['description'], deadline,"chua_nhan")
    myCursor.execute(sql, task_data)
    db.commit()
def getAllAcceptedTasks():
    db = mysql.connector.connect(
        host=host,
        user=username,
        passwd=passwd,
        database=database
    )
    myCursor = db.cursor()
    sql = "SELECT * FROM iot.tasks where status='chua_hoan_thanh' "
    myCursor.execute(sql)
    record =[]
    for item in myCursor:
        record.append(Task(item[0],item[1],item[2],item[3],item[4],item[5],item[6],item[7]))
    print(record)
    return record
def getAllClaimedTasks():
    db = mysql.connector.connect(
        host=host,
        user=username,
        passwd=passwd,
        database=database
    )
    myCursor = db.cursor()
    sql = "SELECT * FROM iot.tasks where status='chua_nhan'"
    myCursor.execute(sql)
    record =[]
    for item in myCursor:
        record.append(Task(item[0],item[1],item[2],item[3],item[4],item[5],item[6],item[7]))
    print(record)
    return record
def getAllDeniedTasks():
    db = mysql.connector.connect(
        host=host,
        user=username,
        passwd=passwd,
        database=database
    )
    myCursor = db.cursor()
    sql = "SELECT * FROM iot.tasks where status='bi_tu_choi'"
    myCursor.execute(sql)
    record =[]
    for item in myCursor:
        record.append(Task(item[0],item[1],item[2],item[3],item[4],item[5],item[6],item[7]))
    print(record)
    return record
def getClaimedTasksByUserId(userID):
    db = mysql.connector.connect(
        host=host,
        user=username,
        passwd=passwd,
        database=database
    )
    myCursor = db.cursor()
    sql = "SELECT * FROM iot.tasks where id_user=%s and status='chua_nhan'";
    myCursor.execute(sql,(userID,))
    record =[]
    for item in myCursor:
        record.append(Task(item[0],item[1],item[2],item[3],item[4],item[5],item[6],item[7]))
    print(record)
    return record
def getAcceptedTasksByUserId(userID):
    db = mysql.connector.connect(
        host=host,
        user=username,
        passwd=passwd,
        database=database
    )
    myCursor = db.cursor()
    sql = "SELECT * FROM iot.tasks where id_user=%s and status='chua_hoan_thanh' order by deadline"
    myCursor.execute(sql,(userID,))
    record =[]
    for item in myCursor:
        record.append(Task(item[0],item[1],item[2],item[3],item[4],item[5],item[6],item[7]))
    print(record)
    return record
def get_current_time():
    return datetime.now()

def getAcceptedTodayTasksByUserId(userID):
    db = mysql.connector.connect(
        host=host,
        user=username,
        passwd=passwd,
        database=database
    )
    myCursor = db.cursor()
    sql = "SELECT * FROM iot.tasks WHERE id_user=%s AND status='chua_hoan_thanh' AND DATE(deadline) = CURDATE()"
    myCursor.execute(sql, (userID,))
    record = []
    for item in myCursor:
        record.append(Task(item[0], item[1], item[2], item[3], item[4], item[5], item[6], item[7]))
    print(record)
    return record

def acceptTaskByTaskId(taskId):
    db = mysql.connector.connect(
        host=host,
        user=username,
        passwd=passwd,
        database=database
    )
    myCursor = db.cursor()
    current_time = get_current_time()
    sql = "UPDATE iot.tasks SET time_receive = %s, status = 'chua_hoan_thanh' WHERE id = %s"
    myCursor.execute(sql, (current_time, taskId))
    db.commit()
    db.close()
def completeTaskByTaskId(taskId):
    db = mysql.connector.connect(
        host=host,
        user=username,
        passwd=passwd,
        database=database
    )
    myCursor = db.cursor()
    print(taskId)
    sql = "UPDATE iot.tasks SET status = 'hoan_thanh' WHERE id = %s"
    myCursor.execute(sql, (taskId,))
    db.commit()
    db.close()
def deniedTaskByTaskId(taskId,reason):
    db = mysql.connector.connect(
        host=host,
        user=username,
        passwd=passwd,
        database=database
    )
    myCursor = db.cursor()
    sql = "UPDATE iot.tasks SET reasonCancel=%s, status = 'bi_tu_choi' WHERE id = %s"
    myCursor.execute(sql, (reason, taskId))
    db.commit()
    db.close()
def getNameByUserId(userId):
    db = mysql.connector.connect(
        host=host,
        user=username,
        passwd=passwd,
        database=database
    )
    myCursor = db.cursor()
    sql ="SELECT name from iot.users where id =%s"
    myCursor.execute(sql,(userId,))
    result = myCursor.fetchone()
    db.close()
    if result:
        return result[0]
    else:
        return None 
# Example data

