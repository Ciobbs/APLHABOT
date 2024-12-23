#!/usr/bin/python
# _*_ coding: utf-8 -*-
# server tpc

# Server copy on the alphabot

import socket as sck
import threading as thr
import time
import RPi.GPIO as GPIO

client_list = []

class AlphaBot(object):  # Alphabot class

    def __init__(self, in1=13, in2=12, ena=6, in3=21, in4=20, enb=26):
        self.IN1 = in1
        self.IN2 = in2
        self.IN3 = in3
        self.IN4 = in4
        self.ENA = ena
        self.ENB = enb
        self.PA = 20  # turning speed
        self.PB = 20  # turning speed  

        # motors
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.IN1, GPIO.OUT)
        GPIO.setup(self.IN2, GPIO.OUT)
        GPIO.setup(self.IN3, GPIO.OUT)
        GPIO.setup(self.IN4, GPIO.OUT)
        GPIO.setup(self.ENA, GPIO.OUT)
        GPIO.setup(self.ENB, GPIO.OUT)
        self.PWMA = GPIO.PWM(self.ENA, 500)
        self.PWMB = GPIO.PWM(self.ENB, 500)
        self.PWMA.start(self.PA)
        self.PWMB.start(self.PB)
        self.stop()

    def stop(self):  # stop the motors
        self.PWMA.ChangeDutyCycle(0)
        self.PWMB.ChangeDutyCycle(0)
        GPIO.output(self.IN1, GPIO.LOW)
        GPIO.output(self.IN2, GPIO.LOW)
        GPIO.output(self.IN3, GPIO.LOW)
        GPIO.output(self.IN4, GPIO.LOW)

    def forward(self, speed=60):  # forward speed 60
        self.PWMA.ChangeDutyCycle(speed)
        self.PWMB.ChangeDutyCycle(speed)
        GPIO.output(self.IN1, GPIO.LOW)
        GPIO.output(self.IN2, GPIO.HIGH)
        GPIO.output(self.IN3, GPIO.HIGH)
        GPIO.output(self.IN4, GPIO.LOW)
        
    def backward(self, speed=60):  
        self.PWMA.ChangeDutyCycle(speed)
        self.PWMB.ChangeDutyCycle(speed)
        GPIO.output(self.IN1, GPIO.HIGH)
        GPIO.output(self.IN2, GPIO.LOW)
        GPIO.output(self.IN3, GPIO.LOW)
        GPIO.output(self.IN4, GPIO.HIGH)    
        
    def left(self, speed=25):  #turning left
        self.PWMA.ChangeDutyCycle(speed)
        self.PWMB.ChangeDutyCycle(speed)
        GPIO.output(self.IN1, GPIO.HIGH)
        GPIO.output(self.IN2, GPIO.LOW)
        GPIO.output(self.IN3, GPIO.HIGH)
        GPIO.output(self.IN4, GPIO.LOW)  

    def right(self, speed=25):  # right speed 25
        self.PWMA.ChangeDutyCycle(speed)
        self.PWMB.ChangeDutyCycle(speed)
        GPIO.output(self.IN1, GPIO.LOW)
        GPIO.output(self.IN2, GPIO.HIGH)
        GPIO.output(self.IN3, GPIO.LOW)
        GPIO.output(self.IN4, GPIO.HIGH)

    def set_pwm_a(self, value):
        self.PA = value
        self.PWMA.ChangeDutyCycle(self.PA)

    def set_pwm_b(self, value):
        self.PB = value
        self.PWMB.ChangeDutyCycle(self.PB)

    def set_motor(self, left, right):
        if (right >= 0) and (right <= 100):
            GPIO.output(self.IN1, GPIO.HIGH)
            GPIO.output(self.IN2, GPIO.LOW)
            self.PWMA.ChangeDutyCycle(right)
        elif (right < 0) and (right >= -100):
            GPIO.output(self.IN1, GPIO.LOW)
            GPIO.output(self.IN2, GPIO.HIGH)
            self.PWMA.ChangeDutyCycle(0 - right)
        if (left >= 0) and (left <= 100):
            GPIO.output(self.IN3, GPIO.HIGH)
            GPIO.output(self.IN4, GPIO.LOW)
            self.PWMB.ChangeDutyCycle(left)
        elif (left < 0) and (left >= -100):
            GPIO.output(self.IN3, GPIO.LOW)
            GPIO.output(self.IN4, GPIO.HIGH)
            self.PWMB.ChangeDutyCycle(0 - left)


def main():
    s = sck.socket(sck.AF_INET, sck.SOCK_STREAM)
    s.bind(("0.0.0.0", 9000))  # bind of tcp server 
    s.listen()
    Ab = AlphaBot()  # initializing alphabot

    running = True

    connection, address = s.accept()  # client connection


    while running:  # infinite loop
        message = (connection.recv(4096)).decode()  # receive command
        comando = message.split('|')[0]
        tempo = int(message.split('|')[1])
        if comando == "exit":  # for closing the program
            running = False

            client_list.remove()

        else:
            print(f"{comando} : {tempo}")

            if comando.upper().startswith("F"):  # forward
                Ab.forward()
                time.sleep(tempo)
                Ab.stop()

            if comando.upper().startswith("R"):  # right
                Ab.right()
                time.sleep(tempo)
                Ab.stop()

            if comando.upper().startswith("L"):  # left
                Ab.left()
                time.sleep(tempo)
                Ab.stop()
                
            if comando.upper().startswith("B"): #backward
                Ab.backward()
                time.sleep(tempo)
                Ab.stop()

            if comando.upper().startswith("STOP"):  # stop
                Ab.stop()

    s.close()

if __name__ == "__main__":
    main()