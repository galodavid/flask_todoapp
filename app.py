from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        task_exercise = request.form['content']
        new_exercise = Todo(content=task_exercise)

        try:
            db.session.add(new_exercise)
            db.session.commit()
            return redirect('/')
        except:
            return 'Try again later'
    else:
        exercises = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', exercises=exercises)

@app.route('/delete/<int:id>')
def delete(id):
    exercise_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(exercise_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return "Couldn't delete that exercise"

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    exercise = Todo.query.get_or_404(id)

    if request.method == 'POST':
        exercise.content = request.form['content'] 

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'Cannot update task'
    else:
        return render_template('update.html', exercise=exercise)
    

if __name__ == "__main__":
    app.run(debug=True)