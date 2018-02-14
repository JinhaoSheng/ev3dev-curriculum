import mqtt_remote_method_calls as com
import robot_controller as robo
import ev3dev.ev3 as ev3
import time


def main():
    print("--------------------------------------------")
    print(" Seeking my little brother.")
    print("--------------------------------------------")
    ev3.Sound.speak("I am seeking my little brother, please give me the color key.").wait()
    ev3.Leds.all_off()

    robot = robo.Snatch3r()
    my_delegate = robot
    mqtt_client = com.MqttClient(my_delegate)
    my_delegate.mqtt_client = mqtt_client
    mqtt_client.connect_to_pc()

    # Buttons on EV3
    btn = ev3.Button()
    btn.on_up = lambda state: handle_button_press(state, mqtt_client, "Where are you, my little brother?")
    btn.on_down = lambda state: handle_button_press(state, mqtt_client, "I really miss you.")
    btn.on_left = lambda state: handle_button_press(state, mqtt_client, "I must find you.")
    btn.on_right = lambda state: handle_button_press(state, mqtt_client, "Don't be afraid.")
    btn.on_backspace = lambda state: handle_shutdown(state, my_delegate)

    while my_delegate.running:
        btn.process()

        # Stop at the color card which you set initially, if this does not work, change it to drive to color method.
        if my_delegate.color_key == my_delegate.color_sensor.color:
            my_delegate.stop()
            ev3.Sound.speak("I get the right color key to the door to add petrol.").wait()
            time.sleep(5)
            my_delegate.drive_inches(7, 100)
            time.sleep(0.1)

    ev3.Sound.speak("Goodbye").wait()


# ----------------------------------------------------------------------
# Button event callback functions
# ----------------------------------------------------------------------
def handle_button_press(button_state, mqtt_client, message):
    """Handle IR / button event."""
    if button_state:
        ev3.Sound.speak(message).wait()
        mqtt_client.send_message("button_pressed", [message])


def handle_shutdown(button_state, my_delegate):
    """Exit the program."""
    if button_state:
        my_delegate.running = False


# ----------------------------------------------------------------------
# Calls  main  to start the ball rolling.
# ----------------------------------------------------------------------
main()
