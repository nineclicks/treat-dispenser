import RPi.GPIO as GPIO
import time
from flask import Flask, render_template
import threading


app = Flask('dispener-server')
lock = threading.Lock()
last_treat = 0
TREAT_MIN_SECONDS = 2

GPIO.setmode(GPIO.BOARD)
control_pins = [7,11,13,15]

for pin in control_pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, 0)

halfstep_seq = [
        [0,1,0,1],
        [0,0,0,1],
        [1,0,0,1],
        [1,0,0,0],
        [1,0,1,0],
        [0,0,1,0],
        [0,1,1,0],
        [0,1,0,0],
        ]

def get_step(n):
    x = n % len(halfstep_seq)
    return halfstep_seq[x]

pos = 0

def stop():
  for pin in range(4):
      GPIO.output(control_pins[pin], 1)

def step():
    with lock:
        global pos
        global last_treat

        if time.time() - last_treat < TREAT_MIN_SECONDS:
            return

        last_treat = time.time()
        for i in range(pos, pos+33):
            s = get_step(i)
            for pin in range(len(control_pins)):
              GPIO.output(control_pins[pin], 1-s[pin])
            time.sleep(.005)
        time.sleep(.1)
        stop()
        pos = pos + 33
        if pos % 100 == 99:
            pos += 1

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/step', methods=['POST'])
def call_step():
    step()
    return 'ok'
