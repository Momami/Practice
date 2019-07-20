
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
import rate

# configuration
DATABASE = '/tmp/flaskr.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'


# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)


@app.route('/')
def show_main_form():
    return render_template('mainform.html')


@app.route('/translate', methods=['GET', 'POST'])
def check():
    error = None
    if request.method == 'POST':
        if request.form['valutes'] != '':
            if request.form['date'] != '':
                response = rate.main_ui(request.form['valutes'].split(),
                                        request.form['date'])
                if response is not None:
                    return render_template('mainform.html', response=response)
                else:
                    error = 'Что-то пошло не так...'
            else:
                error = 'Введите дату!'

        else:
            error = 'Введите хотя бы одну валюту!'
    return render_template('mainform.html', error=error)


if __name__ == '__main__':
    app.run()