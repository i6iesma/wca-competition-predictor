from flask import Flask, jsonify, render_template, request
import json
import sys
sys.path.insert(1, './backend')
import main as backend
app = Flask(__name__)
application = app

class AllUsers():
    pb_users = []
    smart_prediction_users = []
    def __init__(self, pb_users, smart_prediction_users) -> None:
        self.pb_users = pb_users
        self.smart_prediction_users = smart_prediction_users
current_users = AllUsers([], [])
@app.route('/', methods=["POST", "GET"])
def index():
    if request.method == "GET":
        return render_template('index.html', users=[], event="", format="", len_users = 0,  url="")
    elif request.method == "POST":

        url = request.form.get('url')
        format = request.form.get('format')
        event = request.form.get('event')
        #Set the text on the fields and dropdowns to the option
        mode = "pb"
        print("event is " + str(event))
        #Get the users from the backend
        #Filter the competition id from url like this https://www.worldcubeassociation.org/competitions/LazarilloOpen2023
        competition_id = str(url).strip("https://www.worldcubeassociation.org/competitions/")
        #Get all the users already sorted
        pb_users, smart_prediction_users = backend.main(competition_id, event, format) 
        mode_text = "By PB on the event specified"
        #This is a very cheap trick which basically I take all of the user data that I need in 
        #The javascript and place it in a hidden paragraph at the end of the page so js can access it
        jsonified_pb_users = json.dumps(pb_users, indent=2)
        jsonified_smart_prediction_users = json.dumps(smart_prediction_users, indent=2)
        return render_template('index.html',  pb_users=pb_users, mode_text=mode_text,event=event, format=format, url=url, mode=mode, jsonified_pb_users=jsonified_pb_users, jsonified_smart_prediction_users=jsonified_smart_prediction_users)

        
if __name__ == "__main__":
    app.run(debug=True)
