from xbox import xbox_read

""" 
Returns 2+2 bytes representing left and right values for the motor
Scaled to -256 to 255 for arduino servo use

`deadzone`: int=3000, threshold for controller drift
"""
def getByteState(deadzone=3000):
    state = xbox_read.get_controller_state()
    fbvalue = int(state['sThumbLY'])
    lrvalue = int(state['sThumbLX'])

    # print(f"fbval: {fbvalue}, lrval: {lrvalue}")
    if abs(fbvalue) < deadzone:
        fbvalue = 0
    if abs(lrvalue) < deadzone:
        lrvalue = 0

    # need to add actually correct scaling of the values here, this is just a placeholder
    lv = fbvalue + lrvalue
    lv = max(min(lv, 32767), -32768)
    rv = fbvalue - lrvalue
    rv = max(min(rv, 32767), -32768)

    def scale(val, in_min, in_max, out_min, out_max):
        scaled = (val - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
        return int(max(min(round(scaled), out_max), out_min))

    # scale to arduino servo pwm values
    lv = scale(lv, -32768, 32767, -255, 255)
    rv = scale(rv, -32768, 32767, -255, 255)
    print(f"lv: {lv}, rv: {rv}")
    tosend = (lv.to_bytes(2, 'big', signed=True)
          + rv.to_bytes(2, 'big', signed=True))

    return tosend

def get_controller_values(deadzone=3000):
    state = xbox_read.get_controller_state()
    # RY = int(state['sThumbRY'])
    # RY = RY if abs(RY) >= deadzone else 0
    # RX = int(state['sThumbRX'])
    # RY = RX if abs(RX) >= deadzone else 0


    # return [int(state['sThumbLY']), int(state['sThumbLX']), int(state['sThumbRY']), int(state['sThumbRX'])]
    # return [0,1,2,3]
    return state