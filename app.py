from flask import Flask, request, jsonify, redirect, render_template
from yt_dlp import YoutubeDL

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')  # Render the HTML form (index.html) from the templates folder

@app.route('/get_song', methods=['GET'])
def get_song():
    song_name = request.args.get('song_name')
    
    if not song_name:
        return jsonify({"error": "Song name is required"}), 400

    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'noplaylist': True,
        'default_search': 'ytsearch1'
    }
    
    try:
        with YoutubeDL(ydl_opts) as ydl:
            result = ydl.extract_info(song_name, download=False)

            if 'entries' in result and len(result['entries']) > 0:
                audio_url = result['entries'][0]['url']
            else:
                audio_url = result.get('url')

            if not audio_url:
                return jsonify({"error": "No audio found"}), 404

        # Option 1: Return JSON response (for API use)
        # return jsonify({"audio_url": audio_url})

        # Option 2: Redirect directly to the audio URL for browser playback
        return redirect(audio_url)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
