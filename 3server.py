import socket as sck
import time
import RPi.GPIO as GPIO  # Libreria per controllare i GPIO del Raspberry Pi

class AlphaBot(object):
    """
    Classe per controllare il robot AlphaBot. Configura i pin GPIO e fornisce metodi
    per muovere il robot in avanti, indietro, sinistra, destra o fermarlo.
    """
    def __init__(self, in1=13, in2=12, ena=6, in3=21, in4=20, enb=26):
        self.IN1 = in1
        self.IN2 = in2
        self.IN3 = in3
        self.IN4 = in4
        self.ENA = ena
        self.ENB = enb
        self.PA = 20  # Velocità di rotazione del motore sinistro
        self.PB = 20  # Velocità di rotazione del motore destro

        # Configurazione dei pin GPIO come output
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.IN1, GPIO.OUT)
        GPIO.setup(self.IN2, GPIO.OUT)
        GPIO.setup(self.IN3, GPIO.OUT)
        GPIO.setup(self.IN4, GPIO.OUT)
        GPIO.setup(self.ENA, GPIO.OUT)
        GPIO.setup(self.ENB, GPIO.OUT)

        # Configurazione della PWM per i motori
        self.PWMA = GPIO.PWM(self.ENA, 500)
        self.PWMB = GPIO.PWM(self.ENB, 500)
        self.PWMA.start(self.PA)
        self.PWMB.start(self.PB)
        self.stop()  # Arresta il robot all'inizio

    def stop(self):
        """Ferma il robot."""
        self.PWMA.ChangeDutyCycle(0)
        self.PWMB.ChangeDutyCycle(0)
        GPIO.output(self.IN1, GPIO.LOW)
        GPIO.output(self.IN2, GPIO.LOW)
        GPIO.output(self.IN3, GPIO.LOW)
        GPIO.output(self.IN4, GPIO.LOW)

    def forward(self, speed=60):
        """Muove il robot in avanti."""
        self.PWMA.ChangeDutyCycle(speed)
        self.PWMB.ChangeDutyCycle(speed)
        GPIO.output(self.IN1, GPIO.LOW)
        GPIO.output(self.IN2, GPIO.HIGH)
        GPIO.output(self.IN3, GPIO.HIGH)
        GPIO.output(self.IN4, GPIO.LOW)

    def backward(self, speed=60):
        """Muove il robot indietro."""
        self.PWMA.ChangeDutyCycle(speed)
        self.PWMB.ChangeDutyCycle(speed)
        GPIO.output(self.IN1, GPIO.HIGH)
        GPIO.output(self.IN2, GPIO.LOW)
        GPIO.output(self.IN3, GPIO.LOW)
        GPIO.output(self.IN4, GPIO.HIGH)

    def left(self, speed=25):
        """Gira il robot a sinistra."""
        self.PWMA.ChangeDutyCycle(speed)
        self.PWMB.ChangeDutyCycle(speed)
        GPIO.output(self.IN1, GPIO.HIGH)
        GPIO.output(self.IN2, GPIO.LOW)
        GPIO.output(self.IN3, GPIO.HIGH)
        GPIO.output(self.IN4, GPIO.LOW)

    def right(self, speed=25):
        """Gira il robot a destra."""
        self.PWMA.ChangeDutyCycle(speed)
        self.PWMB.ChangeDutyCycle(speed)
        GPIO.output(self.IN1, GPIO.LOW)
        GPIO.output(self.IN2, GPIO.HIGH)
        GPIO.output(self.IN3, GPIO.LOW)
        GPIO.output(self.IN4, GPIO.HIGH)

    def set_pwm_a(self, value):
        """Imposta la velocità del motore sinistro."""
        self.PA = value
        self.PWMA.ChangeDutyCycle(self.PA)

    def set_pwm_b(self, value):
        """Imposta la velocità del motore destro."""
        self.PB = value
        self.PWMB.ChangeDutyCycle(self.PB)

    def set_motor(self, left, right):
        """Controlla entrambi i motori con valori separati per sinistra e destra."""
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


# Configurazione del server
MY_ADDRESS = ("192.168.1.140", 9090)
BUFFER_SIZE = 4096

def main():
    alphaBot = AlphaBot()
    alphaBot.stop()  # Arresta il robot all'inizio

    # Creazione e configurazione del socket TCP
    s = sck.socket(sck.AF_INET, sck.SOCK_STREAM)
    s.bind(MY_ADDRESS)
    s.listen()

    connection, client_address = s.accept()
    print(f"Il client {client_address} si è connesso")

    # Loop principale per gestire i comandi
    while True:
        message = connection.recv(BUFFER_SIZE)  # Ricezione dei dati dal client
        direz_decode = message.decode()

        # Controllo del comando ricevuto
        if direz_decode == "w":
            print("avanti")
            alphaBot.forward()
        elif direz_decode == "s":
            print("indietro")
            alphaBot.backward()
        elif direz_decode == "a":
            print("sinistra")
            alphaBot.left()
        elif direz_decode == "d":
            print("destra")
            alphaBot.right()
        elif direz_decode.isupper():  # Ferma il robot se il comando è maiuscolo
            print("stop")
            alphaBot.stop()

    # Chiusura del socket
    s.close()

if __name__ == "__main__":
    main()
