import os
import csv
from flask import Flask, render_template, url_for, request, redirect

app = Flask(__name__)

os.environ['FLASK_DEBUG'] = 'True'

app.debug = os.environ.get('FLASK_DEBUG') == 'True'


# Rota padrão para a página index
@app.route('/')
def index():
    return render_template('index.html')


# Rota padrão para a página sobre
@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/glossary')
def glossary():
    glossary_terms = []

    with open('bd_glossary.csv', newline='', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter=';')

        for r in reader:
            glossary_terms.append(r)

        return render_template('glossary.html', glossary=glossary_terms)


@app.route('/new_term')
def new_term():
    return render_template('new_term.html')


@app.route('/create_term', methods=['POST'])
def create_term():
    term = request.form['term']
    description_term = request.form['description_term']

    with open('bd_glossary.csv', 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow([term, description_term])

        return redirect(url_for('glossary'))


@app.route('/delete_term/<int:term_id>', methods=['POST'])
def delete_term(term_id):
    with open('bd_glossary.csv', 'r', newline='') as file:
        reader = csv.reader(file, delimiter=';')
        rows = list(reader)

    for i, row in enumerate(rows):
        if i == term_id:
            del rows[i]
            break

    with open('bd_glossary.csv', 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerows(rows)

    return redirect(url_for('glossary'))


#
@app.route('/tasks')
def tasks():
    todo_tasks = []

    # Criando leitor CSV para percorrer o arquivo e inserir os dados na lista vazia
    with open('bd_tasks.csv', newline='', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter=';')

        for r in reader:
            todo_tasks.append(r)

        return render_template('tasks.html', tasks=todo_tasks)


# Função padrão para a página de criação de tarefa
@app.route('/new_tasks')
def new_tasks():
    return render_template('new_tasks.html')


# Função
@app.route('/create_task', methods=['POST'])
def create_task():
    name_task = request.form['name_task']
    description_task = request.form['description_task']

    with open('bd_tasks.csv', 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow([name_task, description_task])

        return redirect(url_for('tasks'))


# Função utilizada para deletar uma tarefa pelo ID dela
@app.route('/delete_task/<int:term_id>', methods=['POST'])
def delete_task(term_id):
    with open('bd_tasks.csv', 'r', newline='') as file:
        reader = csv.reader(file, delimiter=';')
        rows = list(reader)

    # Enumerate para percorrer um for e pegar o indice da nossa lista que contém o id para excluir
    for i, row in enumerate(rows):
        if i == term_id:
            del rows[i]
            break

    # Salvar alterações no arquivo
    with open('bd_tasks.csv', 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerows(rows)

    return redirect(url_for('tasks'))


@app.route('/search_bar/<int:term_id>')
def search_bar(term_id):
    with open('bd_tasks.csv', 'r', newline='') as bd_tasks, open('bd_glossary.csv', 'r', newline='') as bd_glossary:
        reader_tasks = csv.reader(bd_tasks, delimiter=';')
        reader_glossary = csv.reader(bd_glossary, delimiter=';')
        rows_tasks = list(reader_tasks)
        rows_glossary = list(reader_glossary)

        for i, row in zip(rows_tasks, rows_glossary):
            if i == term_id:
                search_task = rows_tasks[term_id]
                search_glossary = rows_glossary[term_id]

    return render_template('search_page.html', task=search_task, glossary=search_glossary)


if __name__ == "__main__":
    app.run(debug=True)
