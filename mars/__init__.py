import requests
import urllib.request
from flask import Flask, render_template, request, url_for, flash, redirect
from flask_mail import Mail, Message
from datetime import datetime

app=Flask(__name__, static_url_path='/static')
app.secret_key = 'adfglajdfgklj34t3453tgehgstrjj78656treye567'

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'fotosdemarteapi@gmail.com'
app.config['MAIL_PASSWORD'] = 'fotosdemarte'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

@app.route('/')
def index():
	return render_template("index.html")

@app.route('/mandar_correo', methods=['POST','GET'])
def enviar_correo():
	#if request.method == 'POST':
	dest = request.form['correo']
	fecha = request.form['fecha']
	datos= get_mars_photo_url(fecha)
	cuerpo = request.form['mensaje'] + "\n\n\n\n Fecha de la foto:{} \n Sol: {}".format(datos['fecha'],datos['sol'])
	mensaje = Message(cuerpo, sender='uippc4@gmail.com',recipients=[dest])
	mensaje.body = cuerpo
	mensaje.subject = "Hola te enviaron una foto de Marte!"
	archivo= str(datetime.now().strftime('%Y-%m-%d %H-%M-%S')) + ".jpg"
	resource = urllib.request.urlopen(datos['url'])
	output = open(archivo,"wb")
	output.write(resource.read())
	output.close()
	with app.open_resource(archivo) as fp:
		mensaje.attach(archivo, "image/jpg", fp.read())
	mail.send(mensaje)
	flash('Correo Enviado')
	return redirect(url_for('index'))


rover_url = 'https://api.nasa.gov/mars-photos/api/v1/rovers/opportunity/photos'
x = 0
def get_mars_photo_url(earth_date, api_key='EgaAzrAjEeVRHI0VKfEXDmgmAmRPdRfQl8WUuadU'):
	params = { 'earth_date': earth_date, 'api_key': api_key }
	response = requests.get(rover_url, params)
	response_dictionary = response.json()
	photos = response_dictionary['photos']
	for x in range(len(photos)):
		if photos[x]['camera']['name'] == 'PANCAM':
			respuesta = {'url':photos[x]['img_src'],'fecha':photos[x]['earth_date'],'sol':photos[x]['sol']}
			return respuesta
		else:
			x+=1

if __name__ == "__main__":
    app.run()
