from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///thoughts.db'
db = SQLAlchemy(app)

class Thought(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Thought %r>' % self.content

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        thought_content = request.form['content']
        new_thought = Thought(content=thought_content)

        try:
            db.session.add(new_thought)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your thought'

    else:
        # check and delete any thoughts that are more than 24 hours old
        for thought in Thought.query.all():
            if datetime.now() - thought.timestamp > timedelta(hours=1.5):
                db.session.delete(thought)
                db.session.commit()

        thoughts = Thought.query.order_by(Thought.timestamp).all()
        return render_template('index.html', thoughts=thoughts)


if __name__ == "__main__":
     with app.app_context():
         db.create_all()
         app.run(debug=True)
    
     