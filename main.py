from flask import Flask, app, render_template, sessions
from flask.helpers import flash
from werkzeug.utils import redirect

app = Flask(__name__)

app.secret_key = '123'
my_list = [
    {
        "name": "test.xls",
        "beizhu": "none"
    },
    {
        "name": "test2.xls",
        "beizhu": "none"
    }
]


@app.route('/sjj')
def sjj():
    """
    """
    return render_template('sjj.html', my_list=my_list)


@app.route('/cftj')
def cftj():
    """
    """
    return render_template('cftj.html')


if __name__ == '__main__':
    app.run(debug=True)
