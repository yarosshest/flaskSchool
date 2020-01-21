from flask import Flask, request, redirect, url_for
# импортируем библиотеку для работы с файловой системой операционной системы
import os
import jinja2
import EnterInSystem

app = Flask(__name__)

# сохраняем в строковую переменную
template_dir = os.path.join(os.path.dirname(__file__), 'templates')
# создаем окружение для шаблона
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=True)

template = '1.html'
params = {'name': 'Josh', 'lastname': 'Scogin'}
t = jinja_env.get_template(template)
t.render(params)

@app.route("/UserLab")
def UserLab():
    return render('UserLab.html')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['Email']
        password = request.form['password']
        replay = EnterInSystem.LoginUser(email, password)
        if replay == "Login success":
            return redirect(url_for('UserLab'))
    else:
        return render('login.html')


@app.route('/', methods=['GET', 'POST'])
def registr():
    if request.method == 'POST':
        email = request.form['Email']
        password = request.form['password']
        EnterInSystem.RegisterUser(email, password, '')
        return redirect(url_for('login'))
    else:
        return render('registr.html')


def render(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)


if __name__ == '__main__':
    app.run()
