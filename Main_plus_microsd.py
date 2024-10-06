# Start MicroSD 
import machine
import sdcard
import os

# Set up SD card
sd_spi = machine.SPI(1, sck=machine.Pin(10), mosi=machine.Pin(11), miso=machine.Pin(12))
sd = sdcard.SDCard(sd_spi, machine.Pin(13))
os.mount(sd, '/sd')

def read_lshow_file(filename):
    with open('/sd/' + filename, 'rb') as f:
        f.read(8)  # Skip magic number and JSON length
        return ujson.loads(f.read())

# Rest of your code remains the same


import machine
import ujson
import time

# Define the GPIO pins connected to LEDs
leds = [machine.Pin(i, machine.Pin.OUT) for i in range(8)]

def set_leds(values):
    for led, value in zip(leds, values):
        led.value(value)

def read_lshow_file(filename):
    with open(filename, 'rb') as f:
        f.read(8)  # Skip magic number and JSON length
        return ujson.loads(f.read())

def play_light_show(data, cycles=50):
    start_time = time.ticks_ms()
    for _ in range(cycles):
        for frame in data['frames']:
            set_leds(frame)
            time.sleep_ms(50)  # 50ms delay
    end_time = time.ticks_ms()
    duration = time.ticks_diff(end_time, start_time) / 1000
    print(f"Light show ran for {duration:.2f} seconds")

def run_test_pattern(cycles=30):
    start_time = time.ticks_ms()
    for _ in range(cycles):
        for i in range(8):
            set_leds([j == i for j in range(8)])
            time.sleep_ms(100)
    end_time = time.ticks_ms()
    duration = time.ticks_diff(end_time, start_time) / 1000
    print(f"Test pattern ran for {duration:.2f} seconds")

try:
    light_data = read_lshow_file('minimal_test.lshow')
    play_light_show(light_data)
except OSError:
    print("Couldn't find .lshow file. Running test pattern.")
    run_test_pattern()

print("Script finished. All LEDs off.")
for led in leds:
    led.off()
