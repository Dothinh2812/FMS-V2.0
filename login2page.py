from playwright.sync_api import Page
import time

def login2page(p):
    """
    Initialize and login to both FMS and Zalo browsers
    """
    # Launch the second browser for chat.zalo.me
    browser2 = p.chromium.launch(headless=False)
    context2 = browser2.new_context()
    zalo = context2.new_page()
    print("Opening chat.zalo.me in the second browser...")
    zalo.goto("https://chat.zalo.me")
    time.sleep(5)  # Wait for QR code scan

    # Launch the first browser for fms.vnpt.vn
    browser1 = p.chromium.launch(headless=False)
    context1 = browser1.new_context()
    fms = context1.new_page()
    print("Opening fms.vnpt.vn in the first browser...")
    
    # Handle login process
    try:
        fms.goto("https://fms.vnpt.vn")
        fms.wait_for_selector("input[name='username']")
        
        # Fill login credentials
        fms.fill("input[name='username']", "thinhdx.hni")  # Replace with actual username
        fms.fill("input[name='password']", "T#g6542u")  # Replace with actual password
        fms.click("button[type='submit']")
        
        print("✅ Login credentials submitted. Waiting for OTP input...")
        time.sleep(10)  # Wait for OTP input
        
    except Exception as e:
        print(f"❌ Login error: {e}")
    
    return browser1, browser2, fms, zalo