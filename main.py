from flask_sqlalchemy import SQLAlchemy
from flask import Flask, app, render_template, sessions, request, url_for
from flask import flash
from sqlalchemy import ForeignKey
from werkzeug.utils import redirect, secure_filename
import os
import pymysql

pymysql.install_as_MySQLdb()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:200189ymy@127.0.0.1:3306/web_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '23'
db = SQLAlchemy(app)


class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    bz = db.Column(db.Text)
    path = db.Column(db.Text)


class Pii(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    sex = db.Column(db.Text)
    age = db.Column(db.Integer)
    abo = db.Column(db.Text)
    symptoms = db.relationship('Sx', back_populates='patient')


class Sx(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    symptom = db.Column(db.Text)
    p_id = db.Column(db.Integer, ForeignKey('pii.id'))
    patient = db.relationship('Pii', back_populates='symptoms')


db.create_all()


@app.route('/sjj', methods=['GET', 'POST'])
def sjj():
    if request.method == 'POST':
        f = request.files.get('wjsc')
        bzhu = request.form.get('beizhu')
        basepath = os.path.dirname(__file__)  # 当前文件所在路径
        upload_path = os.path.join(basepath, r'static\uploads', secure_filename(f.filename))
        f.save(upload_path)
        fl = File(name=secure_filename(f.filename), bz=bzhu)
        db.session.add(fl)
        db.session.commit()
        flash('Upload successfully!')
        return redirect(url_for('sjj'))
    file_list = File.query.all()
    return render_template('sjj.html', file_list=file_list)


@app.route('/rec', methods=['GET', 'POST'])
def recommend():
    if request.method == 'POST':
        hz_id = request.form.get('hz_id')
        nm = request.form.get('nm')
        xb = request.form.get('xb')
        nl = request.form.get('age')
        xx = request.form.get('abo')
        pat = Pii(id=hz_id, name=nm, sex=xb, age=nl, abo=xx)
        db.session.add(pat)
        db.session.commit()
        spt = request.form.get('pmh')
        spts = spt.split(';')
        spt_num = len(spts)
        for index in range(spt_num):
            zz = Sx(symptom=spts[index], p_id=hz_id)
            db.session.add(zz)
            db.session.commit()
        flash('Successfully!')
        return redirect(url_for('recommend'))
    return render_template('cftj.html')


@app.route('/delete/<int:file_id>', methods=['GET', 'POST'])
def delete(file_id):
    if request.method == 'POST':
        fd = File.query.get_or_404(file_id)
        db.session.delete(fd)
        db.session.commit()
        basepath = os.path.dirname(__file__)
        filepath = os.path.join(basepath, r'static\uploads', fd.name)
        os.remove(filepath)
        flash('Delete successfully！')
        return redirect(url_for('sjj'))


@app.route('/cftj')
def cftj():
    """
    """
    return render_template('cftj.html')


if __name__ == '__main__':
    app.run(debug=True)
