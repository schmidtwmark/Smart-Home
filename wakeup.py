from lifxlan import LifxLAN
import time
import math
import os

def check_flag():
  return os.path.isfile("/home/pi/.homebridge/scripts/wakeup_key")

def main():
  lifx = LifxLAN(2)

  print("Discovering lights")
  original_powers = lifx.get_power_all_lights()
  print("Discovered lights")

  flag = check_flag()
  if not flag:
    print("Exiting, flag is off")
    return

  for bulb in original_powers:
    power = original_powers[bulb]
    flag &= power == 0 

  if not flag:
    print("Exiting, some bulb is on")
    return

  total_time = 60 #seconds
  periods = 60
  
  step = 65535 / periods
  #make the lights dim
  print("Setting up lights")

  setup = False
  count = 1
  while not setup and count < 20:
    try:
      for bulb in original_powers:
        bulb.set_brightness(0)
        bulb.set_saturation(0)
        bulb.set_hue(0)
        bulb.set_colortemp(3500)
        time.sleep(1)
        bulb.set_power(1)
        setup = True
    except Exception as e:
      print(str(e))
      print("Failed setting up lights {} time(s)".format(count))
      count += 1
      time.sleep(1)


  for i in range(periods):
    if check_flag(): 
      for bulb in original_powers:
        bulb.set_brightness(i * step, rapid=True)
      print("Set lights to: {}".format(i * step))
      time.sleep(total_time/periods)
    else:
      print("Exiting, flag turned off mid-run")
      return

  print("Success!")

if __name__=="__main__":
  main()
