import board
import busio
import sdcardio
import storage
import time
import random
import analogio
import digitalio
import audiomp3
import audiobusio

spi = busio.SPI(board.GP18, board.GP19, board.GP20)
sd = sdcardio.SDCard(spi, board.GP23)
vfs = storage.VfsFat(sd)
storage.mount(vfs, "/sd")
print("SD card mounted")

audio = audiobusio.I2SOut(board.GP9, board.GP10, board.GP11)
print("I2S audio ready")

from lcd.lcd import LCD, CursorMode
from lcd.i2c_pcf8574_interface import I2CPCF8574Interface
i2c = busio.I2C(scl=board.GP3, sda=board.GP2)
lcd = LCD(I2CPCF8574Interface(i2c, 0x27), num_rows=2, num_cols=16)
lcd.set_cursor_mode(CursorMode.HIDE)
print("LCD ready")

mp3_buffer = bytearray(8192)

Score = 0
lives = 3
DURATION = 7000
game_timer = 0
randNumber = 0

timeout = False

preGame = 0
GameInProgress = 1
LoseGame = 2
gameFinished = 3
GameState = preGame

pin2 = digitalio.DigitalInOut(board.GP4)
pin2.direction = digitalio.Direction.INPUT

pin3 = digitalio.DigitalInOut(board.GP13)
pin3.direction = digitalio.Direction.INPUT

pin4 = digitalio.DigitalInOut(board.GP12)
pin4.direction = digitalio.Direction.INPUT

pinA3 = analogio.AnalogIn(board.GP28)

pin7 = digitalio.DigitalInOut(board.GP26)
pin7.direction = digitalio.Direction.OUTPUT

pin8 = digitalio.DigitalInOut(board.GP27)
pin8.direction = digitalio.Direction.OUTPUT

print("Pins configured")

def millis():
    return time.monotonic_ns() // 1000000

def delay(ms):
    time.sleep(ms / 1000.0)

def digitalWrite(pin, val):
    pin.value = val

def digitalRead(pin):
    return pin.value

def analogRead(pin):
    return pin.value // 64

def setup():
    global GameState

    gamestart()
    setVolume(15)
    print("Playing intro...")
    play(4)

    GameState = preGame
    print("Waiting for start button...")

    random.seed(analogRead(pinA3))

def setVolume(vol):
    pass

def updateDisplay():
    lcd.clear()
    lcd.set_cursor_pos(0, 0)
    lcd.print("Score: " + str(Score))
    lcd.set_cursor_pos(1, 0)
    lcd.print("Lives: " + str(lives))

def playMp3FolderTrack(track):
    fname = "/sd/01/{:03d}.mp3".format(track)
    print("Loading:", fname)
    try:
        mp3 = audiomp3.MP3Decoder(open(fname, "rb"), mp3_buffer)
        audio.play(mp3)
        print("Playback started")
    except Exception as e:
        print("Audio error:", e)

def play(n):
    if n == 1:
        playMp3FolderTrack(1)
        delay(800)
    elif n == 2:
        playMp3FolderTrack(2)
        delay(800)
    elif n == 3:
        playMp3FolderTrack(3)
        delay(800)
    elif n == 4:
        playMp3FolderTrack(4)
        delay(9000)
    elif n == 5:
        playMp3FolderTrack(5)
        delay(14000)
    elif n == 6:
        playMp3FolderTrack(6)
        delay(13000)

def gamestart():
    global Score, DURATION, lives

    print("Resetting game state...")
    digitalWrite(pin7, False)
    digitalWrite(pin8, False)

    Score = 0
    lives = 3
    DURATION = 7000
    updateDisplay()

def timer():
    global DURATION
    DURATION = int(max(1500, 7000 - Score * 50))

def read(n):
    global timeout
    print("Waiting for player input... (timeout:", DURATION, "ms)")
    while not timeout:
        Pay_it = analogRead(pinA3)
        Mix = digitalRead(pin3)
        Call = digitalRead(pin4)

        if millis() - game_timer >= DURATION:
            print("Time's up!")
            timeout = True
            return False

        if n == 1 and Mix and not Call and Pay_it < 614:
            timeout = True
            return True
        if n == 2 and Call and not Mix and Pay_it < 614:
            timeout = True
            return True
        if n == 3 and Pay_it >= 614 and not Call and not Mix:
            timeout = True
            return True

        if (n == 1 and (Call or Pay_it >= 614)) or \
           (n == 2 and (Mix or Pay_it >= 614)) or \
           (n == 3 and (Call or Mix)):
            timeout = True
            return False

    return False

def loop():
    global GameState, randNumber, timeout, game_timer, Score, lives

    if GameState == preGame:
        if digitalRead(pin2) == True:
            print("Game started!")
            GameState = GameInProgress

    elif GameState == GameInProgress:
        randNumber = random.randint(1, 3)

        timeout = False

        commands = {1: "Mix It", 2: "Call It", 3: "Pay It"}
        print("Command:", commands[randNumber])
        play(randNumber)

        timer()
        print("Timer set:", DURATION, "ms")

        game_timer = millis()

        if read(randNumber):
            digitalWrite(pin8, True)

            Score += 1
            print("Correct! Score:", Score)
            updateDisplay()

            delay(1000)

            if Score == 99:
                GameState = gameFinished

            digitalWrite(pin8, False)
        else:
            digitalWrite(pin7, True)
            lives -= 1
            print("Wrong or timeout! Lives left:", lives, "Score:", Score)
            updateDisplay()
            delay(1000)
            digitalWrite(pin7, False)
            if lives == 0:
                GameState = LoseGame

    elif GameState == LoseGame:
        print("Game over! Final score:", Score)
        digitalWrite(pin7, True)
        play(5)
        delay(100)
        gamestart()
        GameState = preGame

    elif GameState == gameFinished:
        print("You win! Score:", Score)
        play(6)
        delay(1000)
        gamestart()
        GameState = preGame

setup()
print("Setup complete. Entering main loop.")
while True:
    loop()
