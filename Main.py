import DatabaseConnection as DBC
import webapp
import Plot
import time
import threading


def main():
    #pass,user,db,host
    db = DBC.DatabaseFacade('ooad','plant','OOADProject','127.0.0.1')
    #need to add an appropriate check to setting up the database
    #db.SetUp()
    #db.AddPlantRecords()
    #return
    
    threads = []
    
    conditionalvar = threading.Condition()

    isrun = True

    running = threading.Condition()

    #create the web app as a thread
    t = threading.Thread(target=setUpWebApp,args=(db,conditionalvar,isrun,running))
    threads.append(t)
    t.start()

    #create a thread does data input
    d = threading.Thread(target=setUpDataService,args=(db,conditionalvar,isrun,running))
    threads.append(d)
    d.start()
    
    u = threading.Thread(target=userListner,args=(db,conditionalvar,isrun,running))
    threads.append(u)
    u.start()


    #there is an implicit wait here
    #db.close()

def setUpWebApp(database,cv,run,running):
    #unclear if a conditional variable is required
    webapp.create(database,36636,cv)
    #this doesn't check right now

def setUpDataService(database,cv,run,running):
    plot = Plot.Plot(database,cv,1)

    start = time.time()
    count = 0
    with run:
        while(running):
            run.notifyAll()
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

def userListner(database,cv,run,running):
    with run:
        while (running):
            run.notifyAll()
            test = input("Type q to quit")
            if(test == 'q'):
                with cv:
                    with run:
                        running = false
                        run.notifyAll()
                    database.close()
                    cv.notifyAll()
    
if __name__ == "__main__":
    main()