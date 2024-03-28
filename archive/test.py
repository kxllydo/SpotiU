import http.server
import socketserver
import webbrowser
import requests
import json
import base64
import os
import hashlib

client_id = 'bbf6ac9a6686421cab10717891f179cf'  # your clientId
client_secret = 'e7ee05789cbd497cb1f571647c411453'  # Your secret
redirect_uri = 'http://127.0.0.1:5500/home.html'  # Your redirect uri

state_key = 'spotify_auth_state'


def generate_random_string(length):
    return hashlib.sha256(os.urandom(length)).hexdigest()[:length]


class SpotifyAuthHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith('/login'):
            state = generate_random_string(16)
            self.send_response(301)
            self.send_header('Location', 'https://accounts.spotify.com/authorize?' +
                             'response_type=code' +
                             '&client_id=' + client_id +
                             '&scope=user-read-private user-read-email' +
                             '&redirect_uri=' + redirect_uri +
                             '&state=' + state)
            self.send_cookie(state_key, state)
            self.end_headers()
        elif self.path.startswith('/callback'):
            code = self.get_param('code')
            state = self.get_param('state')
            stored_state = self.get_cookie(state_key)

            if state is None or state != stored_state:
                self.redirect('/#' + json.dumps({'error': 'state_mismatch'}))
                return

            auth_options = {
                'url': 'https://accounts.spotify.com/api/token',
                'data': {
                    'code': code,
                    'redirect_uri': redirect_uri,
                    'grant_type': 'authorization_code'
                },
                'headers': {
                    'content-type': 'application/x-www-form-urlencoded',
                    'Authorization': 'Basic ' + base64.b64encode((client_id + ':' + client_secret).encode()).decode()
                }
            }

            token_response = requests.post(auth_options['url'], data=auth_options['data'], headers=auth_options['headers'])
            token_data = token_response.json()

            if 'access_token' in token_data:
                access_token = token_data['access_token']
                refresh_token = token_data['refresh_token']

                user_info_response = requests.get('https://api.spotify.com/v1/me', headers={'Authorization': 'Bearer ' + access_token})
                user_info = user_info_response.json()

                print(user_info)  # Output user information

                self.redirect('/#' + json.dumps({
                    'access_token': access_token,
                    'refresh_token': refresh_token
                }))
            else:
                self.redirect('/#' + json.dumps({'error': 'invalid_token'}))
        elif self.path.startswith('/refresh_token'):
            refresh_token = self.get_param('refresh_token')
            auth_options = {
                'url': 'https://accounts.spotify.com/api/token',
                'headers': {
                    'content-type': 'application/x-www-form-urlencoded',
                    'Authorization': 'Basic ' + base64.b64encode((client_id + ':' + client_secret).encode()).decode()
                },
                'data': {
                    'grant_type': 'refresh_token',
                    'refresh_token': refresh_token
                }
            }

            token_response = requests.post(auth_options['url'], data=auth_options['data'], headers=auth_options['headers'])
            token_data = token_response.json()

            if 'access_token' in token_data:
                access_token = token_data['access_token']
                refresh_token = token_data['refresh_token']
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'access_token': access_token, 'refresh_token': refresh_token}).encode())
            else:
                self.send_response(404)
                self.end_headers()
        else:
            super().do_GET()

    def send_cookie(self, key, value):
        self.send_header('Set-Cookie', f'{key}={value}; Secure; HttpOnly; SameSite=Strict')

    def get_cookie(self, key):
        cookie_header = self.headers.get('Cookie')
        if cookie_header:
            cookies = cookie_header.split('; ')
            for cookie in cookies:
                name, value = cookie.split('=')
                if name == key:
                    return value
        return None

    def get_param(self, param_name):
        query_params = self.path.split('?')
        if len(query_params) > 1:
            params = query_params[1].split('&')
            for param in params:
                name, value = param.split('=')
                if name == param_name:
                    return value
        return None

    def redirect(self, location):
        self.send_response(301)
        self.send_header('Location', location)
        self.end_headers()


def run_server(port=5500):
    server = socketserver.TCPServer(('localhost', port), SpotifyAuthHandler)
    webbrowser.open('http://127.0.0.1:5500/home.html')
    server.serve_forever()


if __name__ == "__main__":
    run_server()
