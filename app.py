from flask import Flask,render_template,request,redirect
import urllib
client_id='3c09b102f81b4cc0bfbe1720d41278f1'
authorization_url='https://accounts.spotify.com/authorize?'
redirect_uri= "http://localhost:5000/callback/",
scope='playlist-read-private user-read-private user-read-email'

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
                "response_type":'token',
                "show_dialog":"true"
            }
        url=authorization_url+urllib.parse.urlencode(query_parameter,safe=":")
    
     return redirect (url)
    
   
    
   # return("hello world")

if __name__=="__main__":
    app.run(debug=True)