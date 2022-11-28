def on_button_pressed_a():
    rekabit.set_servo_position(ServoChannel.S1, 45)
    for index in range(4):
        rekabit.set_rgb_pixel_color(0, 0xff8000)
        basic.pause(100)
        rekabit.set_rgb_pixel_color(0, 0x000000)
        basic.pause(100)
    zoombit.turn(TurnDirection.RIGHT, 128)
    basic.pause(500)
    zoombit.brake()
    rekabit.set_servo_position(ServoChannel.S1, 90)
input.on_button_pressed(Button.A, on_button_pressed_a)

def obstacle_avoidance():
    global distance
    distance = zoombit.read_ultrasonic()
    if distance < 10:
        zoombit.move(MotorDirection.BACKWARD, 128)
    elif distance < 20:
        zoombit.brake()
    else:
        zoombit.move(MotorDirection.FORWARD, 128)

def on_button_pressed_ab():
    rekabit.set_all_rgb_pixels_color(0x00ffff)
    zoombit.move(MotorDirection.FORWARD, 128)
    basic.pause(1000)
    zoombit.brake()
    rekabit.set_all_rgb_pixels_color(0x000000)
input.on_button_pressed(Button.AB, on_button_pressed_ab)

def on_button_pressed_b():
    rekabit.set_servo_position(ServoChannel.S1, 135)
    for index2 in range(4):
        rekabit.set_rgb_pixel_color(1, 0xff8000)
        basic.pause(100)
        rekabit.set_rgb_pixel_color(1, 0x000000)
        basic.pause(100)
    zoombit.turn(TurnDirection.LEFT, 128)
    basic.pause(500)
    zoombit.brake()
    rekabit.set_servo_position(ServoChannel.S1, 90)
input.on_button_pressed(Button.B, on_button_pressed_b)

def on_logo_pressed():
    global mode
    mode += 1
    zoombit.brake()
    if mode == 1:
        basic.show_icon(IconNames.HEART)
    elif mode == 2:
        basic.show_icon(IconNames.SQUARE)
    else:
        basic.show_leds("""
            . . . . .
                        . # # # .
                        # # # # #
                        # # # # #
                        . # . # .
        """)
        mode = 0
input.on_logo_event(TouchButtonEvent.PRESSED, on_logo_pressed)

def line_following():
    global position
    if zoombit.is_line_detected_on(LinePosition.CENTER):
        zoombit.move(MotorDirection.FORWARD, 128)
    elif zoombit.is_line_detected_on(LinePosition.LEFT1):
        zoombit.set_motors_speed(50, 100)
        position = 1
    elif zoombit.is_line_detected_on(LinePosition.RIGHT1):
        zoombit.set_motors_speed(100, 50)
        position = 2
    elif zoombit.is_line_detected_on(LinePosition.LEFT2):
        zoombit.set_motors_speed(0, 100)
        position = 1
    elif zoombit.is_line_detected_on(LinePosition.RIGHT2):
        zoombit.set_motors_speed(100, 0)
        position = 2
    elif zoombit.is_line_detected_on(LinePosition.NONE):
        # Check 'position' variable to determine where were the robot's last position before it's away from the line. Then turn the robot to move back to the line.
        if position == 1:
            zoombit.turn(TurnDirection.LEFT, 80)
        elif position == 2:
            zoombit.turn(TurnDirection.RIGHT, 80)
position = 0
distance = 0
mode = 0
music.play_sound_effect(music.builtin_sound_effect(soundExpression.giggle),
    SoundExpressionPlayMode.UNTIL_DONE)
basic.show_icon(IconNames.HAPPY)
zoombit.set_headlight(HeadlightChannel.ALL,
    zoombit.digital_state_picker(DigitalIoState.ON))
rekabit.set_servo_position(ServoChannel.S1, 90)
mode = 0

def on_forever():
    if mode == 1:
        obstacle_avoidance()
    elif mode == 2:
        line_following()
basic.forever(on_forever)
