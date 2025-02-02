from flask import Flask, redirect, url_for, request, render_template, make_response
from flask_debugtoolbar import DebugToolbarExtension
import ping as p
import predict as pr

# Flask constructor takes the name of 
# current module (__name__) as argument.
app = Flask(__name__)

import ping as p

# The route() function of the Flask class is a decorator, 
# which tells the application which URL should call 
# the associated function.
@app.route('/')
def intro():
    return render_template('login.html')

@app.route('/ping')
def pong():
    return p.Pong()

@app.route('/ping/<name>')
def pongwithname(name):
    return p.Pongwithname(name)

@app.route('/login',methods = ['POST', 'GET'])
def login(): #database is expensive so don't read too miuch into what this really does here.
   if request.method == 'POST':
      user = request.form['nm']
      return redirect(url_for('predict',name = user))
   else:
      return redirect(url_for('intro'))

@app.route('/predict/<name>', methods=['GET'])
def predict(name): 
    resp = make_response(render_template('predict.html', name = name))
    resp.set_cookie('username', name)
    return resp
    
@app.route('/predict', methods=['POST'])
def predict_api():
    # Extract input features from the request
    feature1 = request.form['feature1']

    # Make predictions using the loaded model
    prediction = pr.predict(feature1)

    # Output result
    output = "It's a positive review." if prediction == 1 else "It's a negative review."

    name = request.cookies.get('username')

    return render_template('predict.html', name = name, prediction=output)


# main driver function
if __name__ == '__main__':
    app.debug = True
    
    # https://flask-debugtoolbar.readthedocs.io/en/latest/index.html
    app.config['SECRET_KEY'] = 'key'
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
    toolbar = DebugToolbarExtension(app)
    app.run()