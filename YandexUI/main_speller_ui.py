# all the imports
#from __future__ import with_statement
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
from contextlib import closing
import soap_request

# configuration
DATABASE = '/tmp/flaskr.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'


# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)
langs = None


@app.route('/')
def show_entries():
    langs = soap_request.get_lang()
    return render_template('layout.html', langs=langs)


@app.route('/translate', methods=['GET', 'POST'])
def translate():
    langs = soap_request.get_lang()
    error = None
    if request.method == 'POST':
        if request.form['translate'] != '':
            response = soap_request.main_ui(request.form['translate'],
                                            request.form['language'])
            if response is not None:
                return render_template('layout.html', langs=langs, response=response)
            else:
                error = 'Введен текст с ошибками!'
        else:
            error = 'Введите текст для перевода!'
    return render_template('layout.html', error=error, langs=langs)


if __name__ == '__main__':
    app.run()
