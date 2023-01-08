from flask import Flask,render_template,request

app = Flask(__name__)
@app.route("/",methods=['POST','GET'])
def hello_world():
    if request.method == 'POST':
        #youtube()
        print("hellow world")

    return render_template('index.html')

def youtube():
    print("hello world!")
    
        
    
   # return("hello world")

if __name__=="__main__":
    app.run(debug=True)