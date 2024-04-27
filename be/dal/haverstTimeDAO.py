import mysql.connector
from dal.DBContext import host,username,passwd,database
class HarvestTime:
    def __init__(self,id,time_start,time_end,harvest_yield,id_plant,id_employee_confirm):
        self.id = id
        self.time_start = time_start
        self.time_end = time_end
        self.harvest_yield = harvest_yield
        self.id_plant = id_plant
        self.id_employee_confirm = id_employee_confirm
    def to_dict(self):
        return{
            "id":self.id,
            "time_start": self.time_start,
            "time_end":self.time_end,
            "harvest_yield": self.harvest_yield,
            "id_plant": self.id_plant,
            "id_employee_confirm" :self.id_employee_confirm
        }
def getHarvestTimeByIdPlant(idPlant):
    db = mysql.connector.connect(
        host=host,
        user=username,
        passwd=passwd,
        database=database
    )
    myCursor = db.cursor()
    sql = "SELECT * FROM iot.harvest_time WHERE id_plant =%s"
    myCursor.execute(sql,(idPlant,))
    records =[]
    for item in myCursor:
        records.append(HarvestTime(item[0],item[1],item[2],item[3],item[4],item[5]).to_dict())
    return records
import mysql.connector

def saveHarvest(time_start, time_end, harvest_yield, average_temp, average_hum, average_light, average_soil, id_plant):
    # Connect to the database
    db = mysql.connector.connect(
        host=host,
        user=username,
        passwd=passwd,
        database=database
    )
    
    # Create a cursor object to interact with the database
    myCursor = db.cursor()

    # Define the SQL query
    sql = "INSERT INTO iot.harvest_time (time_start, time_end, harvest_yield, average_temp, average_hum, average_light, average_soil, id_plant) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"

    # Execute the query with parameterized values
    myCursor.execute(sql, (time_start, time_end, harvest_yield, average_temp, average_hum, average_light, average_soil, id_plant))

    # Commit the transaction
    db.commit()

    # Close cursor and database connection
    myCursor.close()
    db.close()

    print("Data saved successfully.")
    return "Success"
