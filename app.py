from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///times.db'
db = SQLAlchemy(app)

class Countdowns(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return self.content

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        countdown = request.form['date_input']
        new_countdown = Countdowns(content=countdown)
        

        try:
            db.session.add(new_countdown)
            db.session.commit()
            return redirect('/')
        except:
            return "Oops, fuck yuo"
        
    else:
        countdowns = Countdowns.query.order_by(Countdowns.date_created).first()
        
        app.logger.info(countdowns)
        return render_template('index.html', countdowns=countdowns)
        

    

if __name__ == "__main__":
    app.run(debug=True)