import mqtt_remote_method_calls as com
import robot_controller as robo
import ev3dev.ev3 as ev3
import time



def main():

    ev3.Leds.all_off()

    robot = robo.Snatch3r()
    my_delegate = robot
    mqtt_client = com.MqttClient(my_delegate)
    my_delegate.mqtt_client = mqtt_client
    mqtt_client.connect_to_pc()


    btn = ev3.Button()
    btn.on_up = lambda state: handle_button_press(state, mqtt_client, "I have 100 points, Black is 70 points")
    btn.on_down = lambda state: handle_button_press(state, mqtt_client, "Green is 50 points, B")
    btn.on_left = lambda state: handle_button_press(state, mqtt_client, "Red is 30 points")
    btn.on_right = lambda state: handle_button_press(state, mqtt_client, "Yellow is 20 points")
    btn.on_backspace = lambda state: handle_shutdown(state, my_delegate)

    while my_delegate.running:
        btn.process()


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

main()