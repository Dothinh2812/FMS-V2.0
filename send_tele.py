import requests
import os
from typing import Union, Optional
import glob
import pandas as pd
from datetime import datetime

# Telegram credentials
#TELEGRAM_TOKEN = "7810323512:AAEL6hDjjZgz64gADrJfcKwrqO42himl3oI" #@baocaott8bot
TELEGRAM_TOKEN = "7785723852:AAFZCei8UveSC2brM01JmW76LQMkd_2nJcU" #@bts_tt8_bot
#TELEGRAM_CHAT_ID = "-4795321025" # TEST
TELEGRAM_CHAT_ID = "-4616062001" # TEST
TELEGRAM_CHAT_ID_ALL = "-4709942351" # id nhóm nhận file báo cáo toàn bộ chi tiết    

#TELEGRAM_CHAT_ID = "-4616062001" # CHÍNH THỨC

def send_message(message: str) -> bool:
    """
    Gửi tin nhắn văn bản tới Telegram.
    
    Args:
        message (str): Nội dung tin nhắn cần gửi
        
    Returns:
        bool: True nếu gửi thành công, False nếu thất bại
    """
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        data = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message,
            "parse_mode": "HTML"
        }
        response = requests.post(url, data=data)
        return response.status_code == 200
    except Exception as e:
        print(f"Lỗi khi gửi tin nhắn: {str(e)}")
        return False

def send_file(file_path: str, caption: Optional[str] = None) -> bool:
    """
    Gửi file (document, hình ảnh, biểu đồ) tới Telegram.
    
    Args:
        file_path (str): Đường dẫn tới file cần gửi
        caption (str, optional): Chú thích cho file
        
    Returns:
        bool: True nếu gửi thành công, False nếu thất bại
    """
    try:
        if not os.path.exists(file_path):
            print(f"File không tồn tại: {file_path}")
            return False

        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendDocument"
        
        files = {
            'document': open(file_path, 'rb')
        }
        
        data = {
            "chat_id": TELEGRAM_CHAT_ID
        }
        
        if caption:
            data["caption"] = caption

        response = requests.post(url, data=data, files=files)
        return response.status_code == 200
    except Exception as e:
        print(f"Lỗi khi gửi file: {str(e)}")
        return False
    finally:
        files['document'].close() if 'document' in files else None

def send_image(image_path: str, caption: Optional[str] = None) -> bool:
    """
    Gửi hình ảnh tới Telegram với định dạng ảnh (thay vì dạng document).
    
    Args:
        image_path (str): Đường dẫn tới file ảnh
        caption (str, optional): Chú thích cho ảnh
        
    Returns:
        bool: True nếu gửi thành công, False nếu thất bại
    """
    try:
        if not os.path.exists(image_path):
            print(f"File ảnh không tồn tại: {image_path}")
            return False

        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendPhoto"
        
        files = {
            'photo': open(image_path, 'rb')
        }
        
        data = {
            "chat_id": TELEGRAM_CHAT_ID
        }
        
        if caption:
            data["caption"] = caption

        response = requests.post(url, data=data, files=files)
        return response.status_code == 200
    except Exception as e:
        print(f"Lỗi khi gửi ảnh: {str(e)}")
        return False
    finally:
        files['photo'].close() if 'photo' in files else None

def send_all_reports():
    """
    Gửi tất cả các biểu đồ tới Telegram.
    """
    # Gửi thông báo bắt đầu
    send_message("🚀 Bắt đầu gửi biểu đồ...")

    # Gửi các biểu đồ PTTB
    send_message("📈 Gửi biểu đồ PTTB...")
    for file in glob.glob("pttb_chart/*.png"):
        caption = "📊 Biểu đồ PTTB"
        if "so_sanh" in file:
            caption = "📊 So sánh dịch vụ PTTB"
        elif "thong_ke" in file:
            caption = "📈 Thống kê dịch vụ chính PTTB"
        elif "ty_le_Fiber" in file:
            caption = "🌐 Tỷ lệ Fiber PTTB"
        elif "ty_le_MyTV" in file:
            caption = "📺 Tỷ lệ MyTV PTTB"
        elif "ty_le_phieu" in file:
            caption = "📝 Tỷ lệ phiếu tồn PTTB"
        elif "tong_so_phieu" in file:
            caption = "📋 Tổng số phiếu tồn PTTB"
        send_image(file, caption)

    # Gửi các biểu đồ ĐHSC
    send_message("📈 Gửi biểu đồ ĐHSC...")
    for file in glob.glob("dhsc_chart/*.png"):
        if "thong_ke_" in file:
            huyen = file.split("_")[2]
            send_image(file, f"📊 Thống kê ĐHSC - {huyen}")
        elif "ty_le_Thuê bao SIP" in file:
            send_image(file, "📞 Tỷ lệ Thuê bao SIP")
        elif "ty_le_Fiber" in file:
            send_image(file, "🌐 Tỷ lệ Fiber")
        elif "ty_le_MyTV" in file:
            send_image(file, "📺 Tỷ lệ MyTV")
        elif "ty_le_phan_tram" in file:
            send_image(file, "📈 Tỷ lệ phần trăm")
        elif "thong_ke_theo_dich_vu" in file:
            send_image(file, "📊 Thống kê theo dịch vụ")
        elif "tong_so_may_hong" in file:
            send_image(file, "🔧 Tổng số máy hỏng")

    # Gửi thông báo hoàn thành
    send_message("✅ Đã gửi xong tất cả biểu đồ!")

