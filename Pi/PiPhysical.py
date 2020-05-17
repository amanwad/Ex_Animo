import serial
import RPi.GPIO as GPIO
import time
import pyaudio
import wave
import board
import digitalio
import adafruit_character_lcd.character_lcd as characterlcd
from picamera import PiCamera
from google.cloud import storage

lcd_rs = digitalio.DigitalInOut(board.D26)
lcd_en = digitalio.DigitalInOut(board.D19)
lcd_d7 = digitalio.DigitalInOut(board.D27)
lcd_d6 = digitalio.DigitalInOut(board.D22)
lcd_d5 = digitalio.DigitalInOut(board.D24)
lcd_d4 = digitalio.DigitalInOut(board.D25)

lcd_columns = 16
lcd_rows = 2

camera = PiCamera()

lcd = characterlcd.Character_LCD_Mono(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows)

def recordAudio(form_1, chans, samp_rate, chunk, record_secs, dev_index, wav_name):
    stream = audio.open(format = form_1,rate = samp_rate,channels = chans, \
                    input_device_index = dev_index,input = True, \
                    frames_per_buffer=chunk)
    print("recording")
    frames = []

    for ii in range(0,int((samp_rate/chunk)*record_secs)):
        data = stream.read(chunk)
        frames.append(data)

    print("finished recording")


    stream.stop_stream()
    stream.close()
    #audio.terminate()

    wavefile = wave.open(wav_name,'wb')
    wavefile.setnchannels(chans)
    wavefile.setsampwidth(audio.get_sample_size(form_1))
    wavefile.setframerate(samp_rate)
    wavefile.writeframes(b''.join(frames))
    wavefile.close()



form_1 = pyaudio.paInt16 # 16-bit resolution
chans = 1 # 1 channel
samp_rate = 44100 
chunk = 4096
record_secs = 6 
dev_index = 2 
wav_output_filename = 'heartfile.wav'


audio = pyaudio.PyAudio() 

button = digitalio.DigitalInOut(board.D4)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP

def buttonFunc():
    while(button.value):
        pass

serObj = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
serObj.flush()
while(1):
    lcd.message = "Place\nstethoscope"
    time.sleep(2)
    lcd.clear()
    lcd.message = "on heart\nand press button"
    buttonFunc()
    print("Button pressed")
    lcd.clear()
    recordAudio(form_1, chans, samp_rate, chunk, record_secs, dev_index, wav_output_filename)
    lcd.message = "Place\nstethoscope"
    time.sleep(2)
    lcd.clear()
    lcd.message = "on chest\nand press button"
    buttonFunc()
    print("Button pressed")
    lcd.clear()
    wav_output_filename = 'breathing.wav'
    recordAudio(form_1, chans, samp_rate, chunk, record_secs, dev_index, wav_output_filename)
    audio.terminate()
    lcd.message = "Recording done"
    time.sleep(2)
    lcd.clear()
    camera.start_preview()
    lcd.message = "Point camera at\neye"
    time.sleep(2)
    lcd.clear()
    lcd.message = "and press button"
    buttonFunc()
    camera.capture("img.png")
    camera.stop_preview()
    lcd.clear()
    lcd.message = "Point camera at\nmouth"
    time.sleep(2)
    lcd.clear()
    lcd.message = "and press button"
    buttonFunc()
    camera.capture("img2.png")
    camera.stop_preview()
    lcd.clear()
    lcd.message = "Place\nthermometer"
    time.sleep(2)
    lcd.clear()
    lcd.message = "on forehead\nand press button"
    buttonFunc()
    print("Button pressed")
    print("Starting")
    #time.sleep(5)
    serObj.write(b"Hello World\n")
    while(not(serObj.in_waiting>0)):
        print("Waiting ", serObj.in_waiting)
    print("Found line")
    line = serObj.readline()
    f = open("temp.txt", "w")
    f.write(str(line))
    f.close()
    print(line)
    lcd.message = "Done"
    time.sleep(2)
    lcd.clear()
    storage_client = storage.Client.from_service_account_json('key_copy.json')
    bucket = storage_client.create_bucket("aman-w_cbtvfeww4yyordijm_5-17")
    blob = bucket.blob("Heartbeat")
    blob.upload_from_filename("heartfile.wav")
    blob = bucket.blob("Breathing")
    blob.upload_from_filename("breathing.wav")
    blob = bucket.blob("Temperature")
    blob.upload_from_filename("temp.txt")
    blob = bucket.blob("Eyes")
    blob.upload_from_filename("img.png")
    blob = bucket.blob("Mouth")
    blob.upload_from_filename("img2.png")
    
    
