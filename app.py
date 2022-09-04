import random, copy
import sqlite3
from flask import Flask, flash, redirect, url_for, render_template, request, session, request

app = Flask(__name__)
app.secret_key = "r@nd0mSk_1"

mathematics_question = {
    'Berapa 1+1 =': ['2', '3', '4', '5'],
    'Berapa 1+2 =': ['3', '2', '4', '5'],
    'Berapa 1+3 =': ['4', '3', '2', '5'],
    'Berapa 1+4 =': ['5', '3', '4', '2'],
    'Berapa 1+5 =': ['6', '4', '5', '3']
}

it_question = {
    'Yang termasuk perangkat keras adalah': ['All answers are wrong', 'Software', 'Processor', 'Hardware'],
    'Program-program yang ada di komputer': ['Software', 'Hardware', 'Brainware', 'scanner'],
    'Media penyimpan data': ['Hardisk', 'Scanner', 'Printer', 'Plotter'],
    'Mana yang bukan media sosial': ['Book', 'Facebook', 'Instagram', 'Twitter'],
    'Perintah save dapat juga dijalankan dengan menekan tombol ... dikeyboard': ['Ctrl + S', 'Ctrl + P', 'Ctrl + V', 'Ctrl + C']
}

math_questions = copy.deepcopy(mathematics_question)
it_questions = copy.deepcopy(it_question)

def shuffle(q):
    selected_keys = []
    i = 0
    while i < len(q):
        current_selection = random.choice(list(q.keys()))
        if current_selection not in selected_keys:
            selected_keys.append(current_selection)
            i = i+1
    return selected_keys

@app.route("/")
def index():
    return render_template('LoginRegisterPage/login.html')

@app.route("/history")
def history():
    con = sqlite3.connect("database.db")
    con.row_factory = sqlite3.Row
    historys = con.execute('select * from history  where username = ?', (data['username'],)).fetchall()
    con.close()
    if len(historys) != 0:
        return render_template('QuizPage/history.html', historys=historys)
    else:
        flash("You have not done the quiz at all, please do the quiz first","oops!")
        return render_template('QuizPage/error_history.html')

@app.route("/mathematics_quiz")
def mathematics_quiz():
    questions_shuffled = shuffle(math_questions)
    for i in math_questions.keys():
        random.shuffle(math_questions[i])
    return render_template('QuizPage/mathematics_quiz.html', q = questions_shuffled, o = math_questions)

@app.route("/math_result", methods = ['POST'])
def math_result():
    correct = 0
    topic = 'mathematic'
    score = 0
    for i in math_questions.keys():
        answered = request.form[i]
        if mathematics_question[i][0] == answered:
            correct = correct + 1
            score = correct * 20
            flash("Your Score is: " + str(score),"Good Job!")
    con = sqlite3.connect("database.db")
    cur = con.cursor()
    cur.execute("insert into history(username,topic, score) values(?, ?, ?)", (data['username'], topic, score))
    con.commit()
    return render_template('QuizPage/mathematics_quiz.html')

@app.route("/it_quiz")
def it_quiz():
    question_shuffled = shuffle(it_questions)
    for i in it_questions.keys():
        random.shuffle(it_questions[i])
    return render_template('QuizPage/it_quiz.html', q = question_shuffled, o = it_questions)

@app.route("/it_result", methods = ['POST'])
def it_result():
    correct = 0
    topic = 'information technology'
    score = 0
    for i in it_questions.keys():
        answered = request.form[i]
        if it_question[i][0] == answered:
            correct = correct + 1
            score = correct * 20
            flash("Your Score is: " + str(score),"Good Job!")
    con = sqlite3.connect("database.db")
    cur = con.cursor()
    cur.execute("insert into history(username,topic, score) values(?, ?, ?)", (data['username'], topic, score))
    con.commit()
    return render_template('QuizPage/mathematics_quiz.html')

@app.route('/register', methods=["POST", "GET"])
def register():
    if request.method == 'POST':
        try:
            username = request.form['username']
            password = request.form['password']
            con = sqlite3.connect("database.db")
            cur = con.cursor()
            cur.execute("insert into users(username,password)values(?,?)", (username,password))
            con.commit()
            flash("Register Successfully","success")
        except:
            flash("Register failed","danger")
        finally:
            return redirect(url_for('index'))
            con.close()
    return render_template('LoginRegisterPage/register.html')

@app.route('/login', methods=["POST", "GET"])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        con = sqlite3.connect("database.db")
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("select * from users where username=? and password=?",(username, password))
        global data
        data = cur.fetchone()

        if data:
            session['username'] = data['username']
            return redirect('home')

        else:
            flash("Username and password unregistered, please register first!", "danger")
    return redirect(url_for('index'))

@app.route('/home', methods=['POST', "GET"])
def home():
    return render_template('QuizPage/home.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
