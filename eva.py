from flask import Flask, render_template, request, Response
from flask import jsonify
from functools import wraps

app = Flask(__name__,static_url_path="/static") 

def check_auth(username, password):
    return username == 'felix' and password == '1001'

# Routing
@app.route('/message', methods=['POST'])
def reply():
    return jsonify( { 'resp': "hello, i am bot" } )

def authenticate():
    # 401 response
    return Response('Could not verify your access level for that URL; \n You have to login with proper credentials',
            401,{'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    # f -> function being decorated
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args,**kwargs)
    return decorated

@app.route("/") 
#@requires_auth
def secret_page(): 
    return render_template('index.html')

if (__name__ == "__main__"): 
    app.run(port = 5000) 
