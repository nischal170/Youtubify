from flask import Flask,render_template,redirect,request
import requests
import urllib,json,base64
client_id='3c09b102f81b4cc0bfbe1720d41278f1'
client_secret='68c4e2f213994766bb584ca077e7cefb'
authorization_url='https://accounts.spotify.com/authorize?'
redirect_uri= "http://localhost:5000/callback/",
scope='playlist-read-private user-read-private user-read-email user-library-read user-library-read'
token_url = 'https://accounts.spotify.com/api/token'

app = Flask(__name__)
@app.route("/",methods=['POST','GET'])
def hello_world():



    return render_template('index.html')

def youtube():
    print("hello world!")
@app.route("/connect_spotify",methods=['POST','GET']) 
def spotify():
     if request.method == 'POST':

        if request.form.get('submit_button')=='Connect to Spotify':
            query_parameter={
                "client_id":client_id,
                "redirect_uri":"http://localhost:5000/callback/",
                "scope":scope,
                "response_type":'code',
                "show_dialog":"true"
            }
        url=authorization_url+urllib.parse.urlencode(query_parameter,safe=":")
    
     return redirect (url)

@app.route("/callback/", methods=['GET'])
def callback():
    # Get the authorization code from the query string
    code=request.args.get('code') or None
     
    if code!=None:
        #base64 enc
        auth_header =  f'Basic {base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()}'
        headers = { 'Authorization': auth_header }
        data = { 'grant_type': 'authorization_code', 'code': code, 'redirect_uri': redirect_uri }
        #post request to token_url for access and refresh token
        response = requests.post(token_url, headers=headers, data=data)
        token_json = response.json()

        # Extract the access token and refresh token from the response
        access_token = token_json['access_token']
        
        refresh_token = token_json['refresh_token']

        # Use the access token to make a requests to the Spotify Web API
        headers = { 'Authorization': f'Bearer {access_token}' }
        response = requests.get('https://api.spotify.com/v1/me', headers=headers)
        user_json = response.json()

        return json.dumps(user_json)
            
        
    else:
        return '<h1>Access denied: reason=Cancelled By the User</h1>'

    


if __name__=="__main__":
    app.run(debug=True)