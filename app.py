import os
from flask import (Flask, render_template, url_for,
	request, send_file, send_from_directory, redirect, flash)
import pyttsx3
from gtts import gTTS
import os.path as path

app = Flask(__name__)
app.config['SECRET_KEY'] = 'acitnigeria@yuseehabibu1998.com'
save_uri = path.dirname(path.abspath(__file__))

def convert_txt_to_mp3(txt:str, fn=None):
	if not fn:
		fn = 'Audio'
	else:
		fn, _= path.splitext(fn)
	fn = fn + '.mp3'
	audPath = save_uri + '/static/audio/' + fn
	engine = gTTS(text=txt, lang='en-ng', slow=True)
	engine.save(audPath)
	return fn

@app.route('/')
@app.route('/home')
def home():
	return render_template('home.html')

@app.route('/get_audio', methods=['POST','GET'])
def get_audio():
	if request.method == 'POST':
		txt_data = request.form.get('text')
		txt_file = request.files.get('txt_file')
		if txt_data and txt_file:
			txt_file = None
			fname = convert_txt_to_mp3(txt_data)
		elif txt_data:
			fname = convert_txt_to_mp3(txt_data)
		elif txt_file:
			fd = txt_file.read().decode('utf8')
			fname = txt_file.filename
			fname = convert_txt_to_mp3(fd, fname)
	return render_template('audio.html', fname=fname)


@app.route('/delete/<fn>')
def delete(fn):
	try:
		os.remove(save_uri + '/static/audio/' + fn)
		flash("Audio file was deleted successfuly!")
	except:
		flash("Fail to delete the file!")
	return redirect(url_for('home'))

if __name__=='__main__':
	app.run(debug=True)