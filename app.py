from flask import Flask, request, render_template, jsonify
import os

app = Flask(__name__)
DATA_FILE = 'user_data.txt'

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/form', methods=['GET', 'POST'])
def form_page():
    if request.method == 'POST':
        name = request.form.get('name')
        age = request.form.get('age')
        grade = request.form.get('grade')

        # Validate input
        if not name or not age or not grade or not age.isdigit() or int(age) < 0 or not grade.replace('.', '', 1).isdigit():
            return "Invalid input. Please fill out all fields correctly.", 400

        with open(DATA_FILE, 'a') as f:
            f.write(f"{name},{age},{grade}\n")

        return render_template('success.html', name=name)

    return render_template('form.html')

@app.route('/display')
def display_page():
    if not os.path.exists(DATA_FILE):
        return "No data found", 404

    users = []
    highest_grade = float('-inf')  # Initialize to the lowest possible value
    highest_student = None

    with open(DATA_FILE, 'r') as f:
        for line in f:
            name, age, grade = line.strip().split(',')
            users.append({'name': name, 'age': age, 'grade': float(grade)})

            # Check if this grade is the highest
            if float(grade) > highest_grade:
                highest_grade = float(grade)
                highest_student = name

    return render_template('display.html', users=users, highest_student=highest_student, highest_grade=highest_grade)

@app.route('/api/users', methods=['GET'])
def api_users():
    if not os.path.exists(DATA_FILE):
        return jsonify([])

    users = []
    with open(DATA_FILE, 'r') as f:
        for line in f:
            name, age, grade = line.strip().split(',')
            users.append({'name': name, 'age': int(age), 'grade': float(grade)})

    return jsonify(users)

if __name__ == "__main__":
    app.run(debug=True)
