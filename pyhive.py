from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import requests
import json
from tester import Tester
import time

app = Flask(__name__)


@app.route('/', methods=["POST", "GET"])
def hello_world():

    testobject = Tester()

    if request.method == "POST":

        formresults = request.form
        print(request.files)

        liststr = ""

        canvasstr = ""

        if 'file' not in request.files:

            #Do the text area json part
            print(formresults)
            textareajson = formresults['testinstructions']

            if textareajson == "":
                return render_template('index.html')

            print(textareajson)
            jsondict = json.loads(textareajson)

            for item in jsondict['tests']:
                liststr += "<li class='list-group-item'><em class='btn btn-primary'>URL</em> " + item['url'] + " <em class='btn btn-success'>  " + item['method'] + "  </em> requests = " + item['requestnumber'] + " <em class='btn btn-warning' style='color: white;'> Time </em>" + item['time'] + " seconds</li>"
                testobject.addjob(testname=item['testname'], url=item['url'], iterations=item['requestnumber'], timewait=item['time'])

            retval = testobject.starttests()

            print(retval)

            data = {"labels": [], "times": [], "testnames": []}

            for item in retval['Results']:
                data['labels'].append(item['starttime'])
                data['times'].append(item['totaltime'])
                data['testnames'].append(item['testname'])

            graphportionn = getrecentdata(data)


        file = request.files['file']

        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            #if the file is clicked but then canceled
            return render_template('index.html')
        if file:
            filecontents = request.files['file']

            filestr = filecontents.read()

            jsondict = json.loads(filestr)



            graphstring = ""
            canvasstring = ""
            urlstring = ""

            for item in jsondict['tests']:
                print("ITEM")
                print(item)

                testresults = Tester()
                testresults.addjob(item['testname'], item['url'], item['time'], item['requestnumber'])
                testresults = testresults.starttests()

                datainsert = getrecentdata(testresults)

                # graph inserts
                graphstring += "var colors = ['red', 'orange', 'yellow', 'green', 'blue', 'aqua', 'violet']; var ctx = document.getElementById('" + item['testname'] + "').getContext('2d'); var myChart = new Chart(ctx, { type: 'line', data: { " + datainsert + ", borderWidth: 1 }] }, options: { scales: { yAxes: [{ ticks: { beginAtZero:true } }] } } });"
                # list inserts
                urlstring += "<li class='list-group-item'><em class='btn btn-primary'>URL</em> " + item['url'] + " <em class='btn btn-success'> " + item['method'] + " </em>requests = " + item['requestnumber'] + " <em class='btn btn-warning' style='color: white;'> Time </em> " + item['time'] + " seconds  <em class='btn btn-danger'> " + item['testname'] + " </em></li>"
                # canvas inserts
                canvasstring += "<canvas id='" + item['testname'] + "' style='max-height: 100%; max-width: 100%;'></canvas>"


            return render_template('index.html', listed=urlstring, recentdatas=graphstring, canvasstringinsert=canvasstring)

    return render_template('index.html', listed="")

@app.route('/hivecentral')
def gethive():
    x = "<li class='list-group-item'><em class='btn btn-primary'>URL</em>http://www.google.com/ <em class='btn btn-success' > GET </em>requests = 100<em class='btn btn-warning' style='color: white;'> Time </em>5 seconds</li>"

    requesturl = ""
    requesttype = ""
    numrequests = ""
    time = ""

    return 'temp'

def createlinetxt(ids, inserts):

    counter = len(ids)

    count = 0

    retstr = ""

    while count < counter:
        x = "var colors = ['red', 'orange', 'yellow', 'green', 'blue', 'aqua', 'violet']; var ctx = document.getElementById('" + ids[count] +"').getContext('2d'); var myChart = new Chart(ctx, { type: 'line', data: { " + inserts[count] + ", borderWidth: 1 }] }, options: { scales: { yAxes: [{ ticks: { beginAtZero:true } }] } } });"
        count = count + 1
        retstr += x

    return retstr


def canvasstring(data):

    retstr = ""

    ids = []
    print("Print Data")
    print(data)
    print(type(data))
    for item in data:
        retstr += "<canvas id='" + item + "' style='max-height: 100%; max-width: 100%;'></canvas>"
        ids.append(item)

    return [retstr, ids]




def getrecentdata(data):
    tempnum = 0

    colors = ['rgba(16,16,255,0.2)', 'rgba(54, 162, 235, 0.2)', 'rgba(255, 206, 86, 0.2)','rgba(75, 192, 192, 0.2)', 'rgba(153, 102, 255, 0.2)', 'rgba(255, 159, 64, 0.2)']
    bordercolors = ['rgba(16,16,255,1.0)', 'rgba(54, 162, 235, 1.0)', 'rgba(255, 206, 86, 1.0)','rgba(75, 192, 192, 1.0)', 'rgba(153, 102, 255, 1.0)', 'rgba(255, 159, 64, 1.0)']

    newcolors = []
    newbordercolors = []

    datas = []
    labels = []

    times = []
    labelarr = []

    for key in data.keys():
        holder = data[key]

        for test in holder:
            times.append(test['totaltime'])
            labelarr.append(test['testname'])

    for item in times:
        datas.append(str(item))

    for item in labelarr:
        labels.append("'" + item + "'")

    while tempnum < len(datas):
        colornum = tempnum % len(colors)

        newcolors.append("'" + str(colors[colornum]) + "'")
        newbordercolors.append("'" + str(bordercolors[colornum]) + "'")
        tempnum += 1

    labels = "[" + ",".join(labels) + "]"
    datas = "[" + ",".join(datas) + "]"
    newcolors = "[" + ",".join(newcolors) + "]"
    newbordercolors = "[" + ",".join(newbordercolors) + "]"

    endstr = "labels: " + labels + ", datasets: [{ label: 'Response Times', data: " + datas + ", backgroundColor: " + newcolors + ", borderColor: " + newbordercolors
    return endstr

if __name__ == '__main__':
    app.run()
