import mysql.connector as mariadb
from mysql.connector import errorcode

Table_Name = "data"
Plant_Table_Name = "plants"
Watering_Table_Name = "waterings"

class DatabaseFacade:
    #pass,user,db,host
    def __init__(self,inpassword,inuser,indatabase,inhost):
        self.connection = mariadb.connect(user=inuser,password=inpassword,host=inhost,database=indatabase)
        self.cursor = self.connection.cursor()
    
    def SetUp(self):
        Tables = {}
        #table to track sensor data from plot
        Tables['Data'] = ("CREATE TABLE " + Table_Name + " ("
                    "`record_number` int(10) NOT NULL AUTO_INCREMENT,"  #0
                    "`lux` float(10,5) NOT NULL,"                       #1
                    "`full_spectrum` float(10,5) NOT NULL,"             #2
                    "`infra_red` float(10,5) NOT NULL,"                 #3
                    "`air_humidity` float(10,5) NOT NULL,"              #4
                    "`air_temperature` float(10,5) NOT NULL,"           #5
                    "`soil_humidity` float(10,5) NOT NULL,"             #6
                    "`soil_temperature` float(10,5) NOT NULL,"          #7
                    "`time_taken` TIMESTAMP DEFAULT CURRENT_TIMESTAMP," #8
            "PRIMARY KEY(`record_number`))")
        
        #table to track plants in the database
        Tables['Plants'] = ("CREATE TABLE " + Plant_Table_Name + " ( "
                            "`plant_number` int(10) NOT NULL AUTO_INCREMENT,"
                            "`name` char(50) NOT NULL,"
                            "`min_light` int(8) NOT NULL,"
                            "`max_light` int(8) NOT NULL,"
                            "`light_minutes` int(8) NOT NULL,"
                            "`min_air_hum` int(8) NOT NULL,"
                            "`max_air_hum` int(8) NOT NULL,"
                            "`min_air_temp` int(8) NOT NULL,"
                            "`max_air_temp` int(8) NOT NULL,"
                            "`water_seconds` int(8) NOT NULL,"
                            "`water_interval_days` int(8) NOT NULL,"
                            "`min_soil_hum` int(8) NOT NULL,"
                            "`max_soil_hum` int(8) NOT NULL,"
                            "`notes` char(200),"
                            "PRIMARY KEY(`plant_number`))"
                            )
        #Table to track when pump is turned on
        Tables['Waterings'] = ("CREATE TABLE " + Watering_Table_Name + " ("
                               "`watering_number` int(16) NOT NULL AUTO_INCREMENT,"
                               "`plant_num` int(10) NOT NULL,"
                               "`time_taken` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,"
                               "PRIMARY KEY(`watering_number`))"
                               )
        
        for table_name in Tables:
            table_description = Tables[table_name]
            try:
                print("Creating Data table")
                message = self.cursor.execute(table_description)
                print(message)
            except mariadb.Error as err:
                if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                    print("Data table already exists")
                else:
                    print(err.msg)
            else:
                print("Created data Table")
    
    def AddSensorRecord(self,data):
        #{0},{1},{2},{3},{4},{5},{6}
        print(data)
        command = ("Insert into " + Table_Name + "  (`lux`,`full_spectrum`,`infra_red`,"
                   "`air_humidity`,`air_temperature`,`soil_humidity`,`soil_temperature`"
                   ") values (%s,%s,%s,%s,%s,%s,%s);")
        #print(command)
        try:
            self.cursor.execute(command,data)
        except mariadb.Error as err:
            print(err.msg)
            
        self.connection.commit()
        
    #This is soley for demonstration purposes and should not be taken as a real plant
    def AddPlantRecords(self):
        command = ("Insert into " +Plant_Table_Name + "(name,min_light,max_light,light_minutes,min_air_hum,max_air_hum,"
                    "min_air_temp,max_air_temp,water_seconds,water_interval_days,min_soil_hum,max_soil_hum,notes)"
                    #name,min max light, light minutes, air humidity
                    "values ('MotherInLawsTongue',90,600,720,60,100,"
                   #air temp, watering, soil moisture, notes
                    "18,32,30,0,400,700,'Its a test plant')")
        try:
            self.cursor.execute(command)
        except mariadb.Error as err:
            print(err.msg)
            
        self.connection.commit()
    
    def GetPlantInfo(self,plantnum):
        command = ("SELECT * FROM " +Plant_Table_Name + " WHERE plant_number = "+str(plantnum))
        self.cursor.execute(command)
        #try:
        #    self.cursor.execute(command)
        #except mariadb.Error as err:
        #    print(err.msg)
        #    print("error")
        for row in self.cursor:
            print(row)
            print("Here")
            name = row[1]
            minlight = row[2]
            maxlight = row[3]
            lightmin = row[4]
            minairhum = row[5]
            maxairhum = row[6]
            minairtemp = row[7]
            maxairtemp = row[8]
            waterseconds = row[9]
            waterinterval = row[10]
            minsoilmoist = row[11]
            maxsoilmoist = row[12]
            return(name,minlight,maxlight,lightmin,minairhum,maxairhum,minairtemp,maxairtemp,waterseconds,waterinterval,minsoilmoist,maxsoilmoist)
        
    
    def Close(self):
        self.cursor.close()
        self.connection.close()

    def GetLastData(self):
        query = ("SELECT * FROM " + Table_Name + "  ORDER BY record_number DESC LIMIT 1")
        self.cursor.execute(query)
        for row in self.cursor:
            time = row[8]
            temp = row[5]
            hum = row[4]
            soil = row [6]
            light = row [1] 
        return time,temp,hum,soil,light

    def GetHistData(self, numSamples):
        query = ("SELECT * FROM " + Table_Name + "  ORDER BY record_number DESC LIMIT "+str(numSamples))
        self.cursor.execute(query)
        dates = []
        temps = []
        hums = []
        soils = []
        lights = []
        data = self.cursor.fetchall()
        for row in reversed(data):
            dates.append(row[8])
            temps.append(row[5])
            hums.append(row[4])
            soils.append(row[6])
            lights.append(row[1])
        return dates, temps, hums, soils, lights

    def MaxRowsTable(self):
        query = ("SELECT count(*) from " + Table_Name + " ")
        self.cursor.execute(query)
        for x in self.cursor:
            print(x)
            return x[0]
        #number of rows


    #result = connection.execute("SELECT * FROM *")
        #print(result)