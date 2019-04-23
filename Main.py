import DatabaseConnection as DBC
import webapp
import Plot
import time
import threading

def main():
    #pass,user,db,host
    db = DBC.DatabaseFacade('ooad','plant','OOADProject','127.0.0.1')
    db.SetUp()
    plot = Plot.Plot('Sensor1', 'Test', 10, 10, 10, 10, 10, 10, 10, 10, 'None', cur_airTemp = None, cur_humidity = None, cur_moisture = None, cur_soilTemp = None, cur_light_full = None, cur_light_ir = None, cur_light_lux = None)
    
    conditionalvar = threading.Condition()

    #create the web app as a thread
    t = threading.Thread(target=setUpWebApp,args=(conditionalvar,))
    threads.append(t)
    t.start()

    #create a thread does data input
    d = threading.Thread(target=setUpDataService,args=(conditionalvar,))
    threads.append(d)
    d.start()
    
    #there is an implicit wait here
    

def setUpWebApp(cv):
    #unclear if a conditional variable is required
    webapp.create(db,36636,cv)

def setUpDataService(cv):
    start = time.time()
    running = 0
    while(running < 3):
        if(time.time()-start > 3):
            with cv:
                plot.get_condition()
                db.AddSensorRecord(plot.return_current())
                start = time.time()
                running = running+1
                cv.notifyAll()

    db.close()
    
    
if __name__ == "__main__":
    main()