from flask import (Flask, render_template, request, redirect, session, url_for, send_from_directory)
import sys
sys.path.insert(1, './')
import wrapper_maps as Maps
import wrapper_database as Database

app = Flask(__name__)
app.secret_key = 'Secreto'

database = Database.wrapper_database()

@app.route('/', methods = ['POST', 'GET'])
def house():
    return redirect('/login')

@app.route('/login', methods = ['POST', 'GET'])
def login():
    if(request.method == 'POST'):
        email = request.form.get('email')
        password = request.form.get('pass')
           
        if database.login_user(email,password):
            
            session['user'] = email
            #return redirect('/dashboard')
            return redirect('http://0.0.0.0:8080')

        return "<h1>Credenciales Incorrectas</h1>"    

    return render_template("login.html")

#Para Recursos estaticos de la página web
@app.route("/<path:path>")
def static_dir(path):
    return send_from_directory("static", path)

@app.route('/dashboard')
def dashboard():
    if('user' in session and session['user'] == user['username']):
        return '<h1>Bienvenido al dashboard</h1>'
    

    return '<h1>No estas loggueado.</h1>'  

@app.route('/logout')
def logout():
    session.pop('user')         
    return redirect('/login')

if __name__ == '__main__':
    maps = Maps.wrapper_maps()
    app.run(debug=True, host='0.0.0.0')
