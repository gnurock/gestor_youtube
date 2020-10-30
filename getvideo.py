from flask import Flask,render_template, redirect,url_for,request
import urllib, urllib2
from lxml import etree
from StringIO import StringIO
from bs4 import BeautifulSoup as BS

#from pytube import YouTube  
import pytube

    
app= Flask(__name__)


@app.route("/")
def main():
	return render_template('index.html');


#regresa n  (1-10) sugerencias de videos con nombres, img previa (thumnail)   
def buscarRecomendados(query, n=5):
	print "buscar recomendaiones"
	req=urllib2.Request(query,headers={'User-agent':'Mozila/5.0'})
	f = urllib2.urlopen(req)
       #time.sleep(10);
	html = f.read()
	soup= BS(html) 
	soup.prettify('latin-1')[1:1000]
	relacionados=soup.find(id="content")
 	#relacionados=rela.findAll("li",{"class":"video-list-item"})
	links=relacionados.findAll("a",{"class":"yt-uix-sessionlink"})	
	#print links
	return links[n]




def Descargar(linkVideo):
	print "inicio descarga"+linkVideo
	video=pytube.YouTube(linkVideo)
	video.streams.first().download("/home/gnusyscamus/desarrollo/web/proyecto_youtube/static/multimedia")
	print "finaliza descarga"+linkVideo


@app.route('/descarga',methods = ['POST','GET'])
def descarga():
	##default query hardcore
	#es una lista de sugerencias que se va rendirizar 
	# en el template con nombre video, duracion,link oculto,img de vista previa
	print "descargar todos"
	sugerencias=[]
	query="https://www.youtube.com/watch?v=c0aQkYxjMdI"
	if request.method == 'POST':
		query = request.form['query'];
		#converterir query a string
		query= query.encode('ascii','ignore')
	
	#regresa con una lista links de recomendaciones
	#listaRecomendaciones=buscarRecomendados(query,5)
	#print str(len(listaRecomendaciones))+"recomendaciones"
	video = pytube.YouTube(query)

	sugerencia=(video.title,video.length,video.thumbnail_url,query)
	sugerencias.append(sugerencia)
	#agregar la primera sugerencia
	#for linkVideo in listaRecomendaciones:
	for i in range (0,3):
		#linkVideo=linkVideo.encode('ascii','ignore')
		videoSugerencia=pytube.YouTube("https://www.youtube.com/watch?v=aVV1wK61qxA")
		titulo=videoSugerencia.title
		titulo=titulo.encode('ascii','ignore')
		duracion=videoSugerencia.length
		duracion=duracion.encode('ascii','ignore')
		thumbnail_url=videoSugerencia.thumbnail_url 
		thumbnail_url=thumbnail_url.encode('ascii','ignore')
		print titulo,duracion
		sugerencia=(titulo,duracion,thumbnail_url,"https://www.youtube.com/watch?v=3zrHRfkF2c0")
		sugerencias.append(sugerencia)
	print sugerencias
	return render_template('index.html',sugerencias=sugerencias)

if __name__ == '__main__':
	app.run();