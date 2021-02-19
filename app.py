from flask import Flask, request, render_template, redirect
from flask_debugtoolbar import DebugToolbarExtension

from surveys import satisfaction_survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "super-secret-key"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

responses = []


@app.route("/")
def home_page():
    """Show survey title and instructions."""

    return render_template("home.html",title=satisfaction_survey.title,
     instructions=satisfaction_survey.instructions,
     questions=satisfaction_survey.questions)

@app.route("/questions/<int:question_id>")
def get_questions(question_id):

    question_count = len(satisfaction_survey.questions)
    question = satisfaction_survey.questions[question_id].question
    # question_idx = satisfaction_survey.questions.question)
    choices = satisfaction_survey.questions[question_id].choices
    
    return render_template("questions.html",title=satisfaction_survey.title,
     instructions=satisfaction_survey.instructions,
     question=question,choices=choices, count=question_count)

@app.route("/answer", methods=["POST"])
def answers():
    option = request.form['options']
    return redirect('/questions')