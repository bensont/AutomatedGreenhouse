from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import io
import DatabaseConnection as DBC

from flask import Flask, render_template, send_file, make_response, request
app = Flask(__name__)

db = DBC.DatabaseFacade('LongPassword','Web','OOADProject','127.0.0.1')
# define and initialize global variables
global numSamples
numSamples = db.MaxRowsTable()
if (numSamples > 101):
    numSamples = 100

# main route
@app.route("/")
def index():
    time, temp, hum, soil, light = db.GetLastData()
    templateData = {
        'time'  : time,
        'temp'  : temp,
        'hum'   : hum,
        'soil'  : soil,
        'light' : light,
        'numSamples'    : numSamples
    }
    return render_template('index.html', **templateData)

@app.route('/', methods=['POST'])
def my_form_post():
    global numSamples
    numSamples = int (request.form['numSamples'])
    numMaxSamples = db.MaxRowsTable()
    if (numSamples > numMaxSamples):
        numSamples = (numMaxSamples)
    time, temp, hum, soil, light = db.GetLastData()
    templateData = {
        'time'  : time,
        'temp'  : temp,
        'hum'   : hum,
        'soil' : soil,
        'light' : light,
        'numSamples'    : numSamples
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
    data = db.GetHistData(numSamples)
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    axis.set_title(title)
    axis.set_xlabel("Samples")
    axis.grid(True)
    xs = range(numSamples)
    axis.plot(xs, data[ys])
    canvas = FigureCanvas(fig)
    output = io.BytesIO()
    canvas.print_png(output)
    response = make_response(output.getvalue())
    response.mimetype = 'image/png'
    return response


def create(indb,runport):
    db = indb
    app.run(host='0.0.0.0', port=runport, debug=False)

if __name__ == "__main__":
   app.run(host='0.0.0.0', port=36636, debug=False)