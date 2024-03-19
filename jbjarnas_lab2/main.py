import machine
import ntptime
import esp32

# The red LED should be ON whenever the ESP32 is awake and OFF when it is in sleep mode.
red = machine.Pin(22, machine.Pin.OUT)
red.value(True)

if machine.reset_cause() == machine.DEEPSLEEP_RESET:
    if machine.wake_reason() == 2:
        print("Woke up due to EXT0 wakeup.")
    elif machine.wake_reason() == 4:
        print("Woke up due to TIMER wakeup.")

# The program should use the network module in MicroPython to connect your ESP32 to a WiFi network using the
# ‘SSID’ and ‘Password’ for that network.

def do_connect():
    import network
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        wlan.connect('DialUp', 'jbb2410abh')
        while not wlan.isconnected():
            pass
    print(f'Connected to {wlan.config("ssid")}')
    print(f'IP Address: {wlan.ifconfig()[0]}')

do_connect()

# Get the current time from the Internet using NTP. The program should fetch the current date and time from the
# NTP server ‘pool.ntp.org’ and use it to set the RTC (real time clock).

ntptime.settime()
rtc = machine.RTC()
# Change from UTC to EST
now = rtc.datetime()

est_hour = now[4] - 5
est_day = now[2]
if est_hour < 0:
    est_hour += 24
    est_day -= 1

rtc.datetime((now[0], now[1], est_day, now[3], est_hour, now[5], now[6], now[7]))


def do_print_time():
    # Date: 09/29/2021
    # Time: 10:00:00 HRS
    year, month, day, weekday, hour, minute, second, _ = rtc.datetime()
    formatted_output = "Date: {:02}/{:02}/{:04}\nTime: {:02}:{:02}:{:02} HRS".format(month, day, year, hour, minute, second)
    print(formatted_output)

# Initialize a hardware timer and display the current date and time every 15 seconds. Do not use time.sleep().
# Instead, use the RTC and Timer interrupt/callback.

print_timer = machine.Timer(1, mode=machine.Timer.PERIODIC, period=15000, callback=lambda t: do_print_time())

# Initialize a second hardware timer and read the touch pin values every 50 milliseconds using a Timer interrup-
# t/callback and implement the following pattern. Use calibrated values to detect whether the wire is touched or not.

touch = machine.TouchPad(machine.Pin(14))
green = machine.Pin(32, machine.Pin.OUT)
poll_touch = machine.Timer(2, mode=machine.Timer.PERIODIC, period=50, callback=lambda t: green.value(touch.read() < 100))


# Use a third hardware timer to put the ESP32 into deep sleep every 30 seconds for a duration of 1 minute. Print
# out a message on the terminal before going to sleep like:

def do_sleep():
    print("I am going to sleep for 1 minute.")
    red.value(False)
    machine.deepsleep(60000)

sleep_timer = machine.Timer(3, mode=machine.Timer.ONE_SHOT, period=30000, callback=lambda t: do_sleep())

# External Wake Up Mode 0: Configure the switch as an external wake-up source. Pressing the switch within
# the 1-minute sleep duration should wake up the board and print out it’s an EXT0 wake-up.
wake_pin = machine.Pin(13, machine.Pin.IN, machine.Pin.PULL_UP)
esp32.wake_on_ext0(pin=wake_pin, level=esp32.WAKEUP_ALL_LOW)
