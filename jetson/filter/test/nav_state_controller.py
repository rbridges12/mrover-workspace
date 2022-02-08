from pynput import keyboard
import lcm
from rover_msgs import NavStatus


def send_nav_state(lc, state_name):
    nav_struct = NavStatus()
    nav_struct.nav_state_name = state_name

    # these aren't used by the filter so just make them 0
    nav_struct.completed_wps = 0
    nav_struct.total_wps = 0

    lc.publish("/nav_status", nav_struct.encode())

def on_press(key):
    # use nav state "Off" to stop the filter
    try:
        if key.char == 's':
            send_nav_state(lc, "Off")
            print("sent nav state \"Off\"")

        # use nav state "Drive" to run the filter
        elif key.char == 'd':
            send_nav_state(lc, "Drive")
            print("sent nav state \"Drive\"")
            
        elif key == keyboard.key.esc:
            # keyboard.listener.stop()
            return False 

    except AttributeError:
        pass
    

"""
Simulates the nav state changing between "Off" state and "Drive" state
in order to stop the filter while running it independently.
Press 's' when you stop moving, press 'd' when you start moving.
"""
if __name__ == "__main__":

    # init LCM
    # lc = aiolcm.AsyncLCM()
    lc = lcm.LCM()

    # key listener loop
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

        
            
