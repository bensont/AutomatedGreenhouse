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
                    "`record_number` int(10) NOT NULL AUTO_INCREMENT,"
                    "`lux` float(10,5) NOT NULL,"
                    "`full_spectrum` float(10,5) NOT NULL,"
                    "`infra_red` float(10,5) NOT NULL,"
                    "`air_humidity` float(10,5) NOT NULL,"
                    "`air_temperature` float(10,5) NOT NULL,"
                    "`soil_humidity` float(10,5) NOT NULL,"
                    "`soil_temperature` float(10,5) NOT NULL,"
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
        
    #result = connection.execute("SELECT * FROM *")
        #print(result)