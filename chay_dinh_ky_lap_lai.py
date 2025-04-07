from playwright.sync_api import Page
from datetime import datetime
import traceback
from perform_search import perform_search
from extract_slickgrid_data import extract_slickgrid_data
from process_report import process_report
from send_zalo_theo_huyen import send_zalo_theo_huyen
from send_tele import send_alerts_from_excel, send_file_report_summary

def chay_dinh_ky_lap_lai(fms: Page, zalo: Page) -> None:
    """
    Executes periodic tasks in sequence:
    1. Perform search
    2. Extract data to Excel
    3. Process report
    4. Send Zalo messages
    """
    try:
        print("\n=== Starting periodic execution ===")
        print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        # Step 1: Perform search
        if not perform_search(fms):
            print("❌ Search failed, skipping remaining steps")
            return

        # Step 2: Extract data to Excel
        output_file = "fms_data.xlsx"
        if not extract_slickgrid_data(fms, output_file):
            print("❌ Data extraction failed, skipping remaining steps")
            return

        # Step 3: Process report
        if not process_report("fms_data.xlsx", "report_summary.xlsx"):
            print("❌ Report processing failed, skipping remaining steps")
            return

        # Step 4: Send Zalo messages
        if not send_zalo_theo_huyen(zalo):
            print("❌ Zalo message sending failed")
            return

        # Step 5: Send alerts from Excel
        if not send_alerts_from_excel():
            print("❌ Sending alerts from Excel failed")
            return

        # Step 6: Send report summary file
        if not send_file_report_summary():
            print("❌ Sending report summary file failed")
            return

        print("✅ Periodic execution completed successfully")
        print("=== End of periodic execution ===\n")

    except Exception as e:
        print(f"❌ Error during periodic execution: {str(e)}")
        traceback.print_exc()