import mqtt_remote_method_calls as com
import robot_controller as robo
import ev3dev.ev3 as ev3
import time


def main():
    robot = robo.Snatch3r()
    mqtt_client = com.MqttClient(robot)
    mqtt_client.connect_to_pc()
    robot.loop_forever()  # Calls a function that has a while True: loop within it to avoid letting the program end.

    btn = ev3.Button()

    if btn.up:
        ev3.Sound.speak('I can only pass the black card.')
        ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.BLACK)
        ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.BLACK)
        time.sleep(1)

    if btn.left:
        ev3.Sound.speak('I can only pass the green card.')
        ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.GREEN)
        ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.GREEN)
        time.sleep(1)

    if btn.right:
        ev3.Sound.speak('I can only pass the red card.')
        ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.RED)
        ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.RED)
        time.sleep(1)

    if btn.down:
        ev3.Sound.speak('I can only pass the amber card.')
        ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.AMBER)
        ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.AMBER)
        time.sleep(1)

    if btn.backspace:
        robot.shutdown()
        time.sleep(0.01)

    found_beacon = robot.seek_beacon()
    if found_beacon:
        ev3.Sound.speak("I got the beacon")

# ----------------------------------------------------------------------
# Calls  main  to start the ball rolling.
# ----------------------------------------------------------------------


main()

