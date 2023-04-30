import ultrasonic

while True:
    us = ultrasonic.Ultrasonic()
    distance, overflow = us.get_distance()
    print(f"Distance: {distance}\tOverflow:{overflow}")