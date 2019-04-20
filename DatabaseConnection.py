import mysql.connector as mariadb
from mysql.connector import errorcode

class DatabaseFacade:
    #pass,user,db,host
    def __init__(self,inpassword,inuser,indatabase,inhost):
        self.connection = mariadb.connect(user=inuser,password=inpassword,host=inhost,database=indatabase)
        self.cursor = self.connection.cursor()
    
    def SetUp(self):
        Tables = {}
        Tables['Data'] = ("CREATE TABLE `data` ("
                    "`record_number` int(10) NOT NULL AUTO_INCREMENT,"  #0
                    "`lux` float(10,5) NOT NULL,"                       #1
                    "`full_spectrum` float(10,5) NOT NULL,"             #2
                    "`infra_red` float(10,5) NOT NULL,"                 #3
                    "`air_humidity` float(10,5) NOT NULL,"              #4
                    "`air_temperature` float(10,5) NOT NULL,"           #5
                    "`soil_humidity` float(10,5) NOT NULL,"             #6
                    "`soil_temperature` float(10,5) NOT NULL,"          #7
            "PRIMARY KEY(`record_number`))")
        
        for table_name in Tables:
            table_description = Tables[table_name]
            try:
                print("Creating Table")
                self.cursor.execute(table_description)
            except mariadb.Error as err:
                if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                    print("Table already exists")
                else:
                    print(err.msg)
            else:
                print("Created Table")
    
    def AddSensorRecord(self,data):
        #{0},{1},{2},{3},{4},{5},{6}
        print(data)
        command = ("Insert into `data` (`lux`,`full_spectrum`,`infra_red`,"
                   "`air_humidity`,`air_temperature`,`soil_humidity`,`soil_temperature`"
                   ") values (%s,%s,%s,%s,%s,%s,%s);")
        #print(command)
        try:
            self.cursor.execute(command,data)
        except mariadb.Error as err:
            print(err.msg)
            
        self.connection.commit()
    
    def Close(self):
        self.cursor.close()
        self.connection.close()

    def GetLastData(self):
        query = ("SELECT * FROM data ORDER BY record_number DESC LIMIT 1")
        self.cursor.execute(query)
        for row in self.cursor:
            time = row[0]
            temp = row[5]
            hum = row[4]
            soil = row [6]
            light = row [1] 
        return time,temp,hum,soil,light

    def GetHistData(self, numSamples):
        query = ("SELECT * FROM data ORDER BY record_number DESC LIMIT "+str(numSamples))
        self.cursor.execute(query)
        dates = []
        temps = []
        hums = []
        soils = []
        lights = []
        data = self.cursor.fetchall()
        for row in reversed(data):
            dates.append(row[0])
            temps.append(row[5])
            hums.append(row[4])
            soils.append(row[6])
            lights.append(row[1])
        return dates, temps, hums, soils, lights

    def MaxRowsTable(self):
        query = ("SELECT count(*) from data")
        self.cursor.execute(query)
        for x in self.cursor:
            print(x)
            return x[0]
        #number of rows


    #result = connection.execute("SELECT * FROM *")
        #print(result)