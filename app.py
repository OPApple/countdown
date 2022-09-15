from re import search
from xml.etree.ElementTree import tostring
from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///times.db'
db = SQLAlchemy(app)



def toJsDate(date):

    try:
        new_date = str(date).split("-")
        new_date_hms = new_date[2].split("T")

        year = int(new_date[0])
        month = int(new_date[1]) - 1
        day = int(new_date_hms[0])
        hour = int(new_date_hms[1].split(":")[0])
        minute = int(new_date_hms[1].split(":")[1])

        final_date = [year, month, day, hour, minute]
        

        return final_date
    except:
        return "something went wrong, don't be a fuckwit and submit empty froms"



class Countdowns(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    content = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return self.content

    # this allows getting an element (overrided method)
    def __getitem__(self, id): 
        return self.id
    
    def __str__ (self):
        return str(self.id)

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        
        try:
                
            date = request.form['date_input']
            desc = request.form['desc']
            name = request.form['name']
            new_countdown = Countdowns(content=date, desc=desc, name=name)
            try:
                db.session.add(new_countdown)
                db.session.commit()
                return redirect('/')
            except:
                return "Oops, fuck yuo"
        
        except:
            return redirect('/timer')
        
        


        
    else:
        # countdowns = Countdowns.query.order_by(Countdowns.date_created.desc()).first()
        # countdowns.content = toJsDate(countdowns.content)
        return render_template('index.html')
        
@app.route('/createnew')
def create_new():
    return render_template('createnew.html')

@app.route('/timer', methods=['POST', 'GET'])
def timer():
    
    if request.method == 'POST':
        try:
            search = request.form['search']
            countdowns = Countdowns.query.filter_by(name=search).first()
            countdowns.content = toJsDate(countdowns.content)
            return render_template('timer.html', countdowns=countdowns)
        except:
            
            return render_template('timer.html', countdowns="None")

    else:
        return render_template('timer.html', countdowns=False)

@app.route('/christmas')
def christmas():
    countdowns = Countdowns.query.filter_by(name='x-mas').first()
    countdowns.content = toJsDate(countdowns.content)
    return render_template('christmas.html', countdowns=countdowns)

@app.route('/summer')
def summer():
    countdowns = Countdowns.query.filter_by(name='summer').first()
    countdowns.content = toJsDate(countdowns.content)
    return render_template('christmas.html', countdowns=countdowns)

@app.route('/P5R')
def P5R():
    countdowns = Countdowns.query.filter_by(name='P5R').first()
    countdowns.content = toJsDate(countdowns.content)
    return render_template('christmas.html', countdowns=countdowns)

if __name__ == "__main__":
    app.run(debug=True)