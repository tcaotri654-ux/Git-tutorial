import os
import sys
import time
import datetime
import threading
from pygame import mixer

# Initialize the mixer module for audio playback
# Khởi tạo bộ trộn âm thanh để chuẩn bị phát nhạc
mixer.init()

def wait_for_input():
    global alarm_active
    input()  # Wait for the user to press [ENTER]
    
    alarm_active = False
    mixer.music.stop()  # Stop the music
    print("\n🔔 Báo thức đã dừng! Stop the alarm! Have a great day, ông bạn!")

def set_alarm(alarm_time):
    global alarm_active
    
    # Parse the input string into a datetime object
    # Phân tích chuỗi nhập vào thành kiểu dữ liệu thời gian
    try:
        if len(alarm_time.split(':')) == 2:
            target_time = datetime.datetime.strptime(alarm_time, "%H:%M").time()
        else:
            target_time = datetime.datetime.strptime(alarm_time, "%H:%M:%S").time()
    except ValueError:
        print("❌ Error: Wrong format! Nhập sai định dạng rồi ông ơi (HH:MM / HH:MM:SS)")
        return

    # Locate the audio file (doki_doki.mp3)
    # Xác định đường dẫn file nhạc trong thư mục
    script_dir = os.path.dirname(os.path.abspath(__file__))
    sound_file = os.path.join(script_dir, "doki_doki.mp3")
    
    if not os.path.exists(sound_file):
        print(f"❌ Error: File not found! Không tìm thấy file tại: {sound_file}")
        return

    mixer.music.load(sound_file)
    print(f"⏰ Alarm set for: {target_time}. Monitoring time... Đang theo dõi...")

    alarm_triggered = False
    alarm_active = True

    # Main Loop: Continuously check the current time
    # Vòng lặp chính: Kiểm tra thời gian liên tục
    while True:
        now = datetime.datetime.now()
        target_dt = datetime.datetime.combine(now.date(), target_time)

        # Print current time on the same line (end="\r" prevents scrolling)
        # In thời gian chạy giây nhảy số liên tục tại đúng một dòng cho đẹp
        print(f"⏱️ Current Time: {now.strftime('%H:%M:%S')}", end="\r")

        # Condition to trigger the alarm
        # Điều kiện kích hoạt còi báo thức
        if now >= target_dt and not alarm_triggered:
            print("\n🚨 WAKE UP!!! DẬY ĐI ÔNG BẠN ƠI!!! 🚨")
            print("👉 Press [ENTER] to turn off the alarm / Nhấn Enter để tắt nhạc.")
            
            mixer.music.play(-1)  # Loop indefinitely (Phát lặp vô hạn)
            alarm_triggered = True
            
            # Start a background thread to handle user input without freezing the clock
            # Chạy luồng phụ (Threading) để đợi bấm Enter mà không làm đứng đồng hồ
            input_thread = threading.Thread(target=wait_for_input, daemon=True)
            input_thread.start()

        # Break the loop if the alarm was triggered and turned off
        # Thoát vòng lặp nếu báo thức đã kêu xong và đã được tắt
        if alarm_triggered and not alarm_active:
            break

        # CPU Lifesaver: Sleep for 1 second to reduce CPU usage
        # Cho vòng lặp nghỉ 1 giây để bảo vệ CPU không bị nóng máy
        time.sleep(1)

if __name__ == "__main__":
    alarm_time = input("Enter alarm time / Nhập thời gian báo thức (HH:MM or HH:MM:SS): ")
    set_alarm(alarm_time)
