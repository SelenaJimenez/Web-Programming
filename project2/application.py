#Author: Selena Jiménez Lara
#Project 2

import os
import requests
from flask import Flask, jsonify, render_template, request
from flask_socketio import SocketIO, emit


#======================================================================================================================
#===================================GLOBAL STUFF=======================================================================
#======================================================================================================================
app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)
global name_ch
votes = {"yes": "", "no": 0, "maybe": 0}
channels=[]
allchannel={"channel0":{0:{"date":"","name":"","mess":""}}}
iniciochannel={}
max=100                 #Define a maximun of messages

#======================================================================================================================
#===================================START==============================================================================
#======================================================================================================================
@app.route("/",methods=["GET", "POST"])
def index():
    return render_template("index.html", data=channels)


#======================================================================================================================
#===================================SOCKET=============================================================================
#======================================================================================================================
@socketio.on("vote")
def vote(data):
    if data not in channels:
        allchannel.update({data:{0:{"date":"","name":"","mess":""}}})
        channels.append(data)  
        iniciochannel.update({data:{"star":0,"end":0}})
        emit("vote totals", channels, broadcast=True)
    else:	
        emit("alert",data='')

#======================================================================================================================
#===================================SEND MESSAGE=======================================================================
#======================================================================================================================
@socketio.on("SMsend")
def SMsend(data):
    name_channel=data['channel']                #Save the name of the saved channel
    x=iniciochannel[name_channel]["end"]
    if x<max:                                   #If there are less than 100 msg, then:
        allchannel[name_channel].update({x:data})
        iniciochannel[name_channel]["end"]=x+1
    else:                                                               
        y=iniciochannel[name_channel]["star"]
        iniciochannel[name_channel]["end"]=x+1
        iniciochannel[name_channel]["star"]=y+1
        del allchannel[name_channel][y]
        allchannel[name_channel].update({x+1:data})
    emit("msg totals", allchannel[name_channel], broadcast=True)


#======================================================================================================================
#===================================CHANNEL============================================================================
#======================================================================================================================
@app.route("/channel<string:name_channel>", methods=["GET", "POST"])
def channel(name_channel):
    socketio.emit("set channel", name_channel)
    return render_template("channel.html", channel=allchannel[name_channel],name_channel=name_channel)


#======================================================================================================================
#===================================MAIN===============================================================================
#======================================================================================================================
if __name__ == "__main__":
    app.debug = True
    app.run(host = '172.23.225.247',port=5005)      #My IP and port
    socketio.run(app)

#======================================================================================================================
#===================================THE END============================================================================
#======================================================================================================================


