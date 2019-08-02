from machine import ADC, Pin, SPI
import utime, math

import max7219 # https://github.com/mcauser/micropython-max7219

# ESP32 max7219 8x8 LED Matrix
# 5V    VCC
# GND   GND
# D2    DIN
# D5    CS
# D4    CLK

# -- set up 8 pix matrices of 8x8 LED (monochrome) 
spi = SPI(1, baudrate=10000000, polarity=1, phase=0, sck=Pin(4), mosi=Pin(2))
ss = Pin(5, Pin.OUT)
display = max7219.Matrix8x8(spi, ss, 4)
display.fill(0)
display.show()
    
# -- power the joystick with +3.3V
xPin, yPin, cPin = 34, 32, 27

# -- ADC: see https://docs.micropython.org/en/latest/esp32/quickref.html#adc-analog-to-digital-conversion

width = 10
_width = {9:ADC.WIDTH_9BIT, 10:ADC.WIDTH_10BIT,
          11:ADC.WIDTH_11BIT, 12:ADC.WIDTH_12BIT,}

X = ADC(Pin(xPin, Pin.IN))
X.atten(ADC.ATTN_11DB) # set 11dB input attentuation (voltage range roughly 0.0v - 3.6v)
X.width(_width[width])  

Y = ADC(Pin(yPin, Pin.IN))
Y.atten(ADC.ATTN_11DB) # set 11dB input attentuation (voltage range roughly 0.0v - 3.6v)
Y.width(_width[width]) 

cButton = Pin(cPin, Pin.IN, Pin.PULL_UP)

# -- initialize, assuming central position at startup
x0, y0 = X.read(), Y.read()

def getXY():
    """
    return x and y, between ~ -1 and +1 (+- ~5%)
    """
    global X, Y, x0, x0, width
    return (X.read()-x0)/2**(width-1), (Y.read()-x0)/2**(width-1)

x, y = 2.0, 2.0
i = 0
while True:
    dx, dy = getXY()
    # -- round to closest 0.1
    dx, dy = int(10*dx)/10, int(10*dy)/10
    #print('x=%5.2f y=%5.2f'%(x, y) )
    if dx>0:
        x += math.sqrt(abs(dx))/5
    else:
        x -= math.sqrt(abs(dx))/5
    if dy>0:
        y += math.sqrt(abs(dy))/5
    else:
        y -= math.sqrt(abs(dy))/5

    x, y = x%32, y%8

    if cButton.value():
        display.fill(0)
    display.pixel(int(x), int(y), 1)
    i+=1
    display.show()
    #utime.sleep(0.1)
    
