import mysql.connector as mariadb
from mysql.connector import errorcode

class DatabaseFacade:
    #pass,user,db,host
    def __init__(self,inpassword,inuser,indatabase,inhost):
        self.connection = mariadb.connect(user=inuser,password=inpassword,host=inhost,database=indatabase)
        self.cursor = self.connection.cursor()
    
    def SetUp(self):
        Tables = {}
        Tables['Data'] = ("CREATE TABLE `data` (`record_number` int(10) NOT NULL AUTO_INCREMENT,`temperature` float(10,5) NOT NULL, PRIMARY KEY(`record_number`))")
        
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
    
    def AddSensorRecord(self,Data):
        command = ("Insert into `data` (`temperature`) values (6);")
        try:
            self.cursor.execute(command)
        except mariadb.Error as err:
            print(err.msg)
            
        self.connection.commit()
    
    def Close(self):
        self.cursor.close()
        self.connection.close()
        
    #result = connection.execute("SELECT * FROM *")
        #print(result)