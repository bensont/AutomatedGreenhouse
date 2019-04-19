import DatabaseConnection as DBC
import Plot
import time

def main():
    #pass,user,db,host
    db = DBC.DatabaseFacade('ooad','plant','OOADProject','127.0.0.1')
    db.SetUp()
    plot = Plot.Plot('Sensor1', 'Test', 10, 10, 10, 10, 10, 10, 10, 10, 'None', cur_airTemp = None, cur_humidity = None, cur_moisture = None, cur_soilTemp = None, cur_light_full = None, cur_light_ir = None, cur_light_lux = None)
    
    start = time.time()
    running = 0
    while(running < 10):
        if(time.time()-start > 3):
            plot.get_condition()
            db.AddSensorRecord(plot.return_current())
            start = time.time()
            running = running+1
    
    db.Close()
    
    
if __name__ == "__main__":
    main()