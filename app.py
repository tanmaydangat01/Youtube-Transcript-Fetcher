<<<<<<< HEAD
from flask import Flask, render_template, request, redirect, url_for, session, make_response
from youtube_transcript_api import YouTubeTranscriptApi
from googleapiclient.discovery import build
import re

app = Flask(__name__)
app.secret_key = '9f4351efdfae8db71c15a8437c73889f7dcf229d92629f15e81c4d8b6b25f776'

API_KEY = 'AIzaSyAmS6FwEoi0KU2FvOxJIWhcTOVX9i_7Fx4'

users = {}

def get_video_id(url):
    """Extract video ID from YouTube URL."""
    match = re.search(r'(?:v=|\/)([0-9A-Za-z_-]{11}).*', url)
    return match.group(1) if match else None

def get_video_metadata(video_id):
    """Fetch video title and channel name using YouTube Data API."""
    try:
        youtube = build('youtube', 'v3', developerKey=API_KEY)
        request = youtube.videos().list(part='snippet', id=video_id)
        response = request.execute()
        if response['items']:
            snippet = response['items'][0]['snippet']
            return {
                'title': snippet['title'],
                'channel': snippet['channelTitle']
            }
    except Exception:
        return {'title': 'Unknown Title', 'channel': 'Unknown Channel'}

def format_timestamp(seconds):
    """Convert seconds to HH:MM:SS format."""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    if hours > 0:
        return f"{hours}:{minutes:02}:{secs:02}"
    return f"{minutes}:{secs:02}"

def time_to_seconds(time_str):
    """Convert time string (HH:MM:SS or MM:SS) to total seconds."""
    parts = [int(x) for x in time_str.split(':')]
    return sum(part * 60 ** i for i, part in enumerate(reversed(parts)))

def filter_transcript(transcript, start_time, end_time):
    """Filter transcript based on start and end times."""
    start_seconds = time_to_seconds(start_time) if start_time else 0
    end_seconds = time_to_seconds(end_time) if end_time else float('inf')
    return [entry for entry in transcript if start_seconds <= entry['start'] <= end_seconds]

# Routes
@app.route('/')
def home():
    """Redirect to authentication page first."""
    session.clear() 
    return redirect(url_for('auth'))


@app.route('/auth', methods=['GET', 'POST'])
def auth():
    """Render the authentication page."""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if request.form.get('action') == 'signup':
            if email in users:
                return render_template('auth.html', error="User already exists!")
            users[email] = password
            session['user'] = email
            return redirect(url_for('index'))

        elif request.form.get('action') == 'login':
            if email in users and users[email] == password:
                session['user'] = email
                return redirect(url_for('index'))
            return render_template('auth.html', error="Invalid credentials!")

    return render_template('auth.html')

@app.route('/guest', methods=['GET'])
def guest():
    """Allow users to continue without logging in."""
    session['user'] = 'guest'
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    """Log out the current user and clear the session."""
    session.clear()
    return redirect(url_for('auth'))


@app.route('/index', methods=['GET', 'POST'])
def index():
    """Render the main page and fetch YouTube transcript."""
    if 'user' not in session:
        return redirect(url_for('auth'))

    if request.method == 'POST':
        url = request.form.get('url')
        start_time = request.form.get('start_time')
        end_time = request.form.get('end_time')
        video_id = get_video_id(url)

        if not video_id:
            return render_template('index.html', error="Invalid YouTube URL.")

        # Redirect to the transcript page with video_id, start_time, and end_time
        return redirect(url_for('transcript', video_id=video_id, start_time=start_time, end_time=end_time))

    return render_template('index.html')

@app.route('/transcript', methods=['GET'])
def transcript():
    """Render the transcript page."""
    video_id = request.args.get('video_id')
    start_time = request.args.get('start_time')
    end_time = request.args.get('end_time')

    if not video_id:
        return redirect(url_for('index'))

    try:
        metadata = get_video_metadata(video_id)
        transcript_data = YouTubeTranscriptApi.get_transcript(video_id)
        filtered_transcript = filter_transcript(transcript_data, start_time, end_time)
        transcript = [{'start': format_timestamp(entry['start']), 'text': entry['text']} for entry in filtered_transcript]
        video_url = f"https://www.youtube.com/embed/{video_id}"
        return render_template(
            'transcript.html',
            video_metadata=metadata,
            transcript=transcript,
            video_url=video_url
        )
    except Exception as e:
        return render_template('index.html', error=f"Error fetching transcript: {str(e)}")

@app.route('/download', methods=['POST'])
def download():
    """Download the transcript as a text file."""
    transcript = request.form.get('transcript', 'No transcript available.')
    response = make_response(transcript)
    response.headers["Content-Disposition"] = "attachment; filename=transcript.txt"
    response.headers["Content-Type"] = "text/plain"
    return response


if __name__ == '__main__':
    app.run(debug=True)
