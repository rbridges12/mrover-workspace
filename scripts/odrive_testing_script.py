import odrive
from odrive.enums import AXIS_STATE_CLOSED_LOOP_CONTROL, CONTROL_MODE_VELOCITY_CONTROL, CONTROL_MODE_TORQUE_CONTROL, AXIS_STATE_FULL_CALIBRATION_SEQUENCE, AXIS_STATE_IDLE, ENCODER_MODE_HALL
from odrive.utils import dump_errors
import sys
import select
import fibre

id = "2051377D5753"
    
def drive():
    global test_motor
    test_motor.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
    num = input("Enter new setpoint: ")
    test_motor.controller.config.control_mode = CONTROL_MODE_TORQUE_CONTROL
    test_motor.controller.input_torque = num
    

def stop():
    global test_motor
    test_motor.controller.input_torque = 0
    test_motor.requested_state = AXIS_STATE_IDLE
    
def printInfo():
    global test_motor
    print(test_motor.encoder.vel_estimate)
    print(test_motor.motor.current_control.Iq_measured)

def main():
    global odrv
    global test_motor
    odrv = odrive.find_any(serial_number=id)
    print("found odrive")
    test_motor = odrv.axis1

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
            elif (value == 'p'):
                printInfo()

if __name__=="__main__":
    main()