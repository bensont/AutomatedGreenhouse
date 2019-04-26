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
    
    #This holds all of the threads
    threads = []
    #conditional variable to protect the database
    conditionalvar = threading.Condition()
    #a sentinal for running the app
    running = True
    #conditional varialbe to protect the sentinel
    isrun = threading.Condition()

    #create the web app as a thread
    t = threading.Thread(target=setUpWebApp,args=(db,conditionalvar,isrun,running))
    threads.append(t)
    t.start()

    #create a thread does data input
    d = threading.Thread(target=setUpDataService,args=(db,conditionalvar,isrun,running))
    threads.append(d)
    d.start()
    
    #create a thread that listens to the user
    u = threading.Thread(target=userListner,args=(db,conditionalvar,isrun,running))
    threads.append(u)
    u.start()


    #there is an implicit wait here
    #db.close()

#Tiny function to launch the webapp
def setUpWebApp(database,cv,isrun,running):
    #unclear if a conditional variable is required
    webapp.create(database,36636,cv)
    #this doesn't check right now

#Thread to gather data
def setUpDataService(database,cv,isrun,running):
    plot = Plot.Plot(database,cv,1)

    start = time.time()
    count = 0
    with isrun:
        local = running
        isrun.notifyAll()
    while(local):
        with isrun:
            local = running
            isrun.notifyAll()
        if(local):
            #Only gather data every 3 seconds
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

#thread to listen to uster
def userListner(database,cv,isrun,running):
    with isrun:
        local = running
        isrun.notifyAll()
    while (local):
        test = input("Type q to quit")
        if(test == 'q'):
            with cv:
                with isrun:
                    running = False
                    isrun.notifyAll()
                database.close()
                cv.notifyAll()

#default python convetion
if __name__ == "__main__":
    main()