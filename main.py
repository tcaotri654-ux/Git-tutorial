import os
import time
import datetime
import threading
from pygame import mixer

mixer.init()

def wait_for_input():
    global alarm_active
    input()
    alarm_active = False
    mixer.music.stop()
    print("\n🔔 Báo thức đã dừng! Stop the alarm! Have a great day, ông bạn!")

# --- GIỮ LẠI HÀM XỊN CỦA ÔNG Ở ĐÂY ---
def parse_alarm_time(alarm_time):
    text = alarm_time.strip()
    parts = text.split(":")

    if len(parts) == 2:
        hour, minute = map(int, parts)
        second = 0
    elif len(parts) == 3:
        hour, minute, second = map(int, parts)
    else:
        raise ValueError("❌ Error: Invalid format! Hãy dùng HH:MM hoặc HH:MM:SS")

    if not (0 <= hour <= 23 and 0 <= minute <= 59 and 0 <= second <= 59):
        raise ValueError("❌ Error: Invalid values! Giá trị giờ/phút/giây không hợp lệ")

    return datetime.time(hour, minute, second)

def set_alarm(alarm_time):
    global alarm_active
    
    # Ráp hàm của ông vào đây để lấy target_time sạch
    try:
        target_time = parse_alarm_time(alarm_time)
    except ValueError as e:
        print(e)  # In ra câu báo lỗi ở trên
        return

    # Khúc dưới giữ nguyên...
    script_dir = os.path.dirname(os.path.abspath(__file__))
    sound_file = os.path.join(script_dir, "doki_doki.mp3")
    
    if not os.path.exists(sound_file):
        print(f"❌ Error: File not found! Không tìm thấy file tại: {sound_file}")
        return

    mixer.music.load(sound_file)
    print(f"⏰ Alarm set for: {target_time}. Monitoring time... Đang theo dõi...")

    alarm_triggered = False
    alarm_active = True

    while True:
        now = datetime.datetime.now()
        target_dt = datetime.datetime.combine(now.date(), target_time)

        print(f"⏱️ Current Time: {now.strftime('%H:%M:%S')}", end="\r")

        if now >= target_dt and not alarm_triggered:
            print("\n🚨 WAKE UP!!! DẬY ĐI ÔNG BẠN ƠI!!! 🚨")
            print("👉 Press [ENTER] to turn off the alarm / Nhấn Enter để tắt nhạc.")
            
            mixer.music.play(-1)
            alarm_triggered = True
            
            input_thread = threading.Thread(target=wait_for_input, daemon=True)
            input_thread.start()

        if alarm_triggered and not alarm_active:
            break

        time.sleep(1)

if __name__ == "__main__":
    alarm_time = input("Enter alarm time / Nhập thời gian báo thức (HH:MM or HH:MM:SS): ")
    set_alarm(alarm_time)
