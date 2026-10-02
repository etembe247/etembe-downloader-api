from flask import Flask, request, jsonify
from flask_cors import CORS
import yt_dlp

app = Flask(__name__)
CORS(app) # Allows your etembe.qzz.io domain to securely talk to this backend

@app.route('/extract', methods=['POST'])
def extract_media():
    data = request.get_json()
    if not data or 'url' in not data:
        return jsonify({'status': 'error', 'text': 'Missing URL address parameters.'}), 400

    url = data['url']
    is_audio = data.get('isAudioOnly', False)

    # High-performance yt-dlp core configuration parameters
    ydl_opts = {
        'format': 'bestaudio/best' if is_audio else 'bestvideo+bestaudio/best',
        'quiet': True,
        'no_warnings': True,
        'noplaylist': True
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            # Extract direct, un-throttled stream asset URL downloads
            stream_url = info.get('url') or info.get('formats')[-1].get('url')
            return jsonify({'status': 'stream', 'url': stream_url})
    except Exception as e:
        return jsonify({'status': 'error', 'text': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
