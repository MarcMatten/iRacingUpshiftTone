# import packages
import irsdk
from pygame import *
import winsound

fname = "Beep.wav"  # path to beep soundfile

ir = irsdk.IRSDK()  # initialize iRacing SDK

wasRunning = 0  # flag to check if iRacing was running

print('Waiting for iRacing...')  # initialisation message

# shut down programme if iRacing is not found within one minute
while not ir.startup():
    time.wait(6000)
    print('iRacing not detected. Shutting down...')
    break

# initialisaiton if iRacing is detected
if ir.startup():
    wasRunning = 1
    print('iRacing detected! :-)')

    # play three beep sounds as notification
    winsound.PlaySound(fname, winsound.SND_FILENAME)
    time.wait(300)
    winsound.PlaySound(fname, winsound.SND_FILENAME)
    time.wait(300)
    winsound.PlaySound(fname, winsound.SND_FILENAME)

    # get optimal shift RPM from iRacing and display message
    ShiftRPM = ir['DriverInfo']['DriverCarSLShiftRPM']

    DriverCarIndex = ir['DriverInfo']['DriverCarIdx']
    DriverCarName = ir['DriverInfo']['Drivers'][DriverCarIndex]['CarScreenNameShort']

    # ir['DriverInfo']['Drivers'][ir['DriverInfo']['DriverCarIdx']]['CarScreenNameShort']
    print('Optimal Shift RPM for', DriverCarName,':', ShiftRPM)

    IsOnTrack = False  # flag to check if car has been on track in this session

# execute this loop while iRacing is running
while ir.startup():
    # two beeps sounds as notification when entering track
    if ir['IsOnTrack'] and not IsOnTrack:
        IsOnTrack = True
        winsound.PlaySound(fname, winsound.SND_FILENAME)
        time.wait(300)
        winsound.PlaySound(fname, winsound.SND_FILENAME)

    # execute this loop while player is on track
    while ir['IsOnTrack']:
        # get currenct vehicle data from iRacing
        RPM = ir['RPM']
        Gear = ir['Gear']

        #	check if upshift RPM is reached
        if Gear > 0 and RPM >= ShiftRPM:  # disable sound for neutral and reverse gear
            winsound.PlaySound(fname, winsound.SND_FILENAME)
            time.wait(750)  # pause for 750 ms to avoid multiple beeps when missing shiftpoint

    # update flag when leaving track
    if not ir['IsOnTrack'] and IsOnTrack:
        IsOnTrack = False

    # shut down programme when iRacing terminates
    if wasRunning == 1 and ir.startup() == False:
        print('iRacing terminated. Shutting down...')
        break