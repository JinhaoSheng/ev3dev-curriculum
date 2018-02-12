import mqtt_remote_method_calls as com
import tkinter
from tkinter import ttk


class MyDelegateOnThePc(object):
    """ Helper class that will receive MQTT messages from the EV3. """

    def __init__(self, label_to_display_messages_in):
        self.display_label = label_to_display_messages_in

    def button_pressed(self, message):
        self.display_label.configure(text=message)


def main():
    root = tkinter.Tk()
    root.title("Seeking my little brother")

    main_frame = ttk.Frame(root, padding=40, relief='raised')
    main_frame.grid()

    # LEB Labels and buttons
    left_side_label = ttk.Label(main_frame, text="Left LED")
    left_side_label.grid(row=0, column=0)

    left_green_button = ttk.Button(main_frame, text="Green")
    left_green_button.grid(row=1, column=0)
    left_green_button['command'] = lambda: send_led_command(mqtt_client, "left", "green")

    left_red_button = ttk.Button(main_frame, text="Red")
    left_red_button.grid(row=2, column=0)
    left_red_button['command'] = lambda: send_led_command(mqtt_client, "left", "red")

    left_black_button = ttk.Button(main_frame, text="Black")
    left_black_button.grid(row=3, column=0)
    left_black_button['command'] = lambda: send_led_command(mqtt_client, "left", "black")

    left_yellow_button = ttk.Button(main_frame, text="Yellow")
    left_yellow_button.grid(row=4, column=0)
    left_yellow_button['command'] = lambda: send_led_command(mqtt_client, "left", "yellow")

    button_label = ttk.Label(main_frame, text="  Button messages from EV3  ")
    button_label.grid(row=1, column=1)

    button_message = ttk.Label(main_frame, text="--")
    button_message.grid(row=2, column=1)

    right_side_label = ttk.Label(main_frame, text="Right LED")
    right_side_label.grid(row=0, column=2)

    right_green_button = ttk.Button(main_frame, text="Green")
    right_green_button.grid(row=1, column=2)
    right_green_button['command'] = lambda: send_led_command(mqtt_client, "right", "green")

    right_red_button = ttk.Button(main_frame, text="Red")
    right_red_button.grid(row=2, column=2)
    right_red_button['command'] = lambda: send_led_command(mqtt_client, "right", "red")

    right_black_button = ttk.Button(main_frame, text="Black")
    right_black_button.grid(row=3, column=2)
    right_black_button['command'] = lambda: send_led_command(mqtt_client, "right", "black")

    right_yellow_button = ttk.Button(main_frame, text="Yellow")
    right_yellow_button.grid(row=4, column=2)
    right_yellow_button['command'] = lambda: send_led_command(mqtt_client, "right", "yellow")

    spacer = ttk.Label(main_frame, text="")
    spacer.grid(row=5, column=2)

    pc_delegate = MyDelegateOnThePc(button_message)
    mqtt_client = com.MqttClient(pc_delegate)
    mqtt_client.connect_to_ev3()

    # Drive labels and buttons
    left_speed_label = ttk.Label(main_frame, text="Left")
    left_speed_label.grid(row=0, column=3)
    left_speed_entry = ttk.Entry(main_frame, width=8)
    left_speed_entry.insert(0, "600")
    left_speed_entry.grid(row=1, column=3)

    right_speed_label = ttk.Label(main_frame, text="Right")
    right_speed_label.grid(row=0, column=5)
    right_speed_entry = ttk.Entry(main_frame, width=8, justify=tkinter.RIGHT)
    right_speed_entry.insert(0, "600")
    right_speed_entry.grid(row=1, column=5)

    forward_button = ttk.Button(main_frame, text="Forward")
    forward_button.grid(row=2, column=4)
    # forward_button and '<Up>' key is done for your here...
    forward_button['command'] = lambda: send_forward(mqtt_client, left_speed_entry, right_speed_entry)
    root.bind('<Up>', lambda event: send_forward(mqtt_client, left_speed_entry, right_speed_entry))

    left_button = ttk.Button(main_frame, text="Left")
    left_button.grid(row=3, column=3)
    # left_button and '<Left>' key
    left_button['command'] = lambda: send_left(mqtt_client, left_speed_entry, right_speed_entry)
    root.bind('<Left>', lambda event: send_left(mqtt_client, left_speed_entry, right_speed_entry))

    stop_button = ttk.Button(main_frame, text="Stop")
    stop_button.grid(row=3, column=4)
    # stop_button and '<space>' key (note, does not need left_speed_entry, right_speed_entry)
    stop_button['command'] = lambda: send_stop(mqtt_client)
    root.bind('<space>', lambda event: send_stop(mqtt_client))

    right_button = ttk.Button(main_frame, text="Right")
    right_button.grid(row=3, column=5)
    # right_button and '<Right>' key
    right_button['command'] = lambda: send_right(mqtt_client, left_speed_entry, right_speed_entry)
    root.bind('<Right>', lambda event: send_right(mqtt_client, left_speed_entry, right_speed_entry))

    back_button = ttk.Button(main_frame, text="Back")
    back_button.grid(row=4, column=4)
    # back_button and '<Down>' key
    back_button['command'] = lambda: send_back(mqtt_client, left_speed_entry, right_speed_entry)
    root.bind('<Down>', lambda event: send_back(mqtt_client, left_speed_entry, right_speed_entry))

    up_button = ttk.Button(main_frame, text="Up")
    up_button.grid(row=5, column=3)
    up_button['command'] = lambda: send_up(mqtt_client)
    root.bind('<u>', lambda event: send_up(mqtt_client))

    down_button = ttk.Button(main_frame, text="Down")
    down_button.grid(row=6, column=3)
    down_button['command'] = lambda: send_down(mqtt_client)
    root.bind('<j>', lambda event: send_down(mqtt_client))

    # Button for seek_beacon
    seek_beacon_button = ttk.Button(main_frame, text="Seek beacon")
    seek_beacon_button.grid(row=6, column=4)
    seek_beacon_button['command'] = lambda: seek_beacon(mqtt_client)
    root.bind('<s>', lambda event: send_down(mqtt_client))

    # Buttons for quit and exit
    q_button = ttk.Button(main_frame, text="Quit")
    q_button.grid(row=5, column=5)
    q_button['command'] = (lambda: quit_program(mqtt_client, False))

    e_button = ttk.Button(main_frame, text="Exit")
    e_button.grid(row=6, column=5)
    e_button['command'] = (lambda: quit_program(mqtt_client, True))

    root.mainloop()


