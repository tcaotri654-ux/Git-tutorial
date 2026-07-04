#python Alarm Clock
import os
import time
import datetime
import pygame
import threading


def parse_alarm_time(alarm_time):
    text = alarm_time.strip()
    parts = text.split(":")

    if len(parts) == 2:
        hour, minute = map(int, parts)
        second = 0
    elif len(parts) == 3:
        hour, minute, second = map(int, parts)
    else:
        raise ValueError("Định dạng thời gian không hợp lệ. Hãy dùng HH:MM hoặc HH:MM:SS")

    if not (0 <= hour <= 23 and 0 <= minute <= 59 and 0 <= second <= 59):
        raise ValueError("Giá trị giờ/phút/giây không hợp lệ")

    return datetime.time(hour, minute, second)


def set_alarm(alarm_time):
    print(f"Alarm set for {alarm_time}")

    try:
        target_time = parse_alarm_time(alarm_time)
    except ValueError as err:
        print(err)
        return

    script_dir = os.path.dirname(os.path.abspath(__file__))
    sound_file = os.path.join(script_dir, "doki_doki.mp3")

    if not os.path.exists(sound_file):
        print(f"Sound file not found: {sound_file}")
        return

    while True:
        now = datetime.datetime.now()
        target_dt = datetime.datetime.combine(now.date(), target_time)

        if target_dt <= now:
            print("Wake Up!")
            print("Press Enter to stop the alarm clock")

            pygame.mixer.init()
            pygame.mixer.music.load(sound_file)

            alarm_active = True

            def wait_for_input():
                nonlocal alarm_active
                input()
                alarm_active = False
                pygame.mixer.music.stop()
                print("Alarm stopped!")

            input_thread = threading.Thread(target=wait_for_input, daemon=True)
            input_thread.start()

            while alarm_active:
                if not pygame.mixer.music.get_busy():
                    pygame.mixer.music.play(-1)
                time.sleep(0.1)
            break

        print(now.strftime("%H:%M:%S"))
        time.sleep(1)


if __name__ == "__main__":
    alarm_time = input("Enter the alarm time(HH:MM or HH:MM:SS): ")
    set_alarm(alarm_time)

