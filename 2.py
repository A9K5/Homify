import datetime
import time
import pandas as pd
import requests
import json
from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, render_template, request, redirect, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId


app = Flask(__name__)

# ip address of the NodeMCU
node_ip = "http://192.168.1.6/"

# Database connection code
conn = MongoClient()
db = conn.miot  # conn.name_of_db
collection = db.mproj  # db.table_name
collec = db.newdata10  # db_table_name for pre data (initial fixed data)
collecForNew = db.newdata12  # db_table_name to store new status values from

collecForF = db.newdata11  # sample data for predictions (not used yet)

# database for next week predictions  ----has no status columns.
collPred = db.newdataPred

# GPIO.setmode(GPIO.BCM)

# Create a dictionary called pins to store the pin number, name, and pin state:
pins = {
    '23': {'name': 'GPIO 23', 'state': "LOW"},
    '24': {'name': 'GPIO 24', 'state': "LOW"}
}
device = "Light"
# Dataframe to store next one week predictions
dataframe_future_store = pd.DataFrame()

# Set each pin as an output and make it low:
# for pin in pins:
#     GPIO.setup(pin, GPIO.OUT)
#     GPIO.output(pin, GPIO.LOW)


# Scheduler 1
def Scheduler1():
    # read last 60 days of data stored in the mongodb
    try:
        cursor = collec.find().sort([('_id', -1)]).limit(5)
    except Exception as e:
        print(e)
    data = pd.DataFrame.from_dict([x for x in cursor], orient='columns')

    # clean the data and run ML Algo
    data['Time'] = (data['hr'].values * 60)
    data["CatStatus"] = data["Status"].astype('category')
    data['col1'] = pd.to_datetime(data['Timestamp'])
    import datetime as dt
    print(data.col1.dtype)
    data['col1'] = pd.to_datetime(data['col1'])
    data['col1'] = data['col1'].map(dt.datetime.toordinal)
    print(data.col1.dtype)
    from sklearn.preprocessing import LabelEncoder

    def MultiLabelEncoder(columnlist, dataframe):
        for i in columnlist:
            labelencoder_X = LabelEncoder()
            dataframe[i] = labelencoder_X.fit_transform(dataframe[i])
    columnlist = ['CatStatus']
    MultiLabelEncoder(columnlist, data)

    from sklearn.ensemble import ExtraTreesRegressor
    from sklearn.model_selection import cross_val_score
    from sklearn.model_selection import train_test_split

    columns = ['hr', 'min', 'col1']
    all_X = data[columns]
    all_y = data['CatStatus']
    train_X, test_X, train_y, test_y = train_test_split(
        all_X, all_y, test_size=0.20, random_state=0)

    model = ExtraTreesRegressor()
    model.fit(train_X, train_y)
    # preds = model.predict(X_test)
    # mean_absolute_error(y_test, preds)
    # scores = cross_val_score(model,all_X,all_y,cv=20)
    # accuracy = scores.mean()
    # print("scores",scores)
    # print("accuracy:",accuracy)

    # Generate test dates of the next one week
    # Get date for the next week
    for x in range(0, 1440*7 + 1, 10):
        # print("high", int(x/60), int(x % 60))
        collPred.insert_one(
            {"hr": int(x/60), "min": int(x % 60), "Device": device})
        # generate test entries in the database
    cursor = collPred.find().limit(1009)
    data_pred = pd.DataFrame.from_dict([x for x in cursor], orient='columns')

    # predict the usage pattern and write it to database
    output_pred_val = model.predict(data_pred[columns])
    data_pred['CatStatus'] = output_pred_val.tolist()
    # Store it
    dataframe_future_store = data_pred


# Scheduler 2
def Scheduler2():
    #  constantly read the predictions.
        # prediction stored in the dataframe_future_store .
        # get the time of the day and compare
    node_ip = "http://192.168.1.6/"
    currentDT = datetime.datetime.now()
    day_number = datetime.datetime.today().weekday()
    day_hour = currentDT.hour
    day_min = currentDT.minute
    # derived value to be queried from the dataframe.
    col_val = day_number * (60*24) + (day_hour * (int(day_min / 10) * 10))
    j = dataframe_future_store.loc[dataframe_future_store['col1']
                                   == col_val]['Status']
    s = pd.to_numeric(j)
    a = int(s.values)
    # take decisions based on that.
    # command nodeMCU to switch on
    # to be done later
    if a < 1:
        print('device to be switched OFF')
        print("The device status is OFF")
        # command the device from here
        # pinging the NodeMCU for Device status
        node_ip += "dev1/0/"
        r = requests.get(url=node_ip)
        data = r.json()  # got the device status in json format

    else:
        print('device to be switched on')
        print("The device status is ON")
        # command the device from here
        # pinging the NodeMCU for Device status
        node_ip += "dev1/1/"
        r = requests.get(url=node_ip)
        data = r.json()  # got the device status in json format


