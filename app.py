from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# In a real application, store users and tasks in a database.
users = {}
tasks = {}

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in users:
            return render_template('register.html', error='Username already taken.')

        users[username] = {'password': password}
        return redirect(url_for('login'))

    return render_template('register.html', error=None)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in users and users[username]['password'] == password:
            return redirect(url_for('dashboard', username=username))

        return render_template('login.html', error='Invalid username or password.')

    return render_template('login.html', error=None)

@app.route('/dashboard/<username>')
def dashboard(username):
    if username in users:
        user_tasks = tasks.get(username, [])
        return render_template('dashboard.html', username=username, tasks=user_tasks)
    else:
        return "User not found."

@app.route('/add_task', methods=['GET', 'POST'])
def add_task():
    username = request.args.get('username')

    if request.method == 'POST':
        title = request.form['title']
        due_date = request.form['due_date']

        # For this example, we'll add the new task to the tasks list for the specific user
        if username not in tasks:
            tasks[username] = []

        tasks[username].append({"title": title, "due_date": due_date})

        # Redirect back to the dashboard after adding the task
        return redirect(url_for('dashboard', username=username))

    return render_template('add_task.html', username=username)

@app.route('/remove_task', methods=['POST'])
def remove_task():
    username = request.form.get('username')
    title = request.form.get('title')

    if username in tasks and title:
        user_tasks = tasks[username]
        for task in user_tasks:
            if task['title'] == title:
                user_tasks.remove(task)
                break

    return redirect(url_for('dashboard', username=username))


if __name__ == '__main__':
    app.run(debug=True)

