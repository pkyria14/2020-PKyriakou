#!/usr/bin/python3
import DobotDllTypeX as dType
import sys, getopt
import serial
import time
from threading import Thread
from datetime import datetime


serdev = 'COM13'  # serial device of JeVois 1
serdev2 = 'COM17'  # serial device of Jevois 2

# JEVOIS CAMERA

def objectFound(serdev):
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


# "INITIALIZE(api,speed) - initializes all the variables that we'll use in this program"
def INITIALIZE_PickandPlace(api, speed):
    global distance, HOME_X, HOME_Y, HOME_Z, Place_X, Place_Y, Place_Z, Place_2X, Place_2Y, Place_2Z, Grab_X, Grab_Y, \
        Grab_Z, Grab_X1, Grab_Y1, Grab_Z1, Grab_X2, Grab_Y2, Grab_Z2, Grab_X3, Grab_Y3, Grab_Z3


    # Starting cube positions
    Grab_X = 301.6891
    Grab_Y = -23.6030
    Grab_Z = -40.8829

    Grab_X1 = 297.7000
    Grab_Y1 = 11.0082
    Grab_Z1 = -41.9901

    Grab_X2 = 259.3505
    Grab_Y2 = -23.0657
    Grab_Z2 = -42.1087

    Grab_X3 = 255.3329
    Grab_Y3 = 9.2053
    Grab_Z3 = -40.9706

    """Place 1(left) side"""
    Place_X = 62.7516
    Place_Y = 272.4461
    Place_Z = 15.7109

    """Place 2(right) side"""
    Place_2X = 79.3523
    Place_2Y = -267.1327
    Place_2Z = 12.8948

    HOME_X = 259.0965
    HOME_Y = 0.0002
    HOME_Z = -8.4781
    # dType.SetEndEffectorParamsEx(api, 59.7, 0, 0, 1)
    dType.SetPTPJointParamsEx(api, speed, speed, speed, speed, speed, speed, speed, speed, 1)


# "INITIALIZE(api,speed) - initializes all the variables that we'll use in this program"
def INITIALIZE_Sorting(api, speed):
    global HOME_X, HOME_Y, HOME_Z, Place_X_cube, Place_Y_cube, Place_Z_cube, \
        Place_X_else, Place_Y_else, Place_Z_else, Grab_X_L, Grab_Y_L, Grab_Z_L, Grab_X_R, Grab_Y_R, Grab_Z_R, ColorSensor_X, \
        ColorSensor_Y, ColorSensor_Z, RedCount, BlueCount, GreenCount

    HOME_X = 254.9184
    HOME_Y = -109.7544
    HOME_Z = 15.6738

    Place_X_cube = 214.1724
    Place_Y_cube = -101.1449
    Place_Z_cube = -39.8442

    Place_X_else = 187.0654
    Place_Y_else = -155.9223
    Place_Z_else = -39.5752

    # grap left
    Grab_X_L = 188.3358
    Grab_Y_L = 201.8613
    Grab_Z_L = 15.5308

    Grab_X_R = -40.3719
    Grab_Y_R = -289.4148
    Grab_Z_R = 14.8599


    RedCount = 0
    BlueCount = 0
    GreenCount = 0



# "getcoler(api) - Starts the color sensor and sets its parameters. It recognises the color of the cube and counts how many of each color we scanned "
"""
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
"""
"""Change position that the items will be placed left or right
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
"""

"""Runs the program with parameters(number of items, position to be placed , speed of robot arm). It connects with dobot
api calls initialize and every time an item reaches the infrared sensor the dobot reaches to get it, then it calls
getcoler and then places it at its position"""