def send_alerts_from_excel(excel_file: str = "report_summary.xlsx") -> bool:
    """
    Read data from Excel file and send alerts via Telegram based on specific conditions:
    - Send immediately if 'N.Nhân' contains 'OOS'
    - For 'AC' alerts, only send if 'Kéo dài' > 30
    - Check for duplicate alerts within last 30 mins for AC and 20 mins for OOS
    Also logs sent messages to an Excel file
    """
    try:
        current_time = datetime.now()
        print(f"\n🕒 Bắt đầu kiểm tra cảnh báo lúc: {current_time.strftime('%Y-%m-%d %H:%M:%S')}")

        # Create log directory if it doesn't exist
        log_dir = "log_message"
        os.makedirs(log_dir, exist_ok=True)
        log_file = os.path.join(log_dir, "ban_tin_da_gui.xlsx")

        # Read Excel file
        df = pd.read_excel(excel_file)
        
        # Check required columns
        required_columns = ['Tên NE', 'Tên gợi nhớ', 'N.Nhân', 'TG Sự cố', 'Kéo dài', 'Phân Loại Trạm']
        if not all(col in df.columns for col in required_columns):
            print("❌ Thiếu một số cột dữ liệu cần thiết")
            return False

        # Filter alerts based on conditions
        df_filtered = df[
            ((df['N.Nhân'].str.contains('OOS', case=False, na=False)) |
             (df['N.Nhân'].str.contains('AC', case=False, na=False))) &
            (df['Phân Loại Trạm'] != 'Trạm viễn thông loại 3')
        ]

        # Load existing log if exists
        existing_log = pd.DataFrame()
        if os.path.exists(log_file):
            existing_log = pd.read_excel(log_file)
            existing_log['Thời gian gửi'] = pd.to_datetime(existing_log['Thời gian gửi'])

        # Count total alerts to send
        total_alerts = len(df_filtered)
        if total_alerts == 0:
            print("ℹ️ Không có cảnh báo nào cần gửi")
            return True

        print(f"📊 Số cảnh báo cần kiểm tra: {total_alerts}")

        # Prepare log data
        log_data = []
        alerts_sent = 0

        # Send alerts for filtered incidents
        for index, row in df_filtered.iterrows():
            # Check for duplicates based on alert type
            time_threshold = pd.Timedelta(minutes=30 if 'AC' in str(row['N.Nhân']).upper() else 20)
            
            if not existing_log.empty:
                # Get all matching records
                matching_records = existing_log[
                    (existing_log['Tên NE'] == row['Tên NE']) &
                    (existing_log['Nội dung cảnh báo'] == row['N.Nhân'])
                ]
                
                if not matching_records.empty:
                    # Get the most recent record
                    most_recent = matching_records['Thời gian gửi'].max()
                    time_since_last = current_time - most_recent
                    
                    # Check if within threshold
                    if time_since_last < time_threshold:
                        print(f"⏭️ Bỏ qua cảnh báo trùng lặp cho {row['Tên NE']} (Lần gửi gần nhất: {most_recent.strftime('%Y-%m-%d %H:%M:%S')})")
                        continue
            message = (
                f" <b>{'🔴🔴🗼Cảnh báo MLL trạm' if 'OOS' in str(row['N.Nhân']).upper() else '⚡⚡⚡ Cảnh báo mất AC'}</b>\n"
                f"<b>{row['Tên NE']}</b>/{row['Tên gợi nhớ']}\n"
                f"Cảnh báo: {row['N.Nhân']}\n" 
                f"Bắt đầu: {row['TG Sự cố']}\n"
                f"<b>Kéo dài: {row['Kéo dài']*60:.0f} phút</b>\n"
                f"{row['Phân Loại Trạm']}\n"
                f"Ghi chú: {row['Tỉnh ghi chú']}"
            )
            
            send_time = datetime.now()
            success = send_message(message)
            alerts_sent += 1
            
            # Log the sent message
            log_entry = {
                'Thời gian gửi': send_time,
                'Tên NE': row['Tên NE'],
                'Nội dung cảnh báo': row['N.Nhân'],
                'Trạng thái': 'Thành công' if success else 'Thất bại'
            }
            log_data.append(log_entry)

            if success:
                print(f"✅ Đã gửi cảnh báo {alerts_sent}/{total_alerts}")
            else:
                print(f"❌ Lỗi khi gửi cảnh báo {alerts_sent}/{total_alerts}")

        # Save log to Excel
        if log_data:
            log_df = pd.DataFrame(log_data)
            if not existing_log.empty:
                log_df = pd.concat([existing_log, log_df], ignore_index=True)
            log_df.to_excel(log_file, index=False)

        print(f"✅ Hoàn thành gửi cảnh báo lúc: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"📊 Tổng số cảnh báo đã gửi: {alerts_sent}/{total_alerts}")
        return True

    except Exception as e:
        print(f"❌ Lỗi khi xử lý file Excel: {str(e)}")
        return False

def send_file_report_summary(file_path: str = "report_summary.xlsx") -> bool:
    """
    Gửi file báo cáo tổng hợp qua Telegram
    """
    try:
        # Kiểm tra file tồn tại
        if not os.path.exists(file_path):
            print(f"❌ Không tìm thấy file {file_path}")
            return False
        # Chuẩn bị file để gửi
        files = {
            'document': open(file_path, 'rb')
        }

        # Gửi file qua Telegram API
        response = requests.post(
            f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendDocument',
            data={'chat_id': TELEGRAM_CHAT_ID_ALL},
            files=files
        )

        # Đóng file sau khi gửi
        files['document'].close()

        # Kiểm tra kết quả
        if response.status_code == 200:
            print(f"✅ Đã gửi file {file_path} thành công")
            return True
        else:
            print(f"❌ Lỗi khi gửi file: {response.text}")
            return False

    except Exception as e:
        print(f"❌ Lỗi khi gửi file: {str(e)}")
        return False

def send_latest_screenshot() -> bool:
    """
    Send the most recent screenshot from Screenshot_fms folder to Telegram
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Get absolute path to Screenshot_fms directory
        screenshot_dir = os.path.join(os.path.dirname(__file__), "Screenshot_fms")
        print(f"Looking for screenshots in: {screenshot_dir}")
        
        # Check if directory exists
        if not os.path.exists(screenshot_dir):
            print(f"❌ Directory not found: {screenshot_dir}")
            return False
            
        # Get list of PNG files in directory
        screenshots = glob.glob(os.path.join(screenshot_dir, "*.png"))
        
        if not screenshots:
            print("❌ No screenshots found")
            return False
            
        # Get most recent screenshot by modification time
        latest_screenshot = max(screenshots, key=os.path.getmtime)
        print(f"Found latest screenshot: {latest_screenshot}")
        
        # Verify file is readable
        if not os.access(latest_screenshot, os.R_OK):
            print(f"❌ Cannot read file: {latest_screenshot}")
            return False
            
        # Send the screenshot
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendPhoto"
        
        with open(latest_screenshot, 'rb') as photo_file:
            files = {
                'photo': photo_file
            }
            
            data = {
                "chat_id": TELEGRAM_CHAT_ID,
                "caption": f"📸 Latest FMS Screenshot ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')})"
            }
            
            response = requests.post(url, data=data, files=files)
            
            if response.status_code == 200:
                print(f"✅ Successfully sent screenshot: {latest_screenshot}")
                return True
            else:
                print(f"❌ Failed to send screenshot. Status code: {response.status_code}")
                print(f"Response: {response.text}")
                return False
            
    except Exception as e:
        print(f"❌ Error sending screenshot: {str(e)}")
        return False
    finally:
        if 'photo' in files:
            files['photo'].close()

if __name__ == "__main__":
    send_alerts_from_excel()
    send_file_report_summary()
    send_latest_screenshot()