=======
from flask import Flask, render_template, request, redirect, url_for, session, make_response
from youtube_transcript_api import YouTubeTranscriptApi
from googleapiclient.discovery import build
import re

app = Flask(__name__)
app.secret_key = '9f4351efdfae8db71c15a8437c73889f7dcf229d92629f15e81c4d8b6b25f776'

API_KEY = 'AIzaSyAmS6FwEoi0KU2FvOxJIWhcTOVX9i_7Fx4'

users = {}

def get_video_id(url):
    """Extract video ID from YouTube URL."""
    match = re.search(r'(?:v=|\/)([0-9A-Za-z_-]{11}).*', url)
    return match.group(1) if match else None

def get_video_metadata(video_id):
    """Fetch video title and channel name using YouTube Data API."""
    try:
        youtube = build('youtube', 'v3', developerKey=API_KEY)
        request = youtube.videos().list(part='snippet', id=video_id)
        response = request.execute()
        if response['items']:
            snippet = response['items'][0]['snippet']
            return {
                'title': snippet['title'],
                'channel': snippet['channelTitle']
            }
    except Exception:
        return {'title': 'Unknown Title', 'channel': 'Unknown Channel'}

def format_timestamp(seconds):
    """Convert seconds to HH:MM:SS format."""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    if hours > 0:
        return f"{hours}:{minutes:02}:{secs:02}"
    return f"{minutes}:{secs:02}"

def time_to_seconds(time_str):
    """Convert time string (HH:MM:SS or MM:SS) to total seconds."""
    parts = [int(x) for x in time_str.split(':')]
    return sum(part * 60 ** i for i, part in enumerate(reversed(parts)))

def filter_transcript(transcript, start_time, end_time):
    """Filter transcript based on start and end times."""
    start_seconds = time_to_seconds(start_time) if start_time else 0
    end_seconds = time_to_seconds(end_time) if end_time else float('inf')
    return [entry for entry in transcript if start_seconds <= entry['start'] <= end_seconds]

# Routes
@app.route('/')
def home():
    """Redirect to authentication page first."""
    session.clear() 
    return redirect(url_for('auth'))


@app.route('/auth', methods=['GET', 'POST'])
def auth():
    """Render the authentication page."""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if request.form.get('action') == 'signup':
            if email in users:
                return render_template('auth.html', error="User already exists!")
            users[email] = password
            session['user'] = email
            return redirect(url_for('index'))

        elif request.form.get('action') == 'login':
            if email in users and users[email] == password:
                session['user'] = email
                return redirect(url_for('index'))
            return render_template('auth.html', error="Invalid credentials!")

    return render_template('auth.html')

@app.route('/guest', methods=['GET'])
def guest():
    """Allow users to continue without logging in."""
    session['user'] = 'guest'
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    """Log out the current user and clear the session."""
    session.clear()
    return redirect(url_for('auth'))


@app.route('/index', methods=['GET', 'POST'])
def index():
    """Render the main page and fetch YouTube transcript."""
    if 'user' not in session:
        return redirect(url_for('auth'))

    if request.method == 'POST':
        url = request.form.get('url')
        start_time = request.form.get('start_time')
        end_time = request.form.get('end_time')
        video_id = get_video_id(url)

        if not video_id:
            return render_template('index.html', error="Invalid YouTube URL.")

        # Redirect to the transcript page with video_id, start_time, and end_time
        return redirect(url_for('transcript', video_id=video_id, start_time=start_time, end_time=end_time))

    return render_template('index.html')

@app.route('/transcript', methods=['GET'])
def transcript():
    """Render the transcript page."""
    video_id = request.args.get('video_id')
    start_time = request.args.get('start_time')
    end_time = request.args.get('end_time')

    if not video_id:
        return redirect(url_for('index'))

    try:
        metadata = get_video_metadata(video_id)
        transcript_data = YouTubeTranscriptApi.get_transcript(video_id)
        filtered_transcript = filter_transcript(transcript_data, start_time, end_time)
        transcript = [{'start': format_timestamp(entry['start']), 'text': entry['text']} for entry in filtered_transcript]
        video_url = f"https://www.youtube.com/embed/{video_id}"
        return render_template(
            'transcript.html',
            video_metadata=metadata,
            transcript=transcript,
            video_url=video_url
        )
    except Exception as e:
        return render_template('index.html', error=f"Error fetching transcript: {str(e)}")

@app.route('/download', methods=['POST'])
def download():
    """Download the transcript as a text file."""
    transcript = request.form.get('transcript', 'No transcript available.')
    response = make_response(transcript)
    response.headers["Content-Disposition"] = "attachment; filename=transcript.txt"
    response.headers["Content-Type"] = "text/plain"
    return response


if __name__ == '__main__':
    app.run(debug=True)
>>>>>>> c71ab375b855096a4fc11dec14d4bf4ab9aca485
