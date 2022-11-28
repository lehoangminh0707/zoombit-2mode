input.onButtonPressed(Button.A, function () {
    rekabit.setServoPosition(ServoChannel.S1, 45)
    for (let index = 0; index < 4; index++) {
        rekabit.setRgbPixelColor(0, 0xff8000)
        basic.pause(100)
        rekabit.setRgbPixelColor(0, 0x000000)
        basic.pause(100)
    }
    zoombit.turn(TurnDirection.Right, 128)
    basic.pause(500)
    zoombit.brake()
    rekabit.setServoPosition(ServoChannel.S1, 90)
})
function obstacle_avoidance () {
    distance = zoombit.readUltrasonic()
    if (distance < 10) {
        zoombit.move(MotorDirection.Backward, 128)
    } else if (distance < 20) {
        zoombit.brake()
    } else {
        zoombit.move(MotorDirection.Forward, 128)
    }
}
input.onButtonPressed(Button.AB, function () {
    rekabit.setAllRgbPixelsColor(0x00ffff)
    zoombit.move(MotorDirection.Forward, 128)
    basic.pause(1000)
    zoombit.brake()
    rekabit.setAllRgbPixelsColor(0x000000)
})
input.onButtonPressed(Button.B, function () {
    rekabit.setServoPosition(ServoChannel.S1, 135)
    for (let index = 0; index < 4; index++) {
        rekabit.setRgbPixelColor(1, 0xff8000)
        basic.pause(100)
        rekabit.setRgbPixelColor(1, 0x000000)
        basic.pause(100)
    }
    zoombit.turn(TurnDirection.Left, 128)
    basic.pause(500)
    zoombit.brake()
    rekabit.setServoPosition(ServoChannel.S1, 90)
})
input.onLogoEvent(TouchButtonEvent.Pressed, function () {
    mode += 1
    zoombit.brake()
    if (mode == 1) {
        basic.showIcon(IconNames.Heart)
    } else if (mode == 2) {
        basic.showIcon(IconNames.Square)
    } else {
        basic.showLeds(`
            . . . . .
            . # # # .
            # # # # #
            # # # # #
            . # . # .
            `)
        mode = 0
    }
})
function line_following () {
    if (zoombit.isLineDetectedOn(LinePosition.Center)) {
        zoombit.move(MotorDirection.Forward, 128)
    } else if (zoombit.isLineDetectedOn(LinePosition.Left1)) {
        zoombit.setMotorsSpeed(50, 100)
        position = 1
    } else if (zoombit.isLineDetectedOn(LinePosition.Right1)) {
        zoombit.setMotorsSpeed(100, 50)
        position = 2
    } else if (zoombit.isLineDetectedOn(LinePosition.Left2)) {
        zoombit.setMotorsSpeed(0, 100)
        position = 1
    } else if (zoombit.isLineDetectedOn(LinePosition.Right2)) {
        zoombit.setMotorsSpeed(100, 0)
        position = 2
    } else if (zoombit.isLineDetectedOn(LinePosition.None)) {
        // Check 'position' variable to determine where were the robot's last position before it's away from the line. Then turn the robot to move back to the line.
        if (position == 1) {
            zoombit.turn(TurnDirection.Left, 80)
        } else if (position == 2) {
            zoombit.turn(TurnDirection.Right, 80)
        }
    }
}
let position = 0
let distance = 0
let mode = 0
music.playSoundEffect(music.builtinSoundEffect(soundExpression.giggle), SoundExpressionPlayMode.UntilDone)
basic.showIcon(IconNames.Happy)
zoombit.setHeadlight(HeadlightChannel.All, zoombit.digitalStatePicker(DigitalIoState.On))
rekabit.setServoPosition(ServoChannel.S1, 90)
mode = 0
basic.forever(function () {
    if (mode == 1) {
        obstacle_avoidance()
    } else if (mode == 2) {
        line_following()
    }
})
