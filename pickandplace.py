#!/usr/bin/python3
#import threading
import DobotDllType as dType
import sys, getopt

#"INITIALIZE(api,speed) - initializes all the variables that we'll use in this program"
def INITIALIZE(api, speed):
  global distance, HOME_X, HOME_Y, HOME_Z, Place_X, Place_Y, Place_Z, Place_2X, Place_2Y, Place_2Z, Grab_X, Grab_Y,\
    Grab_Z,Grab_X1, Grab_Y1, Grab_Z1,Grab_X2, Grab_Y2, Grab_Z2,Grab_X3, Grab_Y3, Grab_Z3

  #Starting cube positions
  Grab_X = 227.4745
  Grab_Y = -22.2450
  Grab_Z = -41.6532
  Grab_X1 = 226.8879
  Grab_Y1 = 15.3274
  Grab_Z1 = -40.4631
  Grab_X2 = 274.5497
  Grab_Y2 = -20.4591
  Grab_Z2 = -41.0564
  Grab_X3 = 274.7646
  Grab_Y3 = 18.0517
  Grab_Z3 = -40.9781


  """Place 1(left) side"""
  Place_X = 65.1753
  Place_Y = 259.3055
  Place_Z = 16.1066

  """Place 2(right) side"""
  Place_2X = 53.8462
  Place_2Y = -257.0213
  Place_2Z = 13.4654

  HOME_X = 259.0965
  HOME_Y = 0.0002
  HOME_Z = -8.4781
  #dType.SetEndEffectorParamsEx(api, 59.7, 0, 0, 1)
  dType.SetPTPJointParamsEx(api,speed,speed,speed,speed,speed,speed,speed,speed,1)
  #dType.SetPTPCommonParamsEx(api,100,100,1)
  #dType.SetPTPJumpParamsEx(api,40,100,1)
  #dType.SetEndEffectorSuctionCupEx(api, 1, 1)
  STEP_PER_CRICLE = 360.0 / 1.8 * 10.0 * 16.0
  MM_PER_CRICLE = 3.1415926535898 * 36.0
  vel = float(0) * STEP_PER_CRICLE / MM_PER_CRICLE
  dType.SetEMotorEx(api, 0, 0, int(vel), 1)
  distance = 5


def main(argv):
  #default values
  numberofitems = 3
  speed = 200
  distance = 5
  """check default values
  print("number of items : ", numberofitems)
  print("speed of robotic arm : " , speed)"""

  try:
    opts, args = getopt.getopt(argv, "hn:s:d:", ["numberofitems=", "speed=", "distance="])
  except getopt.GetoptError:
    print('dobotsorting.py -n <numberofitems> -s <speed> -d <distance>')
    sys.exit(2)
  for opt, arg in opts:
    if opt == '-h':
      print('dobotsorting.py -n <numberofitems> -s <speed>')
      #runs with default values
    elif opt in ("-n", "--numberofitems"):
      numberofitems = int(arg)
      if(numberofitems > 10 or numberofitems < 0):
        numberofitems = 3
    elif opt in ("-s", "--speed"):
      speed = int(arg)
      if(speed > 321 or speed < 0):
        speed = 200
    elif opt in ("-d", "--distance"):
      distance = int(arg)
      if(distance > 5 or distance < 0):
        distance = 4.5
  print('Number of items is ', numberofitems)
  print('Speed of joints : ', speed)
  print('Distance of conveyot belt : ', distance)

  CON_STR = {
    dType.DobotConnect.DobotConnect_NoError: "DobotConnect_NoError",
    dType.DobotConnect.DobotConnect_NotFound: "DobotConnect_NotFound",
    dType.DobotConnect.DobotConnect_Occupied: "DobotConnect_Occupied"}

  # Load Dll and get the CDLL object
  api = dType.load()
  # Connect Dobot
  state = dType.ConnectDobot(api, "COM3", 115200)[0]
  print("Connect status:", CON_STR[state])
  INITIALIZE(api, speed)
  print('START')
  stop = 0
  side = True
  i = 0 #for which cube to pick up
  while stop < numberofitems:
      stop = stop + 1
      if (i == 0):
        dType.SetPTPCmdEx(api, 0, Grab_X, Grab_Y, Grab_Z, 0, 1)
      elif (i == 1):
        dType.SetPTPCmdEx(api, 0, Grab_X1, Grab_Y1, Grab_Z1, 0, 1)
      elif (i == 2):
        dType.SetPTPCmdEx(api, 0, Grab_X2, Grab_Y2, Grab_Z2, 0, 1)
      elif (i == 3):
        dType.SetPTPCmdEx(api, 0, Grab_X3, Grab_Y3, Grab_Z3, 0, 1)

      i = i + 1
      dType.SetEndEffectorSuctionCupEx(api, 1, 1)

      if(side):
        dType.SetPTPCmdEx(api, 0, Place_2X, Place_2Y, Place_2Z, 0, 1)
      else:
        dType.SetPTPCmdEx(api, 0, Place_X, Place_Y, Place_Z, 0, 1)

      side = not side #changes side to put one left one right each time
      dType.SetEndEffectorSuctionCupEx(api, 0, 1)

      #go to home position after placing item
      dType.SetPTPCmdEx(api, 0, HOME_X, HOME_Y, HOME_Z, 0, 1)
      time_start = dType.gettime()[0]
      STEP_PER_CRICLE = 360.0 / 1.8 * 10.0 * 16.0
      MM_PER_CRICLE = 3.1415926535898 * 36.0
      vel = float(50) * STEP_PER_CRICLE / MM_PER_CRICLE
      dType.SetEMotorEx(api, 0, 1, int(vel), 1)
      while True:
        #velocity of conveyor belt
        if (dType.gettime()[0]) - time_start >= distance:
          STEP_PER_CRICLE = 360.0 / 1.8 * 10.0 * 16.0
          MM_PER_CRICLE = 3.1415926535898 * 36.0
          vel = float(0) * STEP_PER_CRICLE / MM_PER_CRICLE
          dType.SetEMotorEx(api, 0, 0, int(vel), 1)
          break

  #Disconnect Dobot
  dType.DisconnectDobot(api)

if __name__ == "__main__":
  main(sys.argv[1:])
