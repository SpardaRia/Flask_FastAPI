from flask import Flask, request, make_response, render_template, redirect, url_for

app=Flask(__name__)


@app.route('/')
def base():
    return render_template('main.html')


@app.route('/cookie/', methods=['POST'])
def welcome():
    username = request.form['name']
    usermail = request.form['mail']

    response = make_response(redirect('/hello/'))
    response.set_cookie('name', username)
    response.set_cookie('mail', usermail)
    return response


@app.route('/hello/')
def hello():
    
    username = request.cookies.get('name')
    if username:
        return render_template('hello.html')
    return redirect('/')


@app.route('/login/', methods=['GET', 'POST'])
def login():
    context = {
        'task': 'Задание'
    }
    if request.method == 'POST':
        username = request.form.get('name')
        usermail = request.form.get('mail')
        context = {'username': username,
                   'usermail': usermail}
    return render_template('login.html', **context)


@app.route('/logout/', methods=['GET', 'POST'])
def logout():
    response = make_response(redirect('/'))
    response.delete_cookie('name')
    response.delete_cookie('mail')
    return response


if __name__ == '__main__':
    app.run(debug=True)