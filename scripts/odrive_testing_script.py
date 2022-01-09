import odrive
from odrive.enums import AXIS_STATE_CLOSED_LOOP_CONTROL, CTRL_MODE_VELOCITY_CONTROL, CTRL_MODE_CURRENT_CONTROL, AXIS_STATE_FULL_CALIBRATION_SEQUENCE, AXIS_STATE_IDLE, ENCODER_MODE_HALL
from odrive.utils import dump_errors
import sys
import select
import fibre

id = "205F3883304E"
    
def drive():
    global test_motor
    test_motor.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
    num = input("Enter new setpoint: ")
    vel = input("Enter new velocity: ")
    test_motor.controller.config.control_mode = CTRL_MODE_VELOCITY_CONTROL
    test_motor.controller.vel_setpoint = vel
    test_motor.controller.config.control_mode = CTRL_MODE_CURRENT_CONTROL
    test_motor.controller.current_setpoint = num

def stop():
    global test_motor
    test_motor.controller.vel_setpoint = 0
    test_motor.controller.current_setpoint = 0
    test_motor.requested_state = AXIS_STATE_IDLE

def main():
    global odrv
    global test_motor
    odrv = odrive.find_any(serial_number=id)
    print("found odrive")
    test_motor = odrv.axis0

    # Calibrate first
    try:
        test_motor.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE
        test_motor.motor.config.pre_calibrated = True
        test_motor.encoder.config.pre_calibrated = True
        while(test_motor.requested_state != AXIS_STATE_IDLE):
            pass
        odrv.save_configuration()
        odrv.reboot()
    except fibre.protocol.ChannelBrokenException:
        odrv = odrive.find_any(serial_number=id)
        test_motor = odrv.axis0
        print("found odrive")
        pass

    while(1):
        cmd_input = select.select([sys.stdin], [], [], 1)[0]

        if cmd_input:
            value = sys.stdin.readline().rstrip()
            if (value == 'q'):
                stop()
                print("stopped")
                break
            elif (value == 'd'):
                drive()
                print("driving")
            else:
                print("unknown input")

if __name__=="__main__":
    main()