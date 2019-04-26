import DatabaseConnection as DBC
import webapp
import Plot
import time
import threading

global running

def main():
    #pass,user,db,host
    db = DBC.DatabaseFacade('ooad','plant','OOADProject','127.0.0.1')
    #need to add an appropriate check to setting up the database
    #db.SetUp()
    #db.AddPlantRecords()
    #return
    
    threads = []
    
    conditionalvar = threading.Condition()

    running = True

    #create the web app as a thread
    t = threading.Thread(target=setUpWebApp,args=(db,conditionalvar,))
    threads.append(t)
    t.start()

    #create a thread does data input
    d = threading.Thread(target=setUpDataService,args=(db,conditionalvar,))
    threads.append(d)
    d.start()
    
    u = threading.Thread(target=userListner,args=(db,conditionalvar,))
    threads.append(u)
    u.start()


    #there is an implicit wait here
    #db.close()

def setUpWebApp(database,cv):
    #unclear if a conditional variable is required
    webapp.create(database,36636,cv)

def setUpDataService(database,cv):
    plot = Plot.Plot(database,cv,1)

    start = time.time()
    count = 0
    while(running):
        if(time.time()-start > 3):
            if (count%3 == 0):
                plot.camera_facade.Take_Picture()
            plot.get_condition()
            plot.check_condition()
            with cv:
                database.AddSensorRecord(plot.return_current())
                start = time.time()
                count = count+1
                cv.notifyAll()
    plot.relay_facade.AllOff()

def userListner(database,cv):
    while (running):
        test = input("Type q to quit")
        if(test == 'q'):
            with cv:
                running = false
                database.close()
                cv.notifyAll()
    
if __name__ == "__main__":
    main()