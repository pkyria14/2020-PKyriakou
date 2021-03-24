#!/usr/bin/python3
#import threading
import DobotDllTypeX as dType
import sys, getopt
import serial
import time

serdev = 'COM5:'  # serial device of JeVois
#serdev2 = 'COM6:'  # serial device of Raspberrypi

# JEVOIS CAMERA

def objectFound():
    with serial.Serial(serdev, 115200, timeout=1) as ser:
        while 1:
            # Read a whole line and strip any trailing line ending character:
            line = ser.readline().rstrip()
            print("received: {}".format(line))
            # Split the line into tokens:
            tok = line.split()
            # Skip if timeout or malformed line:
            if len(tok) < 1:
                print("len(tok) < 1")
                continue
            # Skip if not a standardized "Normal 2D" message:
            # See http://jevois.org/doc/UserSerialStyle.html
            if tok[0].decode('utf-8') != 'N2':
                print("tok[0] != N2")
                continue
            # From now on, we hence expect: N2 id x y w h
            if len(tok) != 6:
                print("length !=6")
                continue
            # Assign some named Python variables to the tokens:
            key, id, x, y, w, h = tok
            id = (id.decode('utf-8'))
            #print(id)
            return id


#"INITIALIZE(api,speed) - initializes all the variables that we'll use in this program"
def INITIALIZE_PickandPlace(api, speed):
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
  #dType.SetEMotorEx(api, 0, 0, int(vel), 1)
  distance = 5

# "INITIALIZE(api,speed) - initializes all the variables that we'll use in this program"
def INITIALIZE_Sorting(api, speed):
    global HOME_X, HOME_Y, HOME_Z, Place_X_blue, Place_Y_blue, Place_Z_blue, Place_X_green, Place_Y_green, Place_Z_green, \
        Place_X_red, Place_Y_red, Place_Z_red, Grab_X_L, Grab_Y_L, Grab_Z_L, Grab_X_R, Grab_Y_R, Grab_Z_R, ColorSensor_X, \
        ColorSensor_Y, ColorSensor_Z, RedCount, BlueCount, GreenCount

    HOME_X = 211.5673
    HOME_Y = -0.0002
    HOME_Z = 134.9425
    Place_X_blue = 223.1086
    Place_Y_blue = -115.1117
    Place_Z_blue = -34.4796

    Place_X_green = 200.6262
    Place_Y_green = -100.4792
    Place_Z_green = -36.5469
    Place_X_red = 200.6262
    Place_Y_red = -100.4792
    Place_Z_red = -36.5469

    Grab_X_L = 268.7171
    Grab_Y_L = 149.0243
    Grab_Z_L = 16.7649

    # we cant control left conveyor belt still
    Grab_X_R = 7.4956  # test
    Grab_Y_R = -300.3943  # test
    Grab_Z_R = 16.0973  # test
    # color sensor = JeVois camera
    # ColorSensor_X = 154.369
    # ColorSensor_Y = -115.7922
    # ColorSensor_Z = 27.9397
    #dType.SetEndEffectorParamsEx(api, 59.7, 0, 0, 1)
    RedCount = 0
    BlueCount = 0
    GreenCount = 0
    # dType.SetColorSensor(api, 1 ,1, 0)
    # dType.SetInfraredSensor(api, 1, 1, 0)
    # can change each joints speed at command
    #dType.SetPTPJointParamsEx(api, speed, speed, speed, speed, speed, speed, speed, speed, 1)
    #dType.SetPTPCommonParamsEx(api, 100, 100, 1)
    #dType.SetPTPJumpParamsEx(api, 50, 100, 1)

# "getcoler(api) - Starts the color sensor and sets its parameters. It recognises the color of the cube and counts how many of each color we scanned "
def getcoler(api):
    global ColorSensor_X, ColorSensor_Y, ColorSensor_Z, R, G, B, MAX, Place_X_red, Place_Y_red, Place_Z_red, RedCount, GreenCount, Place_X_blue, Place_Y_blue, Place_Z_blue, BlueCount
    # dType.SetPTPCmdEx(api, 0, ColorSensor_X,  ColorSensor_Y,  ColorSensor_Z, 0, 1)
    # dType.SetWAITCmdEx(api, 1000, 1)
    R = dType.GetColorSensorEx(api, 0)
    G = dType.GetColorSensorEx(api, 1)
    B = dType.GetColorSensorEx(api, 2)
    MAX = max([R, G, B])
    if MAX == R:
        print('Red')
        dType.SetPTPCmdEx(api, 0, Place_X_red, Place_Y_red, Place_Z_red, 0, 1)
        dType.SetEndEffectorSuctionCupEx(api, 0, 1)
        RedCount = RedCount + 1
    elif MAX == G:
        print('Green')
        dType.SetPTPCmdEx(api, 0, Place_X_green, Place_Y_green, Place_Z_green, 0, 1)
        dType.SetEndEffectorSuctionCupEx(api, 0, 1)
        GreenCount = GreenCount + 1
    else:
        print('Blue')
        dType.SetPTPCmdEx(api, 0, Place_X_blue, Place_Y_blue, Place_Z_blue, 0, 1)
        dType.SetEndEffectorSuctionCupEx(api, 0, 1)
        BlueCount = BlueCount + 1

