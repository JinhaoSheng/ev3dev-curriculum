import mqtt_remote_method_calls as com
import robot_controller as robo
import ev3dev.ev3 as ev3
import time


def main():
    ev3.Sound.speak('I am seeking my little brother, please give me the color key.')

    robot = robo.Snatch3r()
    mqtt_client = com.MqttClient(robot)
    mqtt_client.connect_to_pc()
    robot.loop_forever()  # Calls a function that has a while True: loop within it to avoid letting the program end.

    btn = ev3.Button()
    color_to_seek = 0

    if btn.up:
        ev3.Sound.speak('I can only pass the black card.')
        ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.BLACK)
        ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.BLACK)
        color_to_seek = ev3.ColorSensor.COLOR_BLACK
        time.sleep(1)

    if btn.left:
        ev3.Sound.speak('I can only pass the green card.')
        ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.GREEN)
        ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.GREEN)
        color_to_seek = ev3.ColorSensor.COLOR_GREEN
        time.sleep(1)

    if btn.right:
        ev3.Sound.speak('I can only pass the red card.')
        ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.RED)
        ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.RED)
        color_to_seek = ev3.ColorSensor.COLOR_RED
        time.sleep(1)

    if btn.down:
        ev3.Sound.speak('I can only pass the yellow card.')
        ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.YELLOW)
        ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.YELLOW)
        color_to_seek = ev3.ColorSensor.COLOR_YELLOW
        time.sleep(1)

    if btn.backspace:
        robot.shutdown()
        time.sleep(0.01)

    while robot.color_sensor.color != color_to_seek:
        robot.stop()

    found_beacon = robot.seek_beacon()
    if found_beacon:
        ev3.Sound.speak("I got the beacon")

# ----------------------------------------------------------------------
# Calls  main  to start the ball rolling.
# ----------------------------------------------------------------------


main()

