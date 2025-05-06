import requests
import os
from typing import Union, Optional, Tuple
import glob
import pandas as pd
from datetime import datetime

def payload_prepare(excel_file: str = "report_summary.xlsx") -> list[Tuple[str, str]]:
    """
    Read data from Excel and prepare payloads for webhook messages.
    
    Args:
        excel_file (str): Path to Excel file
        
    Returns:
        list[Tuple[str, str]]: List of (group_name, formatted_message) tuples
    """
    try:
        # Read Excel file
        df = pd.read_excel(excel_file)
        
        # Filter alerts based on conditions
        df_filtered = df[
            ((df['N.Nhân'].str.contains('OOS', case=False, na=False)) |
             (df['N.Nhân'].str.contains('AC', case=False, na=False) & (df['Kéo dài'] > 0.5))) &
            (df['Phân Loại Trạm'] != 'Trạm viễn thông loại 3')
        ]

        payloads = []
        
        # Process each row
        for _, row in df_filtered.iterrows():
            # Determine group based on district
            district = row.get('Quận/Huyện', 'Unknown')
            group_name = "TEST-ZALO-AUTO"  # Default group
            
            if district == "Ba Vì":
                group_name = "GS vận hành MFĐ BVI-KTĐH"
            elif district == "Phúc Thọ":
                group_name = "GS vận hành MFĐ PTO-KTĐH"
            elif district == "Thạch Thất":
                group_name = "GS vận hành MFĐ-BTS -TTT-KTĐH"
            elif district == "Đan Phượng":
                group_name = "GS vận hành MFĐ ĐPG-KTĐH"
            elif district == "Sơn Tây":
                group_name = "GS vận hành MFĐ STY-KTĐH"

            # Prepare message header based on district
            # header = "🔴 Cảnh báo sự cố kéo dài"
            # if pd.notna(district):
            #     if district == "Ba Vì":
            #         header = "🔴 Cảnh báo sự cố Ba Vì"
            #     elif district == "Phúc Thọ":
            #         header = "🔴 Cảnh báo sự cố Phúc Thọ"
            #     elif district == "Sơn Tây":
            #         header = "🔴 Cảnh báo sự cố Sơn Tây"
            #     elif district == "Thạch Thất":
            #         header = "🔴 Cảnh báo sự cố Thạch Thất"
            #     elif district == "Đan Phượng":
            #         header = "🔴 Cảnh báo sự cố Đan Phượng"

            # Format duration
            duration = row.get('Kéo dài', 0)
            duration_str = f"{float(duration):.2f}" if isinstance(duration, (int, float)) else str(duration)

            # Format message
            message = (
                f"🔴 Cảnh báo 🔴\n"
                f"{row.get('Tên NE', 'N/A')}/{row.get('Tên gợi nhớ', 'N/A')}\n"
                f"Cảnh báo: {row.get('N.Nhân', 'N/A')}\n"
                f"Bắt đầu: {row.get('TG Sự cố', 'N/A')}\n"
                f"Kéo dài: {duration_str} giờ\n"
                f"{row.get('Phân Loại Trạm', 'N/A')}\n"
                f"Ghi chú: {row.get('Tỉnh ghi chú', 'N/A')}"
            )

            payloads.append((group_name, message))

        return payloads

    except Exception as e:
        print(f"❌ Error preparing payloads: {str(e)}")
        return []

def send_message(message: str, group_name: str) -> bool:
    """
    Send message to webhook endpoint.
    
    Args:
        message (str): Message content to send
        group_name (str): Name of the target group
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        webhook_url = "http://127.0.0.1:5000/webhook"
        payload = {
            "group": group_name,
            "message": message
        }
        
        response = requests.post(webhook_url, json=payload)
        if response.status_code == 200:
            print(f"✅ Successfully sent message to webhook for group: {group_name}")
            return True
        else:
            print(f"❌ Failed to send message. Status code: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error sending message to webhook: {str(e)}")
        return False

if __name__ == "__main__":
    # Get all payloads from Excel
    payloads = payload_prepare()
    
    # Send messages for each payload
    for group, message in payloads:
        print(f"\nSending to group: {group}")
        print(f"Message: {message}\n")
        send_message(message, group)