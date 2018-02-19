import tkinter
from tkinter import ttk
import mqtt_remote_method_calls as com


class MyDelegate(object):

    def __init__(self, label_to_display_messages_in):
        self.display_label = label_to_display_messages_in

    def button_pressed(self, context):
        self.display_label.configure(text=context)


def main():

    mqtt_client = com.MqttClient()
    mqtt_client.connect_to_ev3()
    # mqtt_client = None # Delete this line, it was added temporarily so that the code we gave you had no errors.

    root = tkinter.Tk()
    root.title("MQTT Remote")

    main_frame = ttk.Frame(root, padding=40, relief='raised')
    main_frame.grid()

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

    up_button = ttk.Button(main_frame, text="Show off")
    up_button.grid(row=5, column=3)
    up_button['command'] = lambda: send_up(mqtt_client)
    root.bind('<u>', lambda event: send_up(mqtt_client))

    down_button = ttk.Button(main_frame, text="Not show off")
    down_button.grid(row=6, column=3)
    down_button['command'] = lambda: send_down(mqtt_client)
    root.bind('<j>', lambda event: send_down(mqtt_client))

    detect_cops_button = ttk.Button(main_frame, text="Detect police")
    detect_cops_button.grid(row=1, column=4)
    detect_cops_button['command'] = lambda: detect_cops(mqtt_client, left_speed_entry, right_speed_entry)

    # Buttons for quit and exit
    q_button = ttk.Button(main_frame, text="Quit")
    q_button.grid(row=5, column=5)
    q_button['command'] = (lambda: quit_program(mqtt_client, False))

    e_button = ttk.Button(main_frame, text="Exit")
    e_button.grid(row=6, column=5)
    e_button['command'] = (lambda: quit_program(mqtt_client, True))

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

    button_label = ttk.Label(main_frame, text="  Buttom messages from EV3  ")
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

    spacer = ttk.Label(main_frame, text="")
    spacer.grid(row=4, column=2)

    pc_delegate = MyDelegate(button_message)
    mqtt_client = com.MqttClient(pc_delegate)
    mqtt_client.connect_to_ev3()

    root.mainloop()

    # ----------------------------------------------------------------------
    # Tkinter callbacks
    # ----------------------------------------------------------------------


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


def send_up(mqtt_client):
    print("arm_up")
    mqtt_client.send_message("arm_up")


def send_down(mqtt_client):
    print("arm_down")
    mqtt_client.send_message("arm_down")


def detect_cops(mqtt_client, left_speed_entry, right_speed_entry):
    print("detect police")
    mqtt_client.send_message("detect_police", [left_speed_entry.get(), right_speed_entry.get()])

    # Quit and Exit button callbacks


def quit_program(mqtt_client, shutdown_ev3):
    if shutdown_ev3:
        print("shutdown")
        mqtt_client.send_message("shutdown")
    mqtt_client.close()
    exit()

def send_led_command(mqtt_client, led_side, led_color):
    print("Sending LED side = {}  LED color = {}".format(led_side, led_color))
    mqtt_client.send_message("set_led", [led_side, led_color])

    # ----------------------------------------------------------------------
    # Calls  main  to start the ball rolling.
    # ----------------------------------------------------------------------


main()
