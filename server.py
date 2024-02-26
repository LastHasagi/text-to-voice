from flask import Flask, request, send_file, render_template, make_response
from gtts import gTTS


app = Flask(__name__)

# Home route
@app.route('/')
def home():
    return render_template('index.html')

# Convert text to speech route
@app.route('/convert', methods=['GET', 'POST'])
def convert_text_to_speech():
    if request.method == 'POST':
        # Get the text from the form
        text = request.form.get('text')

        # Create the text-to-speech object
        tts = gTTS(text=text, lang='pt-br', slow=False)

        # Save the audio file
        audio_filename = "speech.mp3"
        tts.save(audio_filename)

        # Return the audio file as a response
        response = make_response(send_file(audio_filename, mimetype='audio/mpeg'))
        response.set_cookie(key='audio', value=audio_filename)
        return response
    elif request.method == 'GET':
        audio_filename = request.cookies.get('audio')
        if audio_filename:
            return send_file(audio_filename, mimetype='audio/mpeg')
        else:
            return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, port=5001)