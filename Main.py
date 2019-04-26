import DatabaseConnection as DBC
import webapp
import Plot
import time
import threading

global running

def main():
    #pass,user,db,host
    db = DBC.DatabaseFacade('ooad','plant','OOADProject','127.0.0.1')
    #These are not default to be run
    #db.SetUp()
    #db.AddPlantRecords()
    
    running = True

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
    
    u = threading.Thread(target=userListner,args=(db,conditionalvar,))
    threads.append(u)
    u.start()

    #there is an implicit wait here
    #db.close()

#a function to set up the webapp
def setUpWebApp(database,cv):
    #unclear if a conditional variable is required
    webapp.create(database,36636,cv)

#the timing data service
def setUpDataService(database,cv):
    plot = Plot.Plot(database,cv,1)

    start = time.time()
    count = 0
    while(running):
        if(time.time()-start > 3):
            plot.get_condition()
            plot.check_condition()
            with cv:
                database.AddSensorRecord(plot.return_current())
                start = time.time()
                cout = count+1
                cv.notifyAll()
            print(count)

def userListner(database,cv):
    while(running):
        #try to listen to the user
        test = input("Press q to quit")
        if(test == "q"):
            running = False
            with cv:
                database.close()
    
    
if __name__ == "__main__":
    main()