# Basically just getting the status of the device and storing it in database.
def Scheduler3():
    # ip address of the NodeMCU
    node_ip = "http://192.168.1.8/"
    # pinging the NodeMCU for Device status
    node_ip += "status/dev1/"
    r = requests.get(url=node_ip)
    print(r)
    data = r.json()  # got the device status in json format
    # Now enter the data into mongodb with timestamps
    # Create timestamps
    currentDT = datetime.datetime.now()
    day_number = datetime.datetime.today().weekday()
    day_hour = currentDT.hour
    day_min = currentDT.minute
    day_date = str(currentDT.year) + "-" + \
        str(currentDT.month) + "-" + str(currentDT.day)
    collecForNew.insert_one({"Timestamp": day_date, "hr": day_hour,
                             "min": day_min, "Status": data['Status'], "Device": data['Device']})
    print("Device status updated in the database")


list_device = []


# def Scheduler4():
#     # node_ip = "http://192.168.1.6/"
#     # node_ip += "dev1/0/"
#     # print(node_ip)

#     if len(list_device) > 0:
#         for i in range(len(list_device)):
#             node_ip = list_device.index(i+1)
#             print(node_ip)
#             del list_device[i]
#             try:
#                 r = requests.get(url=node_ip)
#                 data = r.json()
#                 print(r)
#             except Exception as e:
#                 print(e)


# Adding scheduler jobs
sched = BackgroundScheduler()
# sched.add_job(sensor, 'interval', seconds=15)
# sched.add_job(func=Scheduler1, trigger="cron", day_of_week="mon", id="job1")
# sched.add_job(func=Scheduler2, trigger="interval", seconds=30,  id='job2')
# sched.add_job(func=Scheduler3, trigger="interval", minutes=10,  id="job3")
# sched.add_job(func=Scheduler4, trigger="interval", seconds=5)
sched.start()


# make the part to regular update database on system status
def sensor():
    # For each pin, read the pin state and store it in the pins dictionary:
   #  for pin in pins:
   #      pins[pin]['state'] = GPIO.input(pin)

    now = datetime.datetime.now()
    # Put the pin dictionary into the template data dictionary:
    templateData = {
        'timestamp': time.time(),
        # for reconversion ==-- date = datetime.datetime.fromtimestamp(timestamp)

        # str(now.strftime("%Y-%m-%d-%H-%M")),
        'pins': pins
    }
    # write template data to the database
    # Mongo db code goes here
    rec_id1 = collection.insert_one(templateData)
    print(rec_id1)
    ###
    """ Function for test purposes. """
    print("Scheduler is alive!")

# For switching automation mode


@app.route("/automation1/", methods=['GET', 'POST'])
def automation1():
    # node_ip = "http://192.168.1.13/"
    # print(node_ip)
    # print (request.is_json)

    auto_id = request.get_json()
    print("--------", auto_id["auto"])
    if auto_id["auto"] == "on":
        # Change mode to ON
        try:
            a = sched.pause_job('job2')
            print(a)
        except Exception as e:
            print(e)
        print("Automation ON")
        data = {'Automation': "ON"}
        return json.dumps(data)

    elif auto_id["auto"] == "off":
        # Change mode to OFF
        try:
            a = sched.resume_job('job2')
            print(a)
        except Exception as e:
            print(e)
        print("Automation OFF")
        data = {'Autmation': "OFF"}
        return json.dumps(data)


# For switching off the device
@app.route("/switchboard1/", methods=['GET', 'POST'])
def switchboard1():
    # switchimp()
    node_ip = "http://192.168.1.13/"
    # print(node_ip)
    # print (request.is_json)
    dev_id = request.get_json()
    print("--------", dev_id)

    if dev_id["dev"] == "dev1":
        node_ip += "dev1/0/"
    elif dev_id["dev"] == "dev2":
        node_ip += "dev2/0/"
    elif dev_id["dev"] == "dev3":
        node_ip += "dev3/0/"

    print(node_ip)
    try:
        r = requests.get(url=node_ip)
        data = r.json()
        print(data)
    except Exception as e:
        print(e)
    # except:
    #     print("Request has no reponse")

    # templateData = {
    #     'pins': pins
    # }
    # list_device.append(node_ip)
    # print("Switchboard working")
    # return render_template('index.html')
    return json.dumps(data)

# For Switching on the device


