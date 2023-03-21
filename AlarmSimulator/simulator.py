
from flask import Flask, jsonify, request
import json
from playsound import playsound
import threading

print("hello1")

app = Flask(__name__)
signal = [False]
def play_alarm(path:str):
    while True:
        if signal[0]:
            print("playing")
            playsound(path)
t = threading.Thread(target = play_alarm,args=['beep.mp3'])



@app.route('/', methods = ['POST'])
def alarmHandler():
    message = json.loads(request.data)
    status = message["status"]
    res = {'message' : None}
    if status == 1:
        res.update({'message' : 'Alarm is on'})
        signal[0] = True
    else:
        signal[0] = False
        res.update({'message' : 'Alarm is off'})
    return jsonify(res)
    
if __name__ == '__main__':
    print("hello2")
    t.start()
    app.run(debug = False)
    print("hello3")
    