from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension

from surveys import surveys

app = Flask(__name__)
app.config['SECRET_KEY'] = "super-secret-key"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)


@app.route("/")
def home_page():
    """Show survey title and instructions."""
    return render_template("home.html",surveys=surveys)

@app.route("/survey")
def chosen_survey():
    survey = request.args["surveys"]
    session["survey"] = survey
    chosen_survey = surveys[survey]
    return render_template('survey.html', survey=chosen_survey)

@app.route("/start-survey", methods=["POST"])
def start_survey():
    """Create response session and redirect to first session."""
    session["responses"] = []
    
    return redirect('/questions/0')

@app.route("/questions/<int:question_id>")
def get_questions(question_id):
    """Show next question in survey."""
    current_survey = surveys[session["survey"]]
    allow_text = current_survey.questions[question_id].allow_text

    current_question = len(session["responses"])
    if question_id != len(session["responses"]):
        flash("That was an invalid question!")
        return redirect(f"/questions/{current_question}")
    elif current_question == len(current_survey.questions):
        return redirect('/complete')

    question = current_survey.questions[question_id].question
    choices = current_survey.questions[question_id].choices

    return render_template("questions.html",title=current_survey.title,
     instructions=current_survey.instructions,
     question=question,choices=choices, allow_text=allow_text)

@app.route("/answer", methods=["POST"])
def answers():
    current_survey = surveys[session["survey"]]

    question = request.form['question']
    choice = request.form['choice']
    
    comment = request.form.get('comment', False)

    responses = session["responses"]
    responses.append({"question": question, "choice": choice, "comment": comment})
    session["responses"] = responses
    next = len(session["responses"])
    if next < len(current_survey.questions):
        return redirect(f"/questions/{next}")
    else:
        return render_template("complete.html",title=current_survey.title,
         responses=responses)

@app.route("/complete")
def complete():
    current_survey = surveys[session["survey"]]
    return render_template("complete.html",title=current_survey.title)