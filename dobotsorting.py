#!/usr/bin/python3
import threading
import DobotDllType as dType
import sys, getopt

#"INITIALIZE(api,speed) - initializes all the variables that we'll use in this program"
def INITIALIZE(api, speed):
  global HOME_X, HOME_Y, HOME_Z, Place_X_blue, Place_Y_blue, Place_Z_blue, Place_X_green, Place_Y_green, Place_Z_green,\
    Place_X_red,Place_Y_red, Place_Z_red, Grab_X_L, Grab_Y_L, Grab_Z_L,Grab_X_R, Grab_Y_R, Grab_Z_R, ColorSensor_X,\
    ColorSensor_Y, ColorSensor_Z, RedCount, BlueCount, GreenCount

  HOME_X = 211.5673
  HOME_Y = -0.0002
  HOME_Z = 134.9425
  Place_X_blue = 176.0326
  Place_Y_blue = 198.7422
  Place_Z_blue = -36.9851
  Place_X_green = 200.6262
  Place_Y_green = -100.4792
  Place_Z_green = -36.5469
  Place_X_red = 200.6262
  Place_Y_red = -100.4792
  Place_Z_red = -36.5469
  Grab_X_L= 269.3878
  Grab_Y_L= 140.2518
  Grab_Z_L= 14.1758
  #we cant control left conveyor belt still
  Grab_X_R= 262.6895 #test
  Grab_Y_R= 140.4677 #test
  Grab_Z_R= 15.9159  #test
  #color sensor = JeVois camera
  #ColorSensor_X = 154.369
  #ColorSensor_Y = -115.7922
  #ColorSensor_Z = 27.9397
  dType.SetEndEffectorParamsEx(api, 59.7, 0, 0, 1)
  RedCount = 0
  BlueCount = 0
  GreenCount = 0
  #dType.SetColorSensor(api, 1 ,1, 0)
  dType.SetInfraredSensor(api, 1 ,1, 0)
  #can change each joints speed at command
  dType.SetPTPJointParamsEx(api,speed,speed,speed,speed,speed,speed,speed,speed,1)
  dType.SetPTPCommonParamsEx(api,100,100,1)
  dType.SetPTPJumpParamsEx(api,50,100,1)

#"getcoler(api) - Starts the color sensor and sets its parameters. It recognises the color of the cube and counts how many of each color we scanned "

def getcoler(api):
  global ColorSensor_X, ColorSensor_Y, ColorSensor_Z, R, G, B, MAX, Place_X_red, Place_Y_red, Place_Z_red, RedCount, GreenCount, Place_X_blue, Place_Y_blue, Place_Z_blue, BlueCount
  #dType.SetPTPCmdEx(api, 0, ColorSensor_X,  ColorSensor_Y,  ColorSensor_Z, 0, 1)
  #dType.SetWAITCmdEx(api, 1000, 1)
  R = dType.GetColorSensorEx(api, 0)
  G = dType.GetColorSensorEx(api, 1)
  B = dType.GetColorSensorEx(api, 2)
  MAX = max([R, G, B])
  if MAX == R:
    print('Red')
    dType.SetPTPCmdEx(api, 0, Place_X_red,  Place_Y_red,  Place_Z_red, 0, 1)
    dType.SetEndEffectorSuctionCupEx(api, 0, 1)
    RedCount = RedCount + 1
  elif MAX == G:
    print('Green')
    dType.SetPTPCmdEx(api, 0, Place_X_green,  Place_Y_green,  Place_Z_green, 0, 1)
    dType.SetEndEffectorSuctionCupEx(api, 0, 1)
    GreenCount = GreenCount + 1
  else:
    print('Blue')
    dType.SetPTPCmdEx(api, 0, Place_X_blue,  Place_Y_blue,  Place_Z_blue, 0, 1)
    dType.SetEndEffectorSuctionCupEx(api, 0, 1)
    BlueCount = BlueCount + 1

"""Change position that the items will be placed left or right"""
"""def ChangePos(position):
  global Place_X_blue, Place_Y_blue, Place_Z_blue, Place_X_green, Place_Y_green, Place_Z_green, Place_X_red, Place_Y_red, Place_Z_red
  Place_X_blue = -93.4153
  Place_Y_blue = -291.1590
  Place_Z_blue = -38.5044
  Place_X_green = -117.9651
  Place_Y_green = -222.0522
  Place_Z_green = -37.1846
  Place_X_red = -2.5597
  Place_Y_red = -277.0012
  Place_Z_red = -28.8777"""

"""Runs the program with parameters(number of items, position to be placed , speed of robot arm). It connects with dobot
api calls initialize and every time an item reaches the infrared sensor the dobot reaches to get it, then it calls
getcoler and then places it at its position"""

def main(argv):
  #default values
  numberofitems = 3
  speed = 200
  position = 1
  """check default values
  print("number of items : ", numberofitems)
  print("position left or right (1/0): ", left)
  print("speed of robotic arm : " , speed)"""

  #maybe delete <position> because we will get it after Jevois scan
  try:
    opts, args = getopt.getopt(argv, "hn:p:s:", ["numberofitems=", "position=", "speed="])
  except getopt.GetoptError:
    print('dobotsorting.py -n <numberofitems> -p <position> -s <speed>')
    sys.exit(2)
  for opt, arg in opts:
    if opt == '-h':
      print('dobotsorting.py -n <numberofitems> -p <position> -s <speed>')
      #runs with default values
    elif opt in ("-n", "--numberofitems"):
      if (numberofitems < 10 and numberofitems > 0):
        numberofitems = int(arg)
    elif opt in ("-p", "--position"):
      if (position == 0 or position == 1):
        position = int(arg)
    elif opt in ("-s", "--speed"):
      if(speed < 321 and speed > 0):
        speed = int(arg)
  print('Number of items is ', numberofitems)
  #print('Items will be placed (0-left / 1-right) : ', position)
  print('Speed of joints : ', speed)

  CON_STR = {
    dType.DobotConnect.DobotConnect_NoError: "DobotConnect_NoError",
    dType.DobotConnect.DobotConnect_NotFound: "DobotConnect_NotFound",
    dType.DobotConnect.DobotConnect_Occupied: "DobotConnect_Occupied"}

  # Load Dll and get the CDLL object
  api = dType.load()
  # Connect Dobot
  state = dType.ConnectDobot(api, "COM4", 115200)[0]
  print("Connect status:", CON_STR[state])

  INITIALIZE(api, speed)
  if (position == 0):
    ChangePos(position)
  print('START')
  stop = 0
  while stop < numberofitems:
    #print(dType.GetInfraredSensor(api, 1)[0])
    if (dType.GetInfraredSensor(api, 1)[0]) == 0:
      dType.SetPTPCmdEx(api, 0, Grab_X_L,  Grab_Y_L,  Grab_Z_L, 0, 1)
      dType.SetEndEffectorSuctionCupEx(api, 1, 1)
      getcoler(api)
      stop = stop + 1
  print('RESULTS')
  print("Blue : ", BlueCount)
  print("Green : ", GreenCount)
  print("Red : ",RedCount)
  # go to home position after placing item
  #dType.SetPTPCmdEx(api, 0, HOME_X, HOME_Y, HOME_Z, 0, 1)

  #Disconnect Dobot
  dType.DisconnectDobot(api)

if __name__ == "__main__":
  main(sys.argv[1:])


