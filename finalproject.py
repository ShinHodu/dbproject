from flask import Flask, request  
app = Flask(__name__) 
@app.route('/') 
def finalproject(): 
    return 

@app.route('/mainpage')
def hellohtml():
    render_template("hello.html")

@app.route('/customer', methods==['GET','POST'])
def method():
    if request.method == 'GET':
        return "GET으로 전달" 
    else: 
        return "POST로 전달"


if __name__ == '__main__': 
app.run(debug=True)
