import flask

app = flask.Flask(
    __name__,
    static_url_path="",
    static_folder="static",
)

@app.get("/test")
def test_get():
    return "Hello workshop!"

@app.get('/')
def home():
    return flask.send_file('static/index.html')

if __name__ == "__main__":
    app.run(debug=True)