def Sorting(numberofitems, speed, objectid, objectid2, dobot0, dobot1):
    placement = "right"
    INITIALIZE_Sorting(dobot0, speed)
    print('START SORTING')
    stop = 0
    while stop < 2:
        if (placement == "left"):
            placement = "right"
            # Grap from left
            dType.SetPTPCmdEx(dobot0, 0, Grab_X_L, Grab_Y_L, Grab_Z_L, 0, 1)
            dType.SetEndEffectorSuctionCupEx(dobot0, 1, 1)
        else:
            placement = "left"
            # ChangePos(placement)

            # Grap from right
            dType.SetPTPCmdEx(dobot0, 0, Grab_X_R, Grab_Y_R, Grab_Z_R, 0, 1)
            dType.SetEndEffectorSuctionCupEx(dobot0, 1, 1)
        if (stop == 0 and objectid == "cube.png"):
            print("FIRST ITEM IS CUBE! ", objectid , "stop: ", stop)
            dType.SetPTPCmdEx(dobot0, 0, Place_X_cube, Place_Y_cube, Place_Z_cube, 0, 1)
        elif(stop == 0 and objectid == "notcube.png"):
             print("FIRST ITEM IS NOT CUBE! ",objectid, "stop: ", stop)
             dType.SetPTPCmdEx(dobot0, 0, Place_X_else, Place_Y_else, Place_Z_else, 0, 1)
        elif(stop == 1 and objectid2 == "cube.png"):
            print("SECOND ITEM IS CUBE! ", objectid2, "stop: ", stop)
            dType.SetPTPCmdEx(dobot0, 0, Place_X_cube, Place_Y_cube, Place_Z_cube, 0, 1)
        else:
            print("SECOND ITEM IS NOT CUBE! ", objectid2 , "stop: ", stop)
            dType.SetPTPCmdEx(dobot0, 0, Place_X_else, Place_Y_else, Place_Z_else, 0, 1)
        stop = stop + 1 
        dType.SetEndEffectorSuctionCupEx(dobot0, 0, 1)

    # go to home position after placing item
    dType.SetPTPCmdEx(dobot0, 0, HOME_X, HOME_Y, HOME_Z, 0, 1)
    # dType.SetPTPCmdEx(dobot1, 0, Place_2X, Place_2Y, Place_2Z, 0, 1)

def items_job(dobot1,i,side,):
    print("items_job")

    if (i == 0):
        dType.SetPTPCmdEx(dobot1, 0, Grab_X, Grab_Y, Grab_Z, 0, 1)
    elif (i == 1):
        dType.SetPTPCmdEx(dobot1, 0, Grab_X1, Grab_Y1, Grab_Z1, 0, 1)
    elif (i == 2):
        dType.SetPTPCmdEx(dobot1, 0, Grab_X2, Grab_Y2, Grab_Z2, 0, 1)
    elif (i == 3):
        dType.SetPTPCmdEx(dobot1, 0, Grab_X3, Grab_Y3, Grab_Z3, 0, 1)
    else:
        dType.SetPTPCmdEx(dobot1, 0, Grab_X, Grab_Y, Grab_Z, 0, 1)

    i = i + 1
    dType.SetEndEffectorSuctionCupEx(dobot1, 1, 1)
    if (side):
        dType.SetPTPCmdEx(dobot1, 0, Place_2X, Place_2Y, Place_2Z, 0, 1)
    else:
        dType.SetPTPCmdEx(dobot1, 0, Place_X, Place_Y, Place_Z, 0, 1)
    dType.SetEndEffectorSuctionCupEx(dobot1, 0, 1)
    side = not side  # changes side to put one left one right each time

    # go to home position after placing item
    dType.SetPTPCmdEx(dobot1, 0, HOME_X, HOME_Y, HOME_Z, 0, 1)

def belt_job(belt,distance,dobot0,dobot1,):
    print("Belt_job")
    # belt0 = right belt1 = left
    # conveyor belt default velocity = 14147
    STEP_PER_CRICLE = 360.0 / 1.8 * 10.0 * 16.0
    MM_PER_CRICLE = 3.1415926535898 * 36.0
    vel = (float(50) * STEP_PER_CRICLE / MM_PER_CRICLE)


    if (belt % 2 == 0):
        Thread(target=dType.SetEMotorSEx, args=(dobot1, 0, 1, int(vel), distance * 10000, 1,)).start()
        belt = belt + 1 #change belt
    else:
        Thread(target=dType.SetEMotorSEx, args=(dobot0, 0, 1, int(vel), distance * 10000, 1,)).start()
        belt = belt - 1 #change belt