"""Change position that the items will be placed left or right"""
def ChangePos(placement):
  global Place_X_blue, Place_Y_blue, Place_Z_blue, Place_X_green, Place_Y_green, Place_Z_green, Place_X_red, Place_Y_red, Place_Z_red
  #pos 0
  Place_X_blue = 223.1086
  Place_Y_blue = -115.1117
  Place_Z_blue = -34.4796

  Place_X_green = -117.9651
  Place_Y_green = -222.0522
  Place_Z_green = -37.1846

  Place_X_red = 223.1086
  Place_Y_red = -115.1117
  Place_Z_red = -34.4796
  #pos 1

  

"""Runs the program with parameters(number of items, position to be placed , speed of robot arm). It connects with dobot
api calls initialize and every time an item reaches the infrared sensor the dobot reaches to get it, then it calls
getcoler and then places it at its position"""
def Sorting(numberofitems,speed,objectid,dobot0,dobot1):
    placement = "left"
    INITIALIZE_Sorting(dobot0, speed)
    print('START')
    stop = 0
    while stop < numberofitems:
        if (placement == "left"):
            placement = "right"
            stop = stop + 1
            #ChangePos(placement)
            # Grap from left
            dType.SetPTPCmdEx(dobot0, 0, Grab_X_L, Grab_Y_L, Grab_Z_L, 0, 1)
            dType.SetEndEffectorSuctionCupEx(dobot0, 1, 1)
        else:
            placement = "left"
            #ChangePos(placement)
            stop = stop + 1
            #Grap from right
            dType.SetPTPCmdEx(dobot0, 0, Grab_X_R, Grab_Y_R, Grab_Z_R, 0, 1)
            dType.SetEndEffectorSuctionCupEx(dobot0, 1, 1)
        if (objectid == "cube.png"):
            dType.SetPTPCmdEx(dobot0, 0, Place_X_blue, Place_Y_blue, Place_Z_blue, 0, 1)
        else:
            dType.SetPTPCmdEx(dobot0, 0, Place_X_red, Place_Y_red, Place_Z_red, 0, 1)
        dType.SetEndEffectorSuctionCupEx(dobot0, 0, 1)

    # go to home position after placing item
    dType.SetPTPCmdEx(dobot0, 0, HOME_X, HOME_Y, HOME_Z, 0, 1)
    #dType.SetPTPCmdEx(dobot1, 0, Place_2X, Place_2Y, Place_2Z, 0, 1)