# ----------------------------------------------------------------------
# Tkinter callbacks
# ----------------------------------------------------------------------
def send_led_command(mqtt_client, led_side, led_color):
    print("Sending LED side = {}  LED color = {}".format(led_side, led_color))
    mqtt_client.send_message("set_led", [led_side, led_color])


# Motor command callbacks
def send_forward(mqtt_client, left_speed_entry, right_speed_entry):
    print("forward")
    mqtt_client.send_message("drive", [left_speed_entry.get(), right_speed_entry.get()])


def send_left(mqtt_client, left_speed_entry, right_speed_entry):
    print("left")
    mqtt_client.send_message("drive", [-int(left_speed_entry.get()), right_speed_entry.get()])


def send_right(mqtt_client, left_speed_entry, right_speed_entry):
    print("right")
    mqtt_client.send_message("drive", [left_speed_entry.get(), -int(right_speed_entry.get())])


def send_stop(mqtt_client):
    print("stop")
    mqtt_client.send_message("stop")


def send_back(mqtt_client, left_speed_entry, right_speed_entry):
    print("back")
    mqtt_client.send_message("drive", [-int(left_speed_entry.get()), -int(right_speed_entry.get())])


# Arm command callbacks
def send_up(mqtt_client):
    print("arm_up")
    mqtt_client.send_message("arm_up")


def send_down(mqtt_client):
    print("arm_down")
    mqtt_client.send_message("arm_down")


# Beacon seeking callback
def seek_beacon(mqtt_client):
    print("seek_beacon")
    mqtt_client.send_message("seek_beacon")


# Quit and Exit button callbacks
def quit_program(mqtt_client, shutdown_ev3):
    if shutdown_ev3:
        print("shutdown")
        mqtt_client.send_message("shutdown")
    mqtt_client.close()
    exit()


# ----------------------------------------------------------------------
# Calls  main  to start the ball rolling.
# ----------------------------------------------------------------------
main()
