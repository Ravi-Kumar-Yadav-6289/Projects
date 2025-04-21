from flask import Flask, render_template, request
# this render template is used to redirect to the required html files.
app = Flask(__name__)

@app.route("/")
def welcome():
    return render_template("index.html")

@app.route("/form", methods = ['GET', 'POST'])
def form():

    if request.method == 'POST':
        name = request.form.get('name')
        return f"Hello, {name}! Your form has been submitted successfully."

    return render_template("form.html")


if __name__ == "__main__":
    app.run(debug=True)