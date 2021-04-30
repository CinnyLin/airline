from flask import Flask, render_template

# initialize flask app
app = Flask(__name__)

# define a simple route function
@app.route('/')
def hello():
    # return 'Hello World!'
    return render_template('hello.html')


@app.route('/greet/')
@app.route('/greet/<name>')
def greet(name=None):
    return render_template('greet.html', name=name)


# run the app
if __name__ == '__main__':
    app.run('127.0.0.1', 5000)
