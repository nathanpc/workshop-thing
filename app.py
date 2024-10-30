import flask
from flask import g

app = flask.Flask(
    __name__,
    static_url_path="",
    static_folder="static",
)

@app.get("/test")
def test_get():
    return "Hello workshop!"

@app.get("/tasks")
def list_tasks():
    if "tasks" not in g:
        g.tasks = ["Task 1", "Task 2"]
    return {
        'tasks': g.tasks
    }

@app.get('/')
def home():
    return flask.send_file('static/index.html')

if __name__ == "__main__":
    app.run(debug=True)
