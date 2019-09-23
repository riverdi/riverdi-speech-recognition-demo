
from riverdi.displays.bt81x import ctp50
from bridgetek.bt81x import bt81x
from fortebit.easyvr import easyvr

import streams
import gui

 
#relay functions
def relay_on():
    digitalWrite(D23, HIGH)
    
def relay_off():
    digitalWrite(D23, LOW)

pin = ""                #pin which user enter
valid_pin = "1234"      #valid pin
valid_pin2 = "2580" 
screenLayout = 0        #window currently used
wait = False
counter = 0
user2 = False

#serial communication
pc = streams.serial() 
ser = streams.serial(SERIAL1, baud=9600,set_default=False)

evr = easyvr.EasyVR(ser)

#buttons handler
def pressed(tag, tracked, tp):
    
    global screenLayout
    global pin
    global wait
    global counter
    global user2
    
    #if we are in pinscreen
    if (screenLayout == 2):
        
        counter = 0
        user2 = False
        
        #if we don't click c or connect button and length of pin is no longer than 4 characters
        if ((tag != 67) and (tag !=1)):
            if  (len(pin) >= 4):
                return
            pin = pin + str(chr(tag))
            
        #if we click c button and pin is at least 1 character long
        elif ((tag == 67) and (len(pin) > 0)):
            pin = pin[:-1]
        
        #if we click connect and the pin is valid
        elif ((tag == 1) and ((pin == valid_pin) or (pin == valid_pin2))):
            if pin == valid_pin2:
                user2 = True
            screenLayout = 4
            
        #if we click connect and the pin is invalid but user have to write something
        elif (len(pin) > 0):
            wait = True
            pin = ""
            #[3]access denied
            gui.showMessage("Access Denied")
            #go to screensaver
            evr.playSound(SND_Access_denied, evr.VOL_FULL)
            
           
#image resources
new_resource('images/gui_riverdi_logo.png')
new_resource('images/screensaver.png')


#command definition
SND_Access_denied=1
SND_Access_granted=2
SND_Hello=3
SND_Please_repeat=4
SND_Please_say_your_password=5
SND_Hello_give_command=6
SND_Please_say_name=7
SND_Pwd_activated=8

#module init
pinMode(D23, OUTPUT)

# init display
bt81x.init(SPI0, D4, D33, D34)
 
#config EasyVR
evr.setLevel(2)
evr.setLanguage(evr.ENGLISH)
evr.setKnob(evr.STRICTER)
evr.setCommandLatency(evr.MODE_FAST)
evr.setTimeout(6)


#checking if module is connected
while not evr.detect():
    print("EasyVR not detected!")
print("EasyVR detected")
id = evr.getID()
print("EasyVR version id: %s" % id)


#show all uploaded sounds
mask = evr.getGroupMask()
if mask != None:
    # get trained user names and passwords
    for group in range(evr.PASSWORD + 1): #all groups: 0 to 16
        if mask & 0x01 != 0:
            count = evr.getCommandCount(group)
            if group == evr.TRIGGER:
                print("Trigger: "+ str(count))
            elif group == evr.PASSWORD:
                print("Password: " + str(count))
            else:
                print("Group " + str(group) + ": " + str(count))
            for idx in range(count):
                (name, train) = evr.dumpCommand(group, idx)
                if not evr.isConflict():
                    print("%d %s Trained %d times, OK" % (idx,name,train))
                else:
                    confl = evr.getWord()
                    if confl >= 0:
                        print("%d %s Trained  %d times, Similar to Word %d" % (idx,name,train,confl))
                    else:
                        confl = evr.getCommand()
                        print("%d %s Trained  %d times, Similar to Command %d" % (idx,name,train,confl))
        mask >>= 1


# one callback for all tags
bt81x.touch_loop(((-1, pressed), ))


# screenLayout value map
#[0] show logo
#[1] screensaver
#[2] pin screen
#[3] access denied
#[4] enter voice password
#[5] access granted


#[0] show logo
gui.loadImage('gui_riverdi_logo.png')
gui.showLogo()
sleep(3000)


#to get smooth transition between 0 and 1 screen
bt81x.clear_color(rgb=(0x00, 0x00, 0x00))
bt81x.clear(1, 1, 1)
bt81x.display()
bt81x.swap_and_empty()
screenLayout = 1

###########################################################

#main loop
while 1:
    
    if screenLayout == 1:
        #[1] screensaver
        gui.loadImage("screensaver.png")

        #screensaver logo parameters
        screensaver_logo_width = 300
        screensaver_logo_height = 75
        evr.recognizeWord(4)
        cnt = 0

    while screenLayout == 1:
        if evr.hasFinished():
            if evr.getWord() == 0:
                screenLayout = 2
                break
            evr.recognizeWord(4)
        else:
            cnt += 1
            sleep(100)
            if (cnt == 20):
                x = random(1,bt81x.display_conf.width - screensaver_logo_width)
                y = random(1,bt81x.display_conf.height - screensaver_logo_height)
                gui.showScreensaver(x,y)
                cnt = 0

###########################################################

    counter = 0
    while (screenLayout == 2):
        # [2] pin screen
        if (wait == True):
            wait = False
            sleep(2000)
        gui.pinScreen(pin)
        #wait after wrong password
        if counter == 500:
            screenLayout = 1
        sleep(10)
        counter += 1
    pin=""
    
###########################################################

    if screenLayout == 4:
        #[4] enter voice password
        gui.showMessage("Enter Voice Password")
        evr.playSound(SND_Please_say_your_password, evr.VOL_FULL)

        #checking if user said correct Password
        
        while screenLayout == 4:
            evr.recognizeCommand(16)
            while not evr.hasFinished():
                sleep(100)
            #if user say sth but can't recognize what 
            if ((evr.getCommand() == -1) and (not evr.isTimeout())):
                #[3]access denied
                gui.showMessage("Access Denied")
                evr.playSound(SND_Access_denied, evr.VOL_FULL)
                sleep(1000)
                break
            #if user say not his voice Password
            if ((user2 and (evr.getCommand() != 2) and (evr.getCommand() != -1)) or ((not user2) and  ((evr.getCommand() != 5) and (evr.getCommand() != -1)))):
                gui.showMessage("Access Denied")
                evr.playSound(SND_Access_denied, evr.VOL_FULL)
                sleep(1000)
                break
            if evr.isTimeout():
                #if time out go to pin screen
                screenLayout = 2
                break
            elif (evr.getCommand() == 2 and user2) or (evr.getCommand() == 5 and (not user2)):
                #if command recognized and correct according to entered pin, go further
                screenLayout = 5
                break
            #evr.recognizeCommand(1)
        #print(evr.getCommand())
###########################################################

    if screenLayout == 5:
        #[5] access granted
        gui.showMessage("Access Granted")
        evr.playSound(SND_Access_granted, evr.VOL_FULL)
        sleep(1000)

        relay_on()
        for i in range(5):
            time = str(5-i)
            gui.showMessage("time left: " + time)
            sleep(1000)
        relay_off()
        screenLayout = 1
#ser.close()
