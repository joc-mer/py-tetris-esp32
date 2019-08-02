Erase the flash
```esptool.py --chip esp32 --port /dev/tty. erase_flash```

Install `ampy`command
```pip install adafruit-ampy```

Get the boot.py
```ampy --port /dev/tty.SLAB_USBtoUART get boot.py```

Connect to the esp32's terminal
```screen /dev/tty.SLAB_USBtoUART 115200```

To quit
```
ctrl + a
:
quit
```

Copy a file on the chip
```ampy --port /dev/tty.SLAB_USBtoUART put micropython-max7219/max7219.py```

