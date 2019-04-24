import DatabaseConnection as DBC
import webapp
import Plot
import time
import threading

def main():
    #pass,user,db,host
    db = DBC.DatabaseFacade('ooad','plant','OOADProject','127.0.0.1')
    #db.SetUp()
    
    threads = []
    
    conditionalvar = threading.Condition()

    #create the web app as a thread
    t = threading.Thread(target=setUpWebApp,args=(db,conditionalvar,))
    threads.append(t)
    t.start()

    #create a thread does data input
    d = threading.Thread(target=setUpDataService,args=(db,conditionalvar,))
    threads.append(d)
    d.start()
    
    #there is an implicit wait here
    #db.close()

def setUpWebApp(database,cv):
    #unclear if a conditional variable is required
    webapp.create(database,36636,cv)

def setUpDataService(database,cv):
    plot = Plot.Plot('Sensor1', 'Test', 10, 10, 10, 10, 10, 10, 10, 10, 'None', cur_airTemp = None, cur_humidity = None, cur_moisture = None, cur_soilTemp = None, cur_light_full = None, cur_light_ir = None, cur_light_lux = None)
    
    start = time.time()
    running = 0
    while(running < 3):
        if(time.time()-start > 3):
            plot.get_condition()
            plot.check_condition()
            with cv:
                database.AddSensorRecord(plot.return_current())
                start = time.time()
                running = running+1
                cv.notifyAll()

    
    
if __name__ == "__main__":
    main()