def PickandPlace(numberofitems,speed,distance,dobot0,dobot1):

  """check default values
  print("number of items : ", numberofitems)
  print("speed of robotic arm : " , speed)"""

  print('Number of items is ', numberofitems)
  print('Speed of joints : ', speed)
  print('Distance of conveyot belt : ', distance)

  #print("Connect status:", CON_STR[state])
  INITIALIZE_PickandPlace(dobot1, speed)
  print('START')
  stop = 0
  side = True
  belt = 0
  i = 0 #for which cube to pick up
  while stop < numberofitems:
      stop = stop + 1
      if (i == 0):
        dType.SetPTPCmdEx(dobot1, 0, Grab_X, Grab_Y, Grab_Z, 0, 1)
      elif (i == 1):
        dType.SetPTPCmdEx(dobot1, 0, Grab_X1, Grab_Y1, Grab_Z1, 0, 1)
      elif (i == 2):
        dType.SetPTPCmdEx(dobot1, 0, Grab_X2, Grab_Y2, Grab_Z2, 0, 1)
      elif (i == 3):
        dType.SetPTPCmdEx(dobot1, 0, Grab_X3, Grab_Y3, Grab_Z3, 0, 1)

      i = i + 1
      dType.SetEndEffectorSuctionCupEx(dobot1, 1, 1)

      if(side):
        dType.SetPTPCmdEx(dobot1, 0, Place_2X, Place_2Y, Place_2Z, 0, 1)
      else:
        dType.SetPTPCmdEx(dobot1, 0, Place_X, Place_Y, Place_Z, 0, 1)
      dType.SetEndEffectorSuctionCupEx(dobot1, 0, 1)
      side = not side  # changes side to put one left one right each time

      #go to home position after placing item
      dType.SetPTPCmdEx(dobot1, 0, HOME_X, HOME_Y, HOME_Z, 0, 1)

      # belt0 = right belt1 = left

      if (belt == 0):
          time_start = dType.gettime()[0]
          STEP_PER_CRICLE = 360.0 / 1.8 * 10.0 * 16.0
          MM_PER_CRICLE = 3.1415926535898 * 36.0
          vel = float(50) * STEP_PER_CRICLE / MM_PER_CRICLE
          dType.SetEMotorEx(dobot1, 0, 1, int(vel), 1)
          while True:
              # velocity of conveyor belt
              if (dType.gettime()[0]) - time_start >= distance:
                  STEP_PER_CRICLE = 360.0 / 1.8 * 10.0 * 16.0
                  MM_PER_CRICLE = 3.1415926535898 * 36.0
                  vel = float(0) * STEP_PER_CRICLE / MM_PER_CRICLE
                  dType.SetEMotorEx(dobot1, 0, 0, int(vel), 1)
                  belt = belt + 1
                  break
      else :
            time_start = dType.gettime()[0]
            STEP_PER_CRICLE = 360.0 / 1.8 * 10.0 * 16.0
            MM_PER_CRICLE = 3.1415926535898 * 36.0
            vel = float(50) * STEP_PER_CRICLE / MM_PER_CRICLE
            dType.SetEMotorEx(dobot0, 0, 1, int(vel), 1)
            while True:
                # velocity of conveyor belt
                if (dType.gettime()[0]) - time_start >= distance:
                    STEP_PER_CRICLE = 360.0 / 1.8 * 10.0 * 16.0
                    MM_PER_CRICLE = 3.1415926535898 * 36.0
                    vel = float(0) * STEP_PER_CRICLE / MM_PER_CRICLE
                    dType.SetEMotorEx(dobot0, 0, 0, int(vel), 1)
                    belt = belt - 1
                    break

def main(argv):

    # default values
    numberofitems = 3
    speed = 300
    distance = 5
    """check default values
      print("number of items : ", numberofitems)
      print("speed of robotic arm : " , speed)
      print("distance the item will travel on conveyor belt : ", distance)"""

    try:
        opts, args = getopt.getopt(argv, "hn:p:s:", ["numberofitems=", "speed="])
    except getopt.GetoptError:
        print('control.py -n <numberofitems> -s <speed>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('control.py -n <numberofitems> -s <speed>')
            # runs with default values
        elif opt in ("-n", "--numberofitems"):
            if (numberofitems < 10 and numberofitems > 0):
                numberofitems = int(arg)
        elif opt in ("-d", "--distance"):
            distance = int(arg)
            if (distance > 5 or distance < 0):
                distance = 4.5
        elif opt in ("-s", "--speed"):
            if (speed < 321 and speed > 0):
                speed = int(arg)
    print('Number of items is ', numberofitems)
    print('Speed of joints : ', speed)

    CON_STR = {
        dType.DobotConnect.DobotConnect_NoError: "DobotConnect_NoError",
        dType.DobotConnect.DobotConnect_NotFound: "DobotConnect_NotFound",
        dType.DobotConnect.DobotConnect_Occupied: "DobotConnect_Occupied"}

    # Load Dll and get the CDLL object
    dobot0, state1 = dType.ConnectDobotX("COM3")
    dobot1, state2 = dType.ConnectDobotX("COM6")

    #print(dType.ConnectDobotX("COM3"))
    #print(dType.ConnectDobotX("COM6"))
    # Connect Dobot
    print("Connect status1:", CON_STR[state1[0]])
    print("Connect status2:", CON_STR[state2[0]])

    PickandPlace(numberofitems,speed,distance,dobot0,dobot1)

    # Identify object with JeVois Camera
    objectid = objectFound()
    #objectid = cube2.png
    print("object id : ", objectid)

    Sorting(numberofitems, speed, objectid, dobot0, dobot1)

    # Disconnect All Dobots
    dType.DisconnectAll()



if __name__ == "__main__":
  main(sys.argv[1:])
