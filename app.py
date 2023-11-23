import os
import csv
from flask import Flask, render_template, url_for, request, redirect

app = Flask(__name__)

os.environ['FLASK_DEBUG'] = 'True'

app.debug = os.environ.get('FLASK_DEBUG') == 'True'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/tasks')
def tasks():
    todo_tasks = []

    with open('bd_tasks.csv', newline='', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter=';')

        for r in reader:
            todo_tasks.append(1)

        return render_template('tasks.html', tasks=todo_tasks)


@app.route('/new_tasks')
def new_tasks():
    return render_template('new_tasks.html')


@app.route('/create_task', methods=['POST'])
def create_task():
    name_task = request.form['name_task']
    description_task = request.form['description_task']

    with open('bd_tasks.csv', 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow([name_task, description_task])

        redirect(url_for('/tasks'))


@app.route('/delete_task/<int:term_id>', methods=['POST'])
def delete_task(term_id):
    with open('bd_tasks.csv', 'r', newline='') as file:
        reader = csv.reader(file, delimiter=';')
        rows = list(reader)

    for i, row in enumerate(rows):
        if i == term_id:
            del rows[i]
            break

    with open('bd_tasks.csv', 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerows(rows)

    return redirect(url_for('/tasks'))


if __name__ == "__main__":
    app.run(debug=True)
