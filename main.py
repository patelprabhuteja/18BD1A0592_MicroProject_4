import requests
from flask import Flask, render_template, request, redirect
from twilio.rest import Client

account_sid = ""
auth_token = ""

client = Client(account_sid, auth_token)
app = Flask(__name__, static_url_path="/static")

@app.route('/')
def show_form():
    return render_template("index.html")

@app.route("/checkStatus", methods=["POST", "GET"])
def check_status():
    if request.method == "GET":
        return redirect("/")
    fname = request.form["fname"]
    lname = request.form["lname"]
    phnno = request.form["phnno"]
    email = request.form["email"]
    aadharNo = request.form["aadhar"]
    sstate = request.form["sstate"]
    scity = request.form["scity"]
    dstate = request.form["dstate"]
    dcity = request.form["dcity"]
    name = fname + " " + lname
    fromAdd = scity + ", " + sstate
    toAdd = dcity + ", " + dstate
    r = requests.get("https://api.covid19india.org/v4/data.json")
    data = r.json()
    try:
        confirmedCases = data[dstate]["districts"][dcity]["total"]["confirmed"]
        population = data[dstate]["districts"][dcity]["meta"]["population"]
    except KeyError:
        return render_template("index.html")
    percentageAffected = (confirmedCases / population) * 100
    if percentageAffected < 30:
        status = "Accepted"
    else:
        status = "Rejected"
    print("+91"+phnno)
    client.messages.create(to="+91"+phnno, from_="", body="Hello " + name + ", Your travel request from " + scity + "," + sstate + " to " + dcity+","+dstate+" has been "+status+".")
    return render_template("status.html", name=name, email=email, aadhar=aadharNo, phnno=phnno, fromAdd=fromAdd,
                           toAdd=toAdd, status=status)

if __name__ == '__main__':
    app.run()
