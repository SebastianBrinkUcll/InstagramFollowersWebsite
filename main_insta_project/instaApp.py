from flask import Flask, render_template, request, redirect, url_for
import os
import json

app = Flask(__name__)

# Folder to store uploaded files
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the uploads folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def load_instagram_data(file_path):
    """Load JSON data from a file."""
    if not os.path.exists(file_path):
        print(f"ERROR: File not found: {file_path}")
        return set()

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

            usernames = set()
            if isinstance(data, dict):
                if 'relationships_followers' in data:
                    entries = data['relationships_followers']
                elif 'relationships_following' in data:
                    entries = data['relationships_following']
                else:
                    print(f"No known keys found in {file_path}")
                    return set()
            elif isinstance(data, list):
                entries = data
            else:
                print(f"Unexpected data type in {file_path}")
                return set()

            for entry in entries:
                if isinstance(entry, dict):
                    if 'string_list_data' in entry and entry['string_list_data']:
                        username = entry['string_list_data'][0].get('value')
                        if username:
                            usernames.add(username)
                    elif 'value' in entry:
                        usernames.add(entry['value'])
                elif isinstance(entry, str):
                    usernames.add(entry)

            return usernames

    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return set()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_files():
    if 'followers_file' not in request.files or 'following_file' not in request.files:
        return "No file part", 400

    followers_file = request.files['followers_file']
    following_file = request.files['following_file']

    if followers_file.filename == '' or following_file.filename == '':
        return "No selected file", 400

    followers_path = os.path.join(app.config['UPLOAD_FOLDER'], 'followers.json')
    following_path = os.path.join(app.config['UPLOAD_FOLDER'], 'following.json')

    followers_file.save(followers_path)
    following_file.save(following_path)

    # Load the data and find unfollowers
    followers = load_instagram_data(followers_path)
    following = load_instagram_data(following_path)
    unfollowers = following - followers

    # Return a result
    return render_template('unfollowers.html', unfollowers=sorted(unfollowers))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
