from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import io
import DatabaseConnection as DBC

from flask import Flask, render_template, send_file, make_response, request
app = Flask(__name__)

class Holder:
    datab = None
    NumSamples = 0
    condv = None
    
    @staticmethod
    def SetDataBase(db):
        Holder.datab = db
    
    @staticmethod
    def GetLastData():
        return Holder.datab.GetLastData()
    
    @staticmethod
    def SetNumSamples():
        Holder.NumSamples = Holder.datab.MaxRowsTable()
        if (Holder.NumSamples > 101):
            Holder.NumSamples = 100
            
    @staticmethod
    def numSamples():
        return Holder.NumSamples
    
    @staticmethod
    def SetCondVar(condvar):
        Holder.condv = condvar
        
    @staticmethod
    def cv():
        return Holder.condv
    
    @staticmethod
    def GetHistData():
        return Holder.datab.GetHistData(Holder.numSamples())


# main route
@app.route("/")
def index():
    with Holder.cv():
        time, temp, hum, soil, light = Holder.GetLastData()
        num = Holder.numSamples()
        Holder.cv().notifyAll()
    templateData = {
        'time'  : time,
        'temp'  : temp,
        'hum'   : hum,
        'soil'  : soil,
        'light' : light,
        'numSamples'    : num
    }
    return render_template('index.html', **templateData)

@app.route('/', methods=['POST'])
def my_form_post():
    numMaxSamples = Holder.MaxRowsTable()
    if (Holder.numSamples() > numMaxSamples):
        Holder.SetNumSamples = (numMaxSamples)
    with Holder.cv():
        time, temp, hum, soil, light = Holder.GetLastData()
        Holder.cv().notifyAll()
    templateData = {
        'time'  : time,
        'temp'  : temp,
        'hum'   : hum,
        'soil' : soil,
        'light' : light,
        'numSamples'    : Holder.numSamples()
    }
    return render_template('index.html', **templateData)

@app.route('/plot/temp')
def plot_temp():
    return create_plot("Temperature [C]",1)

@app.route('/plot/hum')
def plot_hum():
    return create_plot("Humidity [%]",2)

@app.route('/plot/soil')
def plot_soil():
    return create_plot("Soil Moisture",3)

@app.route('/plot/light')
def plot_light():
    return create_plot("Light Intensity",4)

def create_plot(title,ys):
    #data is dates, temps, humidity, soil, lights
    with Holder.cv():
        data = Holder.GetHistData()
        Holder.cv().notifyAll()
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    axis.set_title(title)
    axis.set_xlabel("Samples")
    axis.grid(True)
    xs = range(Holder.numSamples())
    axis.plot(xs, data[ys])
    canvas = FigureCanvas(fig)
    output = io.BytesIO()
    canvas.print_png(output)
    response = make_response(output.getvalue())
    response.mimetype = 'image/png'
    return response


def create(indb,runport,condvar):
    Holder.SetDataBase(indb)
    Holder.SetCondVar(condvar)
    Holder.SetNumSamples()
    app.run(host='0.0.0.0', port=runport, debug=False)

if __name__ == "__main__":
   app.run(host='0.0.0.0', port=36636, debug=False)