@app.route("/switchboard2/", methods=['GET', 'POST'])
def switchboard2():
    # switchimp()
    node_ip = "http://192.168.1.13/"
    # print(node_ip)
    # print (request.is_json)

    dev_id = request.get_json()
    print("--------", dev_id)

    if dev_id["dev"] == "dev1":
        node_ip += "dev1/1/"
    elif dev_id["dev"] == "dev2":
        node_ip += "dev2/1/"
    elif dev_id["dev"] == "dev3":
        node_ip += "dev3/1/"

    try:
        r = requests.get(url=node_ip)
        data = r.json()
        print(data)
    except Exception as e:
        print(e)
    # except:
    #     print("Request has no reponse")

    # templateData = {
    #     'pins': pins
    # }
    # list_device.append(node_ip)
    # print("Switchboard working")
    return json.dumps(data)


def switchimp():
    node_ip = "http://192.168.1.9/"
    node_ip += "/dev1/0/"
    print(node_ip)
    try:
        r = requests.get('http://192.168.1.9/dev1/0/')
        data = r.json()
        print(data)
    except Exception as e:
        print(e)


@app.route("/")
def main():
    # For each pin, read the pin state and store it in the pins dictionary:
   #  for pin in pins:
   #      pins[pin]['state'] = GPIO.input(pin)
    # Put the pin dictionary into the template data dictionary:
    templateData = {
        'pins': pins
    }
    # Pass the template data into the template main.html and return it to the user
    return render_template('index.html', **templateData)


@app.route("/createData/")
def createData():
    return render_template("datasetcreater.html")


@app.route("/createDataset/")
def createDataset():
    # take the datetime here and create entries in the dataset
    return render_template("datasetcreater.html")


# creating stimulated values.

@app.route("/createEntry/", methods=['GET'])
def createEntry():
    device = "Light"  # request.arg("device")

    time1 = request.args.getlist("time1")
    time2 = request.args.getlist("time2")
    print("time1:", time1)
    # print("---")
    # print(time1[0].split())
    year1 = time1[0][:4]
    month1 = time1[0][5:7]
    day1 = time1[0][8:10]
    hr1 = int(time1[0][11:13])
    min1 = int(time1[0][14:16])
    hr1 = hr1 * 60 + min1
    print(hr1, "hr1")

    print("time2:", time2)
    # year2 = time2[0][:4]
    # month2 = time2[0][5:7]
    # day2 = time2[0][8:10]
    hr2 = int(time2[0][11:13])
    min2 = int(time2[0][14:16])
    hr2 = hr2 * 60 + min2
    print(hr2, "hr2")

    for x in range(0, 1441, 10):
        if (x >= hr1 and x <= hr2):
            print("high", int(x/60), int(x % 60))
            collecForF.insert_one({"Timestamp": time1[0][:10], "hr": int(
                x/60), "min": int(x % 60), "Status": 'HIGH', "Device": device})
            #Enter in mongodb
        else:
            print("Low", int(x/60), int(x % 60))
            # Enter times in mongodb
            collecForF.insert_one({"Timestamp": time1[0][:10], "hr": int(
                x/60), "min": int(x % 60), "Status": 'LOW', "Device": device})

    return redirect('/')

    # for x in range(0,25):
    #     for y in range(0,61,5):
    #         print(x,":",y)
    #         if (x >= hr1 and x <= hr2):
    #             if (y >= min1 and y <= min2):
    #                 print("High",x,":",y)
    #                 # outside time range Enter LOW in the light.
    #                 # pass
    #         else:
    #         #     #inside the time range Enter HIGH in the light.
    #         #     # print("HIGH",x,":",y)
    #             print(x,":",y)

    # return redirect('/')

# The function below is executed when someone requests a URL with the pin number and action in it:


@app.route("/<changePin>/<action>")
def action(changePin, action):
    # Convert the pin from the URL into an integer:
    changePin = int(changePin)
    # Get the device name for the pin being changed:
    deviceName = pins[changePin]['name']
    # If the action part of the URL is "on," execute the code indented below:
    if action == "on":
        # Set the pin high:
        #   GPIO.output(changePin, GPIO.HIGH)
        pins[changePin]['state'] = 'HIGH'
        # Save the status message to be passed into the template:
        print("Turned ", deviceName, " on.")
    if action == "off":
      #   GPIO.output(changePin, GPIO.LOW)
        pins[changePin]['state'] = 'LOW'
        print("Turned ", deviceName, " off.")

    # For each pin, read the pin state and store it in the pins dictionary:
   #  for pin in pins:
   #      pins[pin]['state'] = GPIO.input(pin)

    # Along with the pin dictionary, put the message into the template data dictionary:
    templateData = {
        'pins': pins
    }

    return render_template('main.html', **templateData)


if __name__ == "__main__":
    app.run(host='192.168.1.47', port=5000, debug=True)
