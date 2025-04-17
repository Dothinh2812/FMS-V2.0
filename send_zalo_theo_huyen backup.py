from playwright.sync_api import Page
import pandas as pd
import time
import os
from datetime import datetime

def send_zalo_theo_huyen(page: Page) -> bool:
    """
    Sends Zalo messages based on district information from report_summary.xlsx
    with filtering conditions and logging functionality
    """
    try:
        current_time = datetime.now()
        print(f"\n🕒 Starting Zalo message check at: {current_time.strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Create log directory if it doesn't exist
        log_dir = "log_message"
        os.makedirs(log_dir, exist_ok=True)
        log_file = os.path.join(log_dir, "zalo_log.xlsx")

        # Look for report_summary.xlsx
        report_file = 'report_summary.xlsx'
        if not os.path.exists(report_file):
            print("❌ report_summary.xlsx not found!")
            return False
            
        print(f"Reading file: {report_file}")
        
        # Read data
        df = pd.read_excel(report_file)
        
        if df.empty:
            print("ℹ️ No data in report file!")
            return False

        # Filter alerts based on conditions
        df_filtered = df[
            ((df['N.Nhân'].str.contains('OOS', case=False, na=False)) |
             (df['N.Nhân'].str.contains('AC', case=False, na=False) & (df['Kéo dài'] > 0.5))) &
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
            print("ℹ️ No alerts to send")
            return True

        print(f"📊 Number of alerts to check: {total_alerts}")
        
        # Wait for Zalo chat to load
        time.sleep(2)
        
        # Check if we're on Zalo chat page
        if "chat.zalo.me" not in page.url:
            print("⏳ Waiting for manual Zalo login...")
            page.wait_for_url("**/chat.zalo.me/**", timeout=300000)
            print("✅ Successfully logged into Zalo")
        
        # Search for group chat
        search_input = page.locator('input#contact-search-input')
        search_input.click()
        search_input.fill("")
        search_input.fill("TEST-ZALO-AUTO")
        time.sleep(3)
        search_input.press("Enter")
        time.sleep(3)

        # Prepare log data
        log_data = []
        alerts_sent = 0
        
        # Process each filtered record
        for index, row in df_filtered.iterrows():
            try:
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
                            print(f"⏭️ Skipping duplicate alert for {row['Tên NE']} (Last sent: {most_recent.strftime('%Y-%m-%d %H:%M:%S')})")
                            continue

                # Prepare message header based on district
                header = "🔴 Cảnh báo sự cố kéo dài"
                if pd.notna(row['Quận/Huyện']):
                    if row['Quận/Huyện'] == "Ba Vì":
                        header = "🔴 Cảnh báo sự cố kéo dài Ba Vì @0914383384"
                    elif row['Quận/Huyện'] == "Phúc Thọ":
                        header = "🔴 Cảnh báo sự cố kéo dài Phúc Thọ @0919519218"
                    elif row['Quận/Huyện'] == "Sơn Tây":
                        header = "🔴 Cảnh báo sự cố kéo dài Sơn Tây @0917680203"
                    elif row['Quận/Huyện'] == "Thạch Thất":
                        header = "🔴 Cảnh báo sự cố kéo dài Thạch Thất @0945748188"
                    elif row['Quận/Huyện'] == "Đan Phượng":
                        header = "🔴 Cảnh báo sự cố kéo dài Đan Phượng @0945548859"
                
                # Format duration
                duration = row.get('Kéo dài', 0)
                if isinstance(duration, (int, float)):
                    duration_str = f"{duration:.2f}"
                else:
                    duration_str = str(duration)
                
                # Prepare message
                message = (
                    f"{header}\n"
                    f"{row.get('Tên NE', 'N/A')}/{row.get('Tên gợi nhớ', 'N/A')}\n"
                    f"Cảnh báo: {row.get('N.Nhân', 'N/A')}\n"
                    f"Bắt đầu: {row.get('TG Sự cố', 'N/A')}\n"
                    f"Kéo dài: {duration_str} giờ\n"
                    f"{row.get('Phân Loại Trạm', 'N/A')}\n"
                    f"Ghi chú: {row.get('Tỉnh ghi chú', 'N/A')}"
                )
                
                # Find message input and send message
                message_input = page.locator('div#input_line_0')
                message_input.fill(message)
                time.sleep(2)
                
                # Click send button
                send_button = page.locator('//*[@id="chat-input-container-id"]/div[2]/div[2]/div[2]/i')
                send_button.click()
                
                send_time = datetime.now()
                alerts_sent += 1

                # Log the sent message
                log_entry = {
                    'Thời gian gửi': send_time,
                    'Tên NE': row['Tên NE'],
                    'Nội dung cảnh báo': row['N.Nhân'],
                    'Trạng thái': 'Thành công'
                }
                log_data.append(log_entry)
                
                time.sleep(2)
                print(f"✅ Sent message {alerts_sent}/{total_alerts}")
                
            except Exception as e:
                print(f"❌ Error processing record {alerts_sent + 1}: {str(e)}")
                # Log failed message
                log_entry = {
                    'Thời gian gửi': datetime.now(),
                    'Tên NE': row['Tên NE'],
                    'Nội dung cảnh báo': row['N.Nhân'],
                    'Trạng thái': 'Thất bại'
                }
                log_data.append(log_entry)

        # Save log to Excel
        if log_data:
            log_df = pd.DataFrame(log_data)
            if not existing_log.empty:
                log_df = pd.concat([existing_log, log_df], ignore_index=True)
            log_df.to_excel(log_file, index=False)

        print(f"✅ Completed sending alerts at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"📊 Total alerts sent: {alerts_sent}/{total_alerts}")
        return True
        
    except Exception as e:
        print(f"❌ Error in send_zalo_theo_huyen: {str(e)}")
        return False