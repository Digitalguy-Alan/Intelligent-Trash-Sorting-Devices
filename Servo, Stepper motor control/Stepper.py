import RPi.GPIO as GPIO
import time

if __name__ == '__main__':
    ServoPin1 = 21
    ServoPin2 = 20
    PWMFreq = 50                        

    GPIO.setmode(GPIO.BCM)            
    GPIO.setup(ServoPin1, GPIO.OUT)
    GPIO.setup(ServoPin2, GPIO.OUT)   
    pwm1 = GPIO.PWM(ServoPin1, PWMFreq)
    pwm2 = GPIO.PWM(ServoPin2, PWMFreq)
    pwm1.start(0)
    pwm2.start(0)
    pwm1.ChangeDutyCycle(7.5)
    pwm2.ChangeDutyCycle(7.5)

    try:
        while True:
            trash_type = float(input("Pleas input the trash type: "))
            if trash_type == 1:
               duty2 = 7.5
               duty1 = 12.5
               pwm1.ChangeDutyCycle(duty1)
               pwm2.ChangeDutyCycle(duty2)
               time.sleep(2)
               pwm1.ChangeDutyCycle(7.5)
               pwm2.ChangeDutyCycle(7.5)
               continue
            if trash_type == 2:
               duty2 = 7.5
               duty1 = 2.5
               pwm1.ChangeDutyCycle(duty1)
               pwm2.ChangeDutyCycle(duty2)
               time.sleep(2)
               pwm1.ChangeDutyCycle(7.5)
               pwm2.ChangeDutyCycle(7.5)
               continue
            if trash_type == 3:
               duty2 = 12.5
               duty1 = 2.5
               pwm1.ChangeDutyCycle(duty1)
               pwm2.ChangeDutyCycle(duty2)
               time.sleep(2)
               pwm1.ChangeDutyCycle(7.5)
               pwm2.ChangeDutyCycle(7.5)
               continue
            if trash_type == 4:
               duty2 = 12.5
               duty1 = 12.5
               pwm1.ChangeDutyCycle(duty1)
               pwm2.ChangeDutyCycle(duty2)
               time.sleep(2)
               pwm1.ChangeDutyCycle(7.5)
               pwm2.ChangeDutyCycle(7.5)
               continue
    finally:
        pwm1.stop()
        pwm2.stop()
        GPIO.cleanup()                  
