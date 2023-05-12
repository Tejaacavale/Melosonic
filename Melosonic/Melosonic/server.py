from flask import Flask, request, jsonify, url_for, send_from_directory, redirect
from flask import render_template
import sqlite3
import hashlib
from flask_cors import CORS
import os
app = Flask(__name__, static_folder='static/')
CORS(app)


def string_to_key(string):
    """Converts a string into an integer hash key using Rabin-Karp rolling hash."""
    BASE = 31  # base for the hash function
    MOD = 10**9 + 9  # modulus for the hash function
    key = 0  # current hash key
    for i, c in enumerate(string):
        key = (key * BASE + ord(c)) % MOD
    return key


@app.route('/Melosonic/<path:filename>')
def serve_file(filename):
    root_dir = os.path.dirname(os.getcwd())
    print(root_dir)
    return send_from_directory(os.path.join(root_dir,'Melosonic'), filename)


# Create SQLite database and table if they don't exist
conn = sqlite3.connect('playlist.db')
conn.execute('CREATE TABLE IF NOT EXISTS songs (id INTEGER PRIMARY KEY, name TEXT, duration TEXT,albumname TEXT, artistname TEXT )')
conn.commit()
conn.close()
# Endpoint for adding a song to the playlist


@app.route('/add-to-playlist', methods=['POST'])
def add_to_playlist():
    print("OK")
    # Get song data from request body
    song = request.get_json()
    name = song['name']
    duration = song['duration']
    artal = song['artal']
    print(artal)
    L = artal.split('-')
    artist = L[0]
    album = L[1]
    id = string_to_key(name)
    # Check if song already exists in database
    conn = sqlite3.connect('playlist.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM songs WHERE id=?', (id,))
    result = cursor.fetchone()
    conn.close()
    if result:
        # Song already exists, return 409 Conflict HTTP status code and error message
        return jsonify({'message': 'Song already exists in playlist.'}), 409

        # Insert song into database
    conn = sqlite3.connect('playlist.db')
    conn.execute('INSERT INTO songs (id,name, duration,albumname,artistname) VALUES (?, ?, ?, ?, ?)',
                 (id, name, duration, album, artist))
    conn.commit()
    conn.close()

    # Return success message
    return jsonify({'message': 'Song added to playlist successfully.'}), 200


@app.route('/playlist')
def playlist():
    # connect to the database
    conn = sqlite3.connect('playlist.db')
    c = conn.cursor()

    # execute a SELECT statement to retrieve all the songs
    c.execute('SELECT * FROM songs')
    songs = c.fetchall()

    # close the database connection
    conn.close()

    # pass the songs to the template for display
    return render_template('playlist.html', songs=songs)


@app.route('/remove-song', methods=['POST'])
def remove_song():
    print("OK")
    # get the song ID from the request data
    song_id = request.json.get('id')

    # remove the song from the database
    conn = sqlite3.connect('playlist.db')
    c = conn.cursor()
    c.execute('DELETE FROM songs WHERE id=?', (song_id,))
    conn.commit()
    conn.close()

    # return a JSON response indicating success
    return jsonify(success=True)

@app.route('/')
def redirect_to_homepage():
    return redirect('/Melosonic/homepage.html')
if __name__ == '__main__':
    app.run(debug=True)
