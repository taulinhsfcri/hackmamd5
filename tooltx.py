import pygame
import random
import time
from collections import Counter
from colorama import Fore, Style, init

# Khởi tạo colorama
init(autoreset=True)

# Khởi tạo pygame để xử lý âm thanh
pygame.mixer.init()

# Tải tệp âm thanh lắc xúc xắc
dice_sound = pygame.mixer.Sound('c:\\Users\\tailinh\\Downloads\\iLoveTik.com_TikTok_Media_002_610bfa3b30240dcd9542468483f55707.m4a')  # Thay 'dice_roll.wav' bằng đường dẫn tệp âm thanh của bạn

# Lưu lịch sử kết quả
history = []  # Lưu lịch sử các kết quả tài/xỉu

def is_valid_md5(md5_hash):
    """Kiểm tra tính hợp lệ của mã MD5"""
    return len(md5_hash) == 32 and all(c in "0123456789abcdefABCDEF" for c in md5_hash)

def analyze_history():
    """Phân tích lịch sử kết quả Tài/Xỉu để tìm xu hướng"""
    if len(history) < 2:
        return "Không đủ dữ liệu lịch sử để phân tích."
    
    # Chuẩn hóa tất cả kết quả về chữ hoa để tránh vấn đề so sánh
    history_normalized = [result.upper() for result in history]

    # Đếm số lần xuất hiện của Tài và Xỉu
    counter = Counter(history_normalized)
    percent_tai = (counter["TÀI"] / len(history_normalized)) * 100
    percent_xiu = (counter["XỈU"] / len(history_normalized)) * 100
    
    return {
        "percent_tai": round(percent_tai, 2),
        "percent_xiu": round(percent_xiu, 2),
        "history": history_normalized
    }

def generate_outcome_from_md5(md5_hash):
    """Tạo kết quả Tài/Xỉu từ MD5 và hỗ trợ cầu ngược"""
    numeric_value = int(md5_hash[:8], 16)  # Lấy 8 ký tự đầu tiên của MD5
    total = sum([((numeric_value >> (4 * i)) % 6) + 1 for i in range(3)])  # Tổng 3 con xúc xắc
    
    # Tính toán tổng giá trị cầu ngược nếu có
    reverse_total = sum([int(digit) for digit in str(numeric_value)[:3]])  # Cầu ngược từ ba chữ số đầu tiên
    
    return total, reverse_total, "Tài" if total >= 11 or reverse_total >= 11 else "Xỉu"

def print_with_effect(text, color=Fore.GREEN):
    """In văn bản với hiệu ứng"""
    for char in text:
        print(color + char, end='', flush=True)
        time.sleep(0.01)
    print()

def print_dice_roll():
    """In hình ảnh mô phỏng xúc xắc và con rồng với hiệu ứng lắc và âm thanh"""
    dice_faces = ['⚀', '⚁', '⚂', '⚃', '⚄', '⚅']
    print(Fore.RED + Style.BRIGHT + """
        Lắc xúc xắc... 🎲🎲🎲
    """)
    
    # Lắc xúc xắc 3 lần, mỗi lần hiển thị xúc xắc ngẫu nhiên và phát âm thanh
    for _ in range(3):
        dice_roll = [random.choice(dice_faces) for _ in range(3)]
        print("Lắc: " + ' '.join(dice_roll), end='\r', flush=True)
        dice_sound.play()  # Phát âm thanh lắc xúc xắc
        time.sleep(0.5)  # Thời gian lắc
    time.sleep(1)  # Thời gian nghỉ trước khi hiển thị kết quả

def make_prediction(md5_hash, history_analysis):
    """Phân tích và đưa ra dự đoán dựa trên tất cả các yếu tố"""
    # Tỷ lệ Tài và Xỉu từ lịch sử
    percent_tai = history_analysis['percent_tai']
    percent_xiu = history_analysis['percent_xiu']
    
    # Kết quả từ MD5
    total, reverse_total, generated_outcome = generate_outcome_from_md5(md5_hash)

    # Quyết định dựa trên tỷ lệ và kết quả MD5
    if percent_tai > percent_xiu:
        if generated_outcome == "Tài":
            trend_outcome = "Tài (Dự đoán chắc chắn dựa trên lịch sử và MD5)"
        else:
            trend_outcome = "Tài (Dựa vào xu hướng lịch sử, nhưng MD5 lại cho Xỉu)"
    else:
        if generated_outcome == "Xỉu":
            trend_outcome = "Xỉu (Dự đoán chắc chắn dựa trên lịch sử và MD5)"
        else:
            trend_outcome = "Xỉu (Dựa vào xu hướng lịch sử, nhưng MD5 lại cho Tài)"
    
    return total, reverse_total, generated_outcome, trend_outcome

def main():
    print(Fore.CYAN + Style.BRIGHT + "Tool Dự đoán Tài/Xỉu")
    print(Fore.CYAN + "=" * 30)
    
    while True:
        md5_input = input(Fore.WHITE + "Nhập mã MD5 cần dự đoán (hoặc 'exit' để thoát): ").strip()
        
        if md5_input.lower() == 'exit':
            print(Fore.CYAN + "Thoát chương trình. Cảm ơn đã sử dụng!")
            break

        if not is_valid_md5(md5_input):
            print(Fore.RED + "Mã MD5 không hợp lệ.")
            continue
        
        # Nhập lịch sử kết quả các phiên trước (Tài/Xỉu)
        input_history = input(Fore.WHITE + "Nhập kết quả các phiên trước (Tài/Xỉu) cách nhau bằng dấu phẩy, ví dụ: Tài, Xỉu, Tài: ").strip()
        
        # Xử lý lịch sử người dùng nhập vào
        if input_history:
            input_history = input_history.split(',')
            input_history = [result.strip() for result in input_history]  # Loại bỏ khoảng trắng
        
        # Cập nhật lịch sử với kết quả nhập vào
        history.extend(input_history)

        # In hiệu ứng phân tích
        print_with_effect("Đang phân tích kết quả...", Fore.CYAN)
        time.sleep(5)  # Thêm thời gian phân tích trước khi ra kết quả (5 giây)

        # Phân tích lịch sử và tỷ lệ Tài/Xỉu
        history_analysis = analyze_history()
        
        # In xúc xắc và con rồng
        print_dice_roll()
        
        # Hiển thị tỷ lệ Tài và Xỉu
        print(Fore.YELLOW + f"Tỷ lệ Tài: {history_analysis['percent_tai']}%")
        print(Fore.YELLOW + f"Tỷ lệ Xỉu: {history_analysis['percent_xiu']}%")
        
        # In các kết quả phân tích và dự đoán
        total, reverse_total, md5_outcome, trend_outcome = make_prediction(md5_input, history_analysis)
        
        # Kết quả sẽ được in sau khi phân tích xong
        print(Fore.GREEN + f"Kết quả dự đoán cuối cùng: {md5_outcome}")
        print(Fore.GREEN + f"Kết quả cầu ngược (từ ba chữ số đầu của MD5): Tổng xúc xắc = {total}, Cầu ngược = {reverse_total}")
        print(Fore.GREEN + f"Kết quả dựa vào xu hướng lịch sử: {trend_outcome}")
        
        print(Fore.CYAN + f"Lịch sử kết quả: {', '.join(history_analysis['history'])}")
        
        print(Fore.CYAN + "=" * 30)
        time.sleep(30)  # Đợi 30 giây cho người dùng quyết định cược

if __name__ == "__main__":
    main() 