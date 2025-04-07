from playwright.sync_api import sync_playwright, Page
import time
import schedule
from login2page import login2page
from select_search_criteria import select_search_criteria
from chay_dinh_ky_lap_lai import chay_dinh_ky_lap_lai

def main():
    with sync_playwright() as p:
        try:
            browser1, browser2, fms, zalo = login2page(p)
            time.sleep(10)

            if not select_search_criteria(fms):
                print("❌ Không thể chọn tiêu chí tìm kiếm. Dừng chương trình.")
                return

            # Run the periodic task once immediately when starting
            chay_dinh_ky_lap_lai(fms, zalo)

            # Schedule to run every 3 minutes
            schedule.every(3).minutes.do(lambda: chay_dinh_ky_lap_lai(fms, zalo))
            print("✅ Scheduled task to run every 3 minutes")

            while True:
                schedule.run_pending()
                time.sleep(1)

        except KeyboardInterrupt:
            print("Closing browsers...")
        finally:
            browser1.close()
            browser2.close()

if __name__ == "__main__":
    main()