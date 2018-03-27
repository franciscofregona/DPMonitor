from flask import Flask

from trabajo import aux_trabajos
from antiguo import aux_antiguo
from mediosvtl import aux_mediosVtl
from antiguos import aux_antiguos
from listasources import listaSources

app = Flask(__name__)


app.config['DEBUG']=True
#app.config['SERVER_NAME']='10.1.4.74:5000'

#@app.route("/")
#def hello():
#    return "Hello, I love Digital Ocean!"

@app.route("/")
@app.route("/trabajo")
def trabajo():
    return aux_trabajos()

@app.route("/antiguo/")
def antiguo():
    return aux_antiguo()

@app.route("/medios/")
def medios():
    return aux_mediosVtl()

@app.route("/antiguos/")
def antiguos():
    return aux_antiguos()

@app.route("/listasources/")
def listasources():
	return listaSources()

if __name__ == "__main__":
    app.run()