from flask import Flask , render_template,request,url_for,session,redirect
import random

app = Flask(__name__)
app.secret_key = 'secret_key'


@app.route('/', methods = ['GET', 'POST'])
def index():
   if request.method=="POST":
       session['player_name'] = request.form['player_name']
       session['attempt_left'] = 10
       session['number'] = random.randint(1,100)
       return redirect(url_for('game'))

   return render_template('player.html')
@app.route('/game', methods=['POST','GET'])
def game():
    if 'number' not in session or 'attempt_left' not in session:
        return redirect(url_for('index'))

    if request.method=='POST':
        guess = int(request.form['guess'])
        attempt_left = session['attempt_left']

        if guess == session['number']:
           session.pop('number')
           session.pop('attempt_left')
           return redirect(url_for('result', prompt = 'CONGRATULATIONS', message = 'You guessed the correct number.'))
        elif guess > session['number']:
            message = "TO HIGH! TRY AGAIN"
        else:
            message = "TO LOW! TRY AGAIN"

        attempt_left -=1
        session['attempt_left'] = attempt_left
        if attempt_left== 0:
            session.pop('number')
            session.pop('attempt_left')
            return redirect(url_for('result', prompt ='Nice try', message = "Game Over"))
        else:
            return render_template('game.html', message = message, attempt_left= attempt_left)
    return render_template("game.html", attempt_left = session['attempt_left'])

@app.route('/result')
def result():
    if 'player_name' in session and 'number' not in session and 'attempt_left' not in session:
        message = request.args.get('message')
        return render_template('result.html', player_name =session['player_name'], message = message)
    else:
        return redirect(url_for('index'))

if __name__ == '__main__' :
    app.run(debug=True)