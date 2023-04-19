from flask import Flask, request, render_template
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

from googleapiclient.errors import HttpError
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google.oauth2.service_account import Credentials
import os
import json
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        video_id = request.form['video_id']
        try:
            transcript = get_transcript(video_id)
            return render_template('transcript.html', transcript=transcript, video_id=video_id)
        except HttpError as error:
            return f'An error occurred: {error}'
    else:
        return render_template('index.html')

def get_transcript(video_id):
    api_service_name = 'youtube'
    api_version = 'v3'
    client_secrets_file = 'client_secrets.json'
    credentials_file = 'credentials.json'
    scopes = ['https://www.googleapis.com/auth/youtube.force-ssl']

    if os.path.exists(credentials_file):
        with open(credentials_file, 'r') as f:
            creds_data = json.load(f)
        creds = Credentials.from_authorized_user_info(creds_data)
    else:
        flow = InstalledAppFlow.from_client_secrets_file(client_secrets_file, scopes)
        creds = flow.run_local_server(port=0)
        with open(credentials_file, 'w') as f:
            json.dump(creds.to_json(), f)

    youtube = build(api_service_name, api_version, credentials=creds)
    response = youtube.captions().list(
        part='id',
        videoId=video_id
    ).execute()

    caption_id = response['items'][0]['id']
    caption_response = youtube.captions().download(
        id=caption_id,
        tfmt='vtt'
    ).execute()

    transcript = caption_response.decode('utf-8')
    return transcript