def PickandPlace(numberofitems, speed, distance, dobot0, dobot1):
    """check default values"""

    print('Number of items is ', numberofitems)
    print('Speed of joints : ', speed)
    print('Distance of conveyot belt : ', distance)

    # print("Connect status:", CON_STR[state])
    INITIALIZE_PickandPlace(dobot1, speed)
    print('START PICK&PLACE')
    stop = 0
    exectime = 0 # for time metrics
    side = False
    belt = 1
    i = 0  # for which cube to pick up

    while stop < numberofitems:

        t1 = Thread(target = items_job, args=(dobot1,i,side,))
        t2 = Thread(target = belt_job, args=(belt,distance,dobot0,dobot1,))

        # calculate execution time
        #start_time = time.time()

        t1.start()
        time.sleep(10) # to synchronise the procedure
        t2.start()

        stop = stop + 1
        i = i + 1
        belt = belt - 1
        side = not side  # changes side to put one left one right each time

        if(stop > 0 and stop % 2 == 0):
            # Identify object with JeVois Camera
            print("JEVOIS TIME\n")
            time.sleep(4) #wait for 4 seconds until items reach cameras view
            objectid = objectFound(serdev)
            time.sleep(2)  # wait for 2 seconds until items reach second cameras view
            # Samples
            #objectid = "cube.png"
            #objectid2 = "notcube.png"
            print("object id  1 : ", objectid) #com 13
            objectid2 = objectFound(serdev2) #com 17
            print("object id 2 : ", objectid2)
            Sorting(numberofitems, speed,  objectid, objectid2, dobot0, dobot1)

        t1.join()
        t2.join()

        #exectime = exectime + (time.time() - start_time)
    # execution time output
    #print("--- Sorting %s seconds ---", exectime)

"""
    #Single-Threade program
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

        if (side):
            dType.SetPTPCmdEx(dobot1, 0, Place_2X, Place_2Y, Place_2Z, 0, 1)
        else:
            dType.SetPTPCmdEx(dobot1, 0, Place_X, Place_Y, Place_Z, 0, 1)
        dType.SetEndEffectorSuctionCupEx(dobot1, 0, 1)
        side = not side  # changes side to put one left one right each time

        # go to home position after placing item
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
        else:
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
"""

def main(argv):
    # default values
    numberofitems = 2
    speed = 300
    distance = 8
    """check default values
      print("number of items : ", numberofitems)
      print("speed of robotic arm : " , speed)
      print("distance the item will travel on conveyor belt : ", distance)"""

    try:
        opts, args = getopt.getopt(argv, "hn:p:s:d:", ["numberofitems=", "speed=", "distance="])
    except getopt.GetoptError:
        print('control.py -n <numberofitems> -s <speed>')
        sys.exit(2)
    for opt, arg in opts:# runs with default values
        if opt == '-h': # print usage of program
            print('USAGE : control.py -n <numberofitems> -s <speed>')
        elif opt in ("-n", "--numberofitems"):
            if (numberofitems > 0):
                if (numberofitems % 2 != 0):
                    print("Must be even number of items")
                else:
                    numberofitems = int(arg)
        elif opt in ("-d", "--distance"):
            distance = int(arg)
            if (distance > 10 or distance < 0):
                print("wrong distance, defaulting to 5\n")
                distance = 8
        elif opt in ("-s", "--speed"):
            speed = int(arg)
            if (speed < 321 and speed > 0):
                print("Outside speed limits, defaulting to 300")
                speed = 300
    print('Number of items is ', numberofitems)
    print('Speed of joints : ', speed)
    print("distance the item will travel on conveyor belt : ", distance)

    CON_STR = {
        dType.DobotConnect.DobotConnect_NoError: "DobotConnect_NoError",
        dType.DobotConnect.DobotConnect_NotFound: "DobotConnect_NotFound",
        dType.DobotConnect.DobotConnect_Occupied: "DobotConnect_Occupied"
    }

    # Load Dll and get the CDLL object
    dobot0, state1 = dType.ConnectDobotX("COM3") # sorting
    dobot1, state2 = dType.ConnectDobotX("COM9") # pick and place

    # print(dType.ConnectDobotX("COM3"))
    # print(dType.ConnectDobotX("COM6"))
    # Connect Dobot
    print("Connect status1:", CON_STR[state1[0]])
    print("Connect status2:", CON_STR[state2[0]])

    PickandPlace(numberofitems,speed,distance,dobot0,dobot1)

    # Disconnect All Dobots
    dType.DisconnectAll()



if __name__ == "__main__":
    main(sys.argv[1:])
