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
        numSamples = (numMaxSamples-1)
    time, temp, hum, soil, light = getLastData()
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
    times, temps, hums, soils, lights = db.GetHistData(numSamples)
    ys = temps
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    axis.set_title("Temperature [C]")
    axis.set_xlabel("Samples")
    axis.grid(True)
    xs = range(numSamples)
    axis.plot(xs, ys)
    canvas = FigureCanvas(fig)
    output = io.BytesIO()
    canvas.print_png(output)
    response = make_response(output.getvalue())
    response.mimetype = 'image/png'
    return response

@app.route('/plot/hum')
def plot_hum():
    times, temps, hums, soils, lights = db.GetHistData(numSamples)
    ys = hums
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    axis.set_title("Humidity [%]")
    axis.set_xlabel("Samples")
    axis.grid(True)
    xs = range(numSamples)
    axis.plot(xs, ys)
    canvas = FigureCanvas(fig)
    output = io.BytesIO()
    canvas.print_png(output)
    response = make_response(output.getvalue())
    response.mimetype = 'image/png'
    return response

@app.route('/plot/soil')
def plot_soil():
    times, temps, hums, soils, lights = db.GetHistData(numSamples)
    ys = soils
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    axis.set_title("Soil Moisture")
    axis.set_xlabel("Samples")
    axis.grid(True)
    xs = range(numSamples)
    axis.plot(xs, ys)
    canvas = FigureCanvas(fig)
    output = io.BytesIO()
    canvas.print_png(output)
    response = make_response(output.getvalue())
    response.mimetype = 'image/png'
    return response

@app.route('/plot/light')
def plot_light():
    times, temps, hums, soils, lights = db.GetHistData(numSamples)
    ys = lights
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    axis.set_title("Light Intensity")
    axis.set_xlabel("Samples")
    axis.grid(True)
    xs = range(numSamples)
    axis.plot(xs, ys)
    canvas = FigureCanvas(fig)
    output = io.BytesIO()
    canvas.print_png(output)
    response = make_response(output.getvalue())
    response.mimetype = 'image/png'
    return response

if __name__ == "__main__":
   app.run(host='0.0.0.0', port=36636, debug=False)