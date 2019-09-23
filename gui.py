
from riverdi.displays.bt81x import ctp50
from bridgetek.bt81x import bt81x


#
# loadImage
#
def loadImage(image):
    bt81x.load_image(0, 0, image)

#
# showLogo
#
def showLogo():

    # start
    bt81x.dl_start()
    bt81x.clear_color(rgb=(0xff, 0xff, 0xff))
    bt81x.clear(1, 1, 1)
    
    # image
    image = bt81x.Bitmap(1, 0, (bt81x.ARGB4, 642 * 2), (bt81x.BILINEAR, bt81x.BORDER, bt81x.BORDER, 642, 144))
    image.prepare_draw()
    image.draw(((bt81x.display_conf.width - 642)//2, (bt81x.display_conf.height - 144)//2), vertex_fmt=0)

    # display
    bt81x.display()
    bt81x.swap_and_empty()

#
# pinScreen
#
def pinScreen(pin):
    
    pin_masked = "****"
    pin_length = len(pin)
    
    # start
    bt81x.dl_start()
    bt81x.clear(1, 1, 1)
    
    #text
    #drawing instructions
    txt = bt81x.Text(200, 150, 31, bt81x.OPT_CENTERX | bt81x.OPT_CENTERY, "Enter Pin:", )
    bt81x.add_text(txt)

    #drawing user pin
    txt.text = pin_masked[:pin_length]
    txt.x = 200
    txt.y = 200
    txt.font = 31
    bt81x.add_text(txt)
        
    # keys
    bt81x.track(430, 50, 350, 70, 0)
    bt81x.add_keys(430, 50, 350, 70, 30, 0, "123")
    bt81x.add_keys(430, 130, 350, 70, 30, 0, "456")
    bt81x.add_keys(430, 210, 350, 70, 30, 0, "789")
    bt81x.add_keys(430, 290, 350, 70, 30, 0, ".0C")
    
    # connect button
    btn = bt81x.Button(430, 370, 350, 70, 30, 0, "Connect")
    bt81x.tag(1)
    bt81x.add_button(btn)

    # display
    bt81x.display()
    bt81x.swap_and_empty()
    
#
# showMessage
#
def showMessage(text):
    
    # start
    bt81x.dl_start()
    bt81x.clear(1, 1, 1)
    
    #text
    txt = bt81x.Text(400, 240, 31, bt81x.OPT_CENTERX | bt81x.OPT_CENTERY, text, )
    bt81x.add_text(txt)
    
    # display
    bt81x.display()
    bt81x.swap_and_empty()
    
#
# showScreensaver
#
def showScreensaver(x,y):
    
    # start
    bt81x.dl_start()
    bt81x.clear_color(rgb=(0x00, 0x00, 0x00))
    bt81x.clear(1, 1, 1)
    
    # image
    image = bt81x.Bitmap(1, 0, (bt81x.ARGB4, (300) * 2), (bt81x.BILINEAR, bt81x.BORDER, bt81x.BORDER, 300, 75))
    image.prepare_draw()
    image.draw((x, y), vertex_fmt=0)
    
    # display
    bt81x.display()
    bt81x.swap_and_empty()
