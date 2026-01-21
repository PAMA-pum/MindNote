from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def hello_world():
	firstName = "Patthama"
	lastName = "Pangthaisong"
    
	return render_template("home.html", firstName=firstName, lastName=lastName)

@app.route("/about")
def about():
	firstName = "Patthama"
	lastName = "Pangthaisong"
	age = "19"
    
	return render_template("about.html", firstName=firstName, lastName=lastName, age=age)

@app.route("/xyz")
def xyzPage():
    return "<p>Page2</p>"

if __name__ == "__main__":
    app.run(debug=True)