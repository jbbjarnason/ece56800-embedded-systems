print("starting")
current_year = int(input("Year: "))
current_month = int(input("Month: "))
current_day = int(input("Day: "))
current_weekday = int(input("Weekday: "))
current_hour = int(input("Hour: "))
current_minute = int(input("Minute: "))
current_second = int(input("Second: "))
current_microsecond = int(input("Microsecond: "))

# Use the real-time clock (RTC) and a hardware timer to print the current date and time every 10 seconds.

# Import the machine module.
from machine import RTC, Timer, Pin, PWM

# Create a RTC object.
rtc = RTC()
rtc.datetime((current_year, current_month, current_day, current_weekday, current_hour, current_minute, current_second, current_microsecond))

# Use second hardware timer of esp32
timer = Timer(
    1,
    mode=Timer.PERIODIC,
    period=10000,
    callback=lambda t: print(rtc.datetime())
)

# Initialize and start a PWM signal on the external LED using a frequency of 1 Hz and a duty cycle of 256. The LED
# should start blinking at the 1 Hz frequency.
pwm0 = PWM(Pin(22), freq=1, duty_u16=2560)

# Detect a switch press using an interrupt/callback. Implement switch debouncing using another timer-based
# interrupt/callback. The switch press in intended to affect the LED’s blink rate (i.e., the PWM frequency).
# No change should occur in the LED’s intensity.
class Debounce:
    def __init__(self, pin: Pin, callback, delay=50, timer_id=2):
        self.pin = pin
        self.callback = callback
        self.delay = delay
        self.timer_id = timer_id
        self.timer = None
        self.pin.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=self.interrupt)
        self.last_state = self.pin.value()

    def interrupt(self, pin):
        self.last_state = pin.value()
        if self.timer:
            self.timer.deinit()
            self.timer = None
        self.timer = Timer(self.timer_id)
        self.timer.init(period=self.delay, mode=Timer.ONE_SHOT, callback=lambda t: self.callback(self.last_state))

# – When you press the switch for the first time, the LED should start blinking faster at a frequency of 5 Hz.
# – When you press the switch for the second time, the LED should go back to blinking slowly at a frequency of 1 Hz.
# – The third switch press should result in a fast blink (5 Hz), the fourth press should result in a slow blink (1
# Hz), and so on...

def change_frequency(state):
    frequency = pwm0.freq()
    if state:
        frequency = 5 if frequency == 1 else 1
        pwm0.freq(frequency)

pin = Debounce(Pin(23, Pin.IN, Pin.PULL_UP), change_frequency)
