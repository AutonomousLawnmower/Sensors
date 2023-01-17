import ultrasonic


while True:
    us = ultrasonic.Ultrasonic()
    distance = us.get_distance()
    print(distance)
    


