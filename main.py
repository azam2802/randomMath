from flask import Flask, render_template, jsonify, request, redirect, url_for, session
import random

app = Flask(__name__, static_url_path='/static')
app.config['SECRET_KEY'] = 'azam_key'

users = {}

user_stats = {}

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username not in users:
            # Register new user
            users[username] = password
            user_stats[username] = {
                'correct_answers': 0,
                'total_questions': 1,  
                'attempts': 0,
                'incorrect_answers': 0
            }
            session['username'] = username
            return redirect(url_for('index'))
        elif users[username] == password:
            session['username'] = username
            return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/')
def index():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    username = session['username']
    if username not in users:
        users[username] = 'default'  
    if username not in user_stats:
        user_stats[username] = {
            'correct_answers': 0,
            'total_questions': 1,  
            'attempts': 0,
            'incorrect_answers': 0
        }
    
    return render_template('index.html', user_stats=user_stats[session['username']], username=session['username'])

@app.route('/get_problem')
def get_problem():
    if 'username' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    problem, answer = generate_problem()
    return jsonify({'problem': problem, 'answer': answer})

@app.route('/update_stats', methods=['POST'])
def update_stats():
    if 'username' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    username = session['username']
    data = request.json
    
    user_stats[username].update({
        'correct_answers': data.get('correct'),
        'total_questions': data.get('total'),
        'attempts': data.get('attempts'),
        'incorrect_answers': data.get('incorrect')
    })
    
    return jsonify({'status': 'success'})

@app.route('/get_all_stats')
def get_all_stats():
    if 'username' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    all_stats = []
    for username, stats in user_stats.items():
        all_stats.append({
            'username': username,
            'correct': stats['correct_answers'],
            'incorrect': stats['incorrect_answers'],
            'total': stats['total_questions'],
            'attempts': stats['attempts']
        })
    
    return jsonify(all_stats)

def generate_problem():
    operators = ['+', '-', '*']
    num1 = random.randint(1, 20)
    num2 = random.randint(1, 20)
    operator = random.choice(operators)
    
    if operator == '+':
        answer = num1 + num2
    elif operator == '-':
        answer = num1 - num2
    else:
        answer = num1 * num2
    
    problem = f"{num1} {operator} {num2}"
    return problem, answer

if __name__ == '__main__':
    app.run(debug=False)
