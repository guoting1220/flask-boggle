from flask import Flask, request, render_template, redirect, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from boggle import Boggle

app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"
debug = DebugToolbarExtension(app)
boggle_game = Boggle()

@app.route('/')
def show_board():
    """show the board and the form for user to submit a guess"""

# put the code below here instead of global, solve the problem that the board is not changed when refreshing the page
    board = boggle_game.make_board()
    session['board'] = board
    highest = session.get("highest", 0)
    playtimes = session.get("playtimes", 0)
    return render_template("index.html", board=board, highest=highest, playtimes=playtimes)


@app.route('/check-word')
def check_word_valid():
    """Check if word is in dictionary."""

    # On the server, take the form value and check if it is a valid word in the dictionary
    board = session["board"]
    word = request.args.get("word")
    result = boggle_game.check_valid_word(board, word)
    
    # Since you made an AJAX request to your server, you will need to respond with JSON using the jsonify function from Flask.
    #  {“result”: “ok”}, {“result”: “not-on-board”}, or {“result”: “not-a-word”},
    return jsonify({'result': result})


@app.route('/post-score', methods=["POST"])
def update_score_times():
    """update the the highest score and the times the player have played the game"""

    # update the highest score in session

    # Since you will be sending this data as JSON when you make an axios request, you will see this data come in your Flask app inside of request.json not request.form.
    score = request.json["score"]
    highest_score = session.get("highest", 0)
    session["highest"] = max(score, highest_score)

    # update the times of play in session
    times_of_plays = session.get("playtimes", 0)     
    session["playtimes"] = times_of_plays + 1

    return jsonify({"highest_score": session["highest"], "times_of_plays": session["playtimes"]})

