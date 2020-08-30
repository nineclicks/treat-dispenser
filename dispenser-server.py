import RPi.GPIO as GPIO
import time
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
  global pos
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

while True:
  time.sleep(10)
  step()
