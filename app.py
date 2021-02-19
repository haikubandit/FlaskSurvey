from flask import Flask, request, render_template, redirect, flash
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
    print(question_id)
    current_question = len(responses)
    if question_id != len(responses):
        flash("That was an invalid question!")
        return redirect(f"/questions/{current_question}")
    elif current_question == len(satisfaction_survey.questions):
        return redirect('/complete')
    
    question = satisfaction_survey.questions[question_id].question
    choices = satisfaction_survey.questions[question_id].choices

    return render_template("questions.html",title=satisfaction_survey.title,
     instructions=satisfaction_survey.instructions,
     question=question,choices=choices)

@app.route("/answer", methods=["POST"])
def answers():
    choice = request.form['choice']
    responses.append(choice)
    next = len(responses)

    if next < len(satisfaction_survey.questions):
        return redirect(f"/questions/{next}")
    else:
        return render_template("complete.html",title=satisfaction_survey.title)

@app.route("/complete")
def complete():
    
    return render_template("complete.html",title=satisfaction_survey.title)