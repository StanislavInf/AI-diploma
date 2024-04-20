from datetime import datetime
import math
import time
import random
from flask import Flask, render_template, Response, request
from flask_socketio import SocketIO, emit
from threading import Lock

app = Flask(__name__)
socketio = SocketIO(app)

thread = None
thread_lock = Lock()

slider =  {1:0,
           2:0,
           3:0}

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('slider_change_1')
def handle_slider_change1(data):
    global slider
    slider[1] = int(data['value'])

@socketio.on('slider_change_2')
def handle_slider_change2(data):
    global slider
    slider[2] = int(data['value'])

@socketio.on('slider_change_3')
def handle_slider_change3(data):
    global slider
    slider[3] = int(data['value'])

def background_task():
    # socketio.sleep(1) # cпить
    charts = {0:[random.randint(1, slider[1]) for i in range(24)],
              1:[random.randint(1, slider[2]) for i in range(24)],
              2:[random.randint(1, slider[3]) for i in range(24)]}
    
    # передача
    socketio.emit('my_response', { 'data': charts})


@socketio.on('date_change')
def handle_date_change(date):
    print("Выполняется расчёт")
    background_task()

def gen():
    while(True):
        global slider
        print(slider)
@app.route('/render')
def video_feed():
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')
def gen_video():
    print()
@app.route('/video')
def video():
    return Response(    )




if __name__ == '__main__':
    socketio.run(app)
