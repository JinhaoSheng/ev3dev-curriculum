"""
  Library of EV3 robot functions that are useful in many different applications. For example things
  like arm_up, arm_down, driving around, or doing things with the Pixy camera.

  Add commands as needed to support the features you'd like to implement.  For organizational
  purposes try to only write methods into this library that are NOT specific to one tasks, but
  rather methods that would be useful regardless of the activity.  For example, don't make
  a connection to the remote control that sends the arm up if the ir remote control up button
  is pressed.  That's a specific input --> output task.  Maybe some other task would want to use
  the IR remote up button for something different.  Instead just make a method called arm_up that
  could be called.  That way it's a generic action that could be used in any task.
"""

import ev3dev.ev3 as ev3
import time
import math


class Snatch3r(object):
    """Commands for the Snatch3r robot that might be useful in many different programs."""

    def __init__(self):
        """Constructs and connects two large motors on output ports B and C."""
        self.left_motor = ev3.LargeMotor(ev3.OUTPUT_B)
        self.right_motor = ev3.LargeMotor(ev3.OUTPUT_C)
        self.arm_motor = ev3.MediumMotor(ev3.OUTPUT_A)
        self.touch_sensor = ev3.TouchSensor()
        self.color_sensor = ev3.ColorSensor()
        self.ir_sensor = ev3.InfraredSensor()
        self.pixy = ev3.Sensor(driver_name="pixy-lego")
        self.color_key = None

        self.MAX_SPEED = 900
        self.running = True
        
        """Check that the motors are actually connected."""
        assert self.left_motor.connected
        assert self.right_motor.connected
        assert self.arm_motor.connected
        assert self.touch_sensor
        assert self.color_sensor
        assert self.ir_sensor
        assert self.pixy

    def drive_inches(self, inches_target, speed_deg_per_second):
        """Drives robot to move a given distance with a given speed."""
        self.left_motor.run_to_rel_pos(position_sp=inches_target * 90, speed_sp=speed_deg_per_second,
                                       stop_action=ev3.Motor.STOP_ACTION_BRAKE)
        self.right_motor.run_to_rel_pos(position_sp=inches_target * 90, speed_sp=speed_deg_per_second,
                                        stop_action=ev3.Motor.STOP_ACTION_BRAKE)
        self.left_motor.wait_while(ev3.Motor.STATE_RUNNING)
        self.right_motor.wait_while(ev3.Motor.STATE_RUNNING)
        ev3.Sound.beep().wait()

    def turn_degrees(self, degrees_to_turn, turn_speed_sp):
        """Makes robot do polygon motion."""
        self.left_motor.run_to_rel_pos(position_sp=-degrees_to_turn * 4.51, speed_sp=turn_speed_sp,
                                       stop_action=ev3.Motor.STOP_ACTION_BRAKE)
        self.right_motor.run_to_rel_pos(position_sp=degrees_to_turn * 4.51, speed_sp=turn_speed_sp,
                                        stop_action=ev3.Motor.STOP_ACTION_BRAKE)
        self.left_motor.wait_while(ev3.Motor.STATE_RUNNING)
        self.right_motor.wait_while(ev3.Motor.STATE_RUNNING)
        ev3.Sound.beep().wait()

    def drive(self, left_speed_entry, right_speed_entry):
        """Drive robot running."""
        self.left_motor.run_forever(speed_sp=left_speed_entry)
        self.right_motor.run_forever(speed_sp=right_speed_entry)

    def stop(self):
        """stops robot running."""
        self.left_motor.stop(stop_action="brake")
        self.right_motor.stop(stop_action="brake")

    def arm_calibration(self):
        """Makes arm do calibration."""
        self.arm_motor.run_forever(speed_sp=self.MAX_SPEED)
        while not self.touch_sensor.is_pressed:
            time.sleep(0.01)
        self.arm_motor.stop(stop_action="brake")
        ev3.Sound.beep().wait()

        arm_revolutions_for_full_range = 14.2
        self.arm_motor.run_to_rel_pos(position_sp=-arm_revolutions_for_full_range * 360, speed_sp=self.MAX_SPEED)
        self.arm_motor.wait_while(ev3.Motor.STATE_RUNNING)
        ev3.Sound.beep().wait()

        self.arm_motor.position = 0

    def arm_up(self):
        """Moves the Snatch3r arm to the up position."""
        self.arm_motor.run_forever(speed_sp=self.MAX_SPEED)
        while not self.touch_sensor.is_pressed:
            time.sleep(0.01)
        self.arm_motor.stop(stop_action="brake")
        ev3.Sound.beep().wait()

    def arm_down(self):
        """Moves the Snatch3r arm to the down position."""
        self.arm_motor.run_to_abs_pos(position_sp=0)
        self.arm_motor.wait_while(ev3.Motor.STATE_RUNNING)  # Blocks until the motor finishes running
        ev3.Sound.beep().wait()

    def shutdown(self):
        """Shuts down the robot to exit the program."""
        self.running = False
        self.left_motor.stop(stop_action="brake")
        self.right_motor.stop(stop_action="brake")
        self.arm_motor.stop(stop_action="brake")
        ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.GREEN)
        ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.GREEN)
        print("Goodbye!")
        ev3.Sound.speak("Goodbye").wait()

    def loop_forever(self):
        # This is a convenience method that I don't really recommend for most programs other than m5.
        #   This method is only useful if the only input to the robot is coming via mqtt.
        #   MQTT messages will still call methods, but no other input or output happens.
        # This method is given here since the concept might be confusing.
        self.running = True
        while self.running:
            time.sleep(0.1)  # Do nothing (except receive MQTT messages) until an MQTT message calls shutdown.

    def seek_beacon(self):
        """Uses the IR Sensor in BeaconSeeker mode to find the beacon.  If the beacon is found this return True.
        If the beacon is not found and the attempt is cancelled by hitting the touch sensor, return False."""
        beacon_seeker = ev3.BeaconSeeker(channel=1)
        forward_speed = 300
        turn_speed = 100

        while not self.touch_sensor.is_pressed:
            # The touch sensor can be used to abort the attempt (sometimes handy during testing)
            current_heading = beacon_seeker.heading  # use the beacon_seeker heading
            current_distance = beacon_seeker.distance  # use the beacon_seeker distance
            if current_distance == -128:
                # If the IR Remote is not found just sit idle for this program until it is moved.
                print("IR Remote not found. Distance is -128")
                self.stop()
            else:
                if math.fabs(current_heading) < 2:
                    # Close enough of a heading to move forward
                    print("On the right heading. Distance: ", current_distance)
                    if current_distance == 0:
                        self.stop()
                        return True
                    else:
                        self.drive(forward_speed, forward_speed)

                elif 2 <= math.fabs(current_heading) < 10:
                    if current_heading < 0:
                        self.drive(-turn_speed, turn_speed)
                        print("Adjusting heading: ", current_heading)
                    elif current_heading > 0:
                        self.drive(turn_speed, -turn_speed)
                        print("Adjusting heading: ", current_heading)

                elif math.fabs(current_heading) > 10:
                    self.stop()
                    print("Heading is too far off to fix: ", current_heading)

            time.sleep(0.2)

        # The touch_sensor was pressed to abort the attempt if this code runs.
        print("Abandon ship!")
        self.stop()
        return False

    def set_led(self, led_side_string, led_color_string):
        ev3.Sound.speak("I get the {} color key".format(led_color_string))
        time.sleep(0.1)
        led_side = None
        if led_side_string == "left":
            led_side = ev3.Leds.LEFT
        elif led_side_string == "right":
            led_side = ev3.Leds.RIGHT

        led_color = None
        if led_color_string == "green":
            led_color = ev3.Leds.GREEN
            self.color_key = ev3.ColorSensor.COLOR_GREEN
        elif led_color_string == "red":
            led_color = ev3.Leds.RED
            self.color_key = ev3.ColorSensor.COLOR_RED
        elif led_color_string == "black":
            led_color = ev3.Leds.BLACK
            self.color_key = ev3.ColorSensor.COLOR_BLACK
        elif led_color_string == "yellow":
            led_color = ev3.Leds.YELLOW
            self.color_key = ev3.ColorSensor.COLOR_YELLOW

        if led_side is None or led_color is None:
            print("Invalid parameters sent to set_led. led_side_string = {} led_color_string = {}".format(
                led_side_string, led_color_string))
        else:
            ev3.Leds.set_color(led_side, led_color)

    def detect_police(self, left_speed_entry, right_speed_entry):
        spl = int(left_speed_entry)
        spr = int(right_speed_entry)
        sp = (spl + spr) / 2
        self.pixy.mode = "ALL"
        while not self.touch_sensor.is_pressed:

            x = self.pixy.value(2)
            y = self.pixy.value(3)
            width = self.pixy.value(4)
            print('(X, Y) = ({}, {})'.format(x, y))

            if sp < 500:
                if width > 0:
                    if x > 0:
                        self.left_motor.stop(stop_action="brake")
                        self.right_motor.stop(stop_action="brake")
                        ev3.Sound.speak("This is not a big deal").wait()
                        break
                    else:
                        break
                else:
                    break
            else:
                if width > 0:
                    if x > 0:
                        self.left_motor.run_to_rel_pos(position_sp=-180 * 4.51, speed_sp=600,
                                                       stop_action=ev3.Motor.STOP_ACTION_BRAKE)
                        self.right_motor.run_to_rel_pos(position_sp=180 * 4.51, speed_sp=600,
                                                        stop_action=ev3.Motor.STOP_ACTION_BRAKE)
                        time.sleep(0.1)
                        ev3.Sound.speak("Run Run Run").wait()
                        time.sleep(0.1)
                        x = self.pixy.value(2)
                        self.left_motor.run_forever(speed_sp=self.MAX_SPEED)
                        self.right_motor.run_forever(speed_sp=self.MAX_SPEED)
                        print(x)
                        if width > 0:
                            if x > 0:
                                self.left_motor.stop(stop_action="brake")
                                self.right_motor.stop(stop_action="brake")
                                time.sleep(0.5)
                                ev3.Sound.speak("Game over").wait()
                                break
                    else:
                        break
                else:
                    break