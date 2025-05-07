from playwright.sync_api import Page
import time

def perform_search(fms: Page) -> bool:
    """
    Performs search operations on the FMS page by clicking specific buttons and handling alerts
    """
    try:
        # Wait for page to be fully loaded
        fms.wait_for_load_state("networkidle")
        
        # Click the refresh alerts button
        search_button = fms.wait_for_selector('//*[@id="btnSearch"]', timeout=10000)
        if not search_button:
            print("⚠️ Refresh alerts button not found")
            return False
            
        search_button.click()
        print("✅ Successfully clicked refresh alerts button")
        
        # Wait for data to load using network idle instead of sleep
        fms.wait_for_load_state("networkidle", timeout=10000)
        print("✅ Data loading completed")
        
        # Check if any error messages or alerts appear
        error_message = fms.query_selector('.error-message')
        if error_message:
            print(f"⚠️ Error message detected: {error_message.text_content()}")
            return False
            
        # Thêm thời gian chờ để đảm bảo trang đã load hoàn toàn
        time.sleep(10)
        
        try:
            # Take screenshot with increased timeout and specific options
            timestamp = time.strftime("%Y%m%d-%H%M%S")
            screenshot_path = f"Screenshot_fms/search_result_{timestamp}.png"
            fms.screenshot(
                path=screenshot_path,
                timeout=60000,  # Tăng timeout lên 60 giây
                type='jpeg',    # Sử dụng định dạng JPEG thay vì PNG
                quality=80,     # Giảm chất lượng ảnh để tăng tốc độ
                animations='disabled'  # Tắt animations
            )
            print(f"✅ Screenshot saved to {screenshot_path}")
        except Exception as screenshot_error:
            print(f"⚠️ Screenshot failed but continuing execution: {screenshot_error}")
            # Tiếp tục thực thi ngay cả khi screenshot thất bại
            
        return True

    except Exception as e:
        print(f"❌ Error during search operation: {e}")
        return False