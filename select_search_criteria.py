from playwright.sync_api import Page
import time

def select_search_criteria(page: Page) -> bool:
    """
    Xử lý việc chọn các tiêu chí tìm kiếm
    """
    try:
        # Click vào nút Tìm kiếm
        page.wait_for_selector('//*[@id="main"]/section[1]/div[1]/div[1]/div/button', timeout=30000)
        page.click('//*[@id="main"]/section[1]/div[1]/div[1]/div/button')
        time.sleep(1)  # Chờ 1 giây
        print("✅ Đã click vào phần tử Tìm kiếm")

        # Chọn các tiêu chí
        selectors = [
            '//*[@id="bodySearch"]/div[11]/div/div/span/div/button',
            '//*[@id="bodySearch"]/div[11]/div/div/span/div/ul/li[4]/a/label',
            '//*[@id="bodySearch"]/div[10]/div/div/span/div/button/span'
        ]
        
        for selector in selectors:
            page.wait_for_selector(selector, timeout=10000)
            page.click(selector)
            time.sleep(1)  # Chờ 1 giây sau mỗi click

        # Điền giá trị tìm kiếm đầu tiên: site_oos
        page.wait_for_selector('//*[@id="bodySearch"]/div[10]/div/div/span/div/ul/li[1]/div/input')
        page.fill('//*[@id="bodySearch"]/div[10]/div/div/span/div/ul/li[1]/div/input', 'MLL SITE')
        time.sleep(1)  # Chờ 1 giây sau khi điền giá trị

        # Chọn tickbox cho site_oos
        page.wait_for_selector('//*[@id="bodySearch"]/div[10]/div/div/span/div/ul/li[2]/a/label/input')
        page.click('//*[@id="bodySearch"]/div[10]/div/div/span/div/ul/li[2]/a/label/input')
        time.sleep(1)  # Chờ 1 giây sau khi chọn tickbox

        # Xóa trắng form để điền giá trị mới
        page.wait_for_selector('//*[@id="bodySearch"]/div[10]/div/div/span/div/ul/li[1]/div/input')
        page.fill('//*[@id="bodySearch"]/div[10]/div/div/span/div/ul/li[1]/div/input', '')
        time.sleep(1)  # Chờ 1 giây sau khi xóa trắng form

        # Điền giá trị tìm kiếm thứ hai: POWER_AC_EAS
        page.fill('//*[@id="bodySearch"]/div[10]/div/div/span/div/ul/li[1]/div/input', 'POWER_AC_EAS')
        time.sleep(1)  # Chờ 1 giây sau khi điền giá trị mới

        # Chọn tickbox cho site_oos
        page.wait_for_selector('//*[@id="bodySearch"]/div[10]/div/div/span/div/ul/li[2]/a/label/input')
        page.click('//*[@id="bodySearch"]/div[10]/div/div/span/div/ul/li[2]/a/label/input')
        time.sleep(1)  # Chờ 1 giây sau khi chọn tickbox

        # Xóa trắng form để điền giá trị mới
        page.wait_for_selector('//*[@id="bodySearch"]/div[10]/div/div/span/div/ul/li[1]/div/input')
        page.fill('//*[@id="bodySearch"]/div[10]/div/div/span/div/ul/li[1]/div/input', '')
        time.sleep(1)  # Chờ 1 giây sau khi xóa trắng form

        # Điền giá trị tìm kiếm thứ hai: SITE_OOS
        page.fill('//*[@id="bodySearch"]/div[10]/div/div/span/div/ul/li[1]/div/input', 'SITE_OOS')
        time.sleep(1)  # Chờ 1 giây sau khi điền giá trị mới

        # Chọn tickbox cho site_oos
        page.wait_for_selector('//*[@id="bodySearch"]/div[10]/div/div/span/div/ul/li[2]/a/label/input')
        page.click('//*[@id="bodySearch"]/div[10]/div/div/span/div/ul/li[2]/a/label/input')
        time.sleep(1)  # Chờ 1 giây sau khi chọn tickbox


        # chọn các cột cần hiển thị trong báo cao
        # Chọn các cột hiển thị trong báo cáo
        page.wait_for_selector('//*[@id="tblBox"]/div/div[1]/div/div[3]/span/div/button/span', timeout=10000)
        page.click('//*[@id="tblBox"]/div/div[1]/div/div[3]/span/div/button/span')
        time.sleep(1)  # Chờ 1 giây sau khi click

        # Chọn tickbox cho các cột hiển thị
        page.wait_for_selector('//*[@id="tblBox"]/div/div[1]/div/div[3]/span/div/ul/li[2]/a/label/input', timeout=10000)
        page.click('//*[@id="tblBox"]/div/div[1]/div/div[3]/span/div/ul/li[2]/a/label/input')
        time.sleep(1)  # Chờ 1 giây sau khi chọn tickbox

        # Tìm và điền giá trị "Tên NE" vào ô tìm kiếm
        page.wait_for_selector('//*[@id="tblBox"]/div/div[1]/div/div[3]/span/div/ul/li[1]/div/input')
        page.fill('//*[@id="tblBox"]/div/div[1]/div/div[3]/span/div/ul/li[1]/div/input', 'Tên NE')
        time.sleep(1)  # Chờ 1 giây sau khi điền giá trị

        # Chọn tickbox cho "Tên NE"
        page.wait_for_selector('//*[@id="tblBox"]/div/div[1]/div/div[3]/span/div/ul/li[8]/a/label/input', timeout=10000)
        page.click('//*[@id="tblBox"]/div/div[1]/div/div[3]/span/div/ul/li[8]/a/label/input')
        time.sleep(1)  # Chờ 1 giây sau khi chọn tickbox

        # Xóa trắng ô tìm kiếm
        page.wait_for_selector('//*[@id="tblBox"]/div/div[1]/div/div[3]/span/div/ul/li[1]/div/input')
        page.fill('//*[@id="tblBox"]/div/div[1]/div/div[3]/span/div/ul/li[1]/div/input', '')
        time.sleep(1)  # Chờ 1 giây sau khi xóa trắng form
        # Tìm và điền giá trị "Tên gợi nhớ" vào ô tìm kiếm
        page.wait_for_selector('//*[@id="tblBox"]/div/div[1]/div/div[3]/span/div/ul/li[1]/div/input')
        page.fill('//*[@id="tblBox"]/div/div[1]/div/div[3]/span/div/ul/li[1]/div/input', 'Tên gợi nhớ')
        time.sleep(1)  # Chờ 1 giây sau khi điền giá trị

        # Chọn tickbox cho "Tên gợi nhớ"
        page.wait_for_selector('//*[@id="tblBox"]/div/div[1]/div/div[3]/span/div/ul/li[9]/a/label/input', timeout=10000)
        page.click('//*[@id="tblBox"]/div/div[1]/div/div[3]/span/div/ul/li[9]/a/label/input')
        time.sleep(1)  # Chờ 1 giây sau khi chọn tickbox

        # Xóa trắng ô tìm kiếm
        page.wait_for_selector('//*[@id="tblBox"]/div/div[1]/div/div[3]/span/div/ul/li[1]/div/input')
        page.fill('//*[@id="tblBox"]/div/div[1]/div/div[3]/span/div/ul/li[1]/div/input', '')
        time.sleep(1)  # Chờ 1 giây sau khi xóa trắng form
        # Tìm và điền giá trị "N.Nhân" vào ô tìm kiếm
        page.wait_for_selector('//*[@id="tblBox"]/div/div[1]/div/div[3]/span/div/ul/li[1]/div/input')
        page.fill('//*[@id="tblBox"]/div/div[1]/div/div[3]/span/div/ul/li[1]/div/input', 'N.Nhân')
        time.sleep(1)  # Chờ 1 giây sau khi điền giá trị

        # Chọn tickbox cho "N.Nhân"
        page.wait_for_selector('//*[@id="tblBox"]/div/div[1]/div/div[3]/span/div/ul/li[12]/a/label/input', timeout=10000)
        page.click('//*[@id="tblBox"]/div/div[1]/div/div[3]/span/div/ul/li[12]/a/label/input')
        time.sleep(1)  # Chờ 1 giây sau khi chọn tickbox

        # Xóa trắng ô tìm kiếm
        page.wait_for_selector('//*[@id="tblBox"]/div/div[1]/div/div[3]/span/div/ul/li[1]/div/input')
        page.fill('//*[@id="tblBox"]/div/div[1]/div/div[3]/span/div/ul/li[1]/div/input', '')
        time.sleep(1)  # Chờ 1 giây sau khi xóa trắng form

        # Tìm và điền giá trị "TG Sự cố" vào ô tìm kiếm
        page.wait_for_selector('//*[@id="tblBox"]/div/div[1]/div/div[3]/span/div/ul/li[1]/div/input')
        page.fill('//*[@id="tblBox"]/div/div[1]/div/div[3]/span/div/ul/li[1]/div/input', 'TG Sự cố')
        time.sleep(1)  # Chờ 1 giây sau khi điền giá trị

        # Chọn tickbox cho "TG Sự cố"
        page.wait_for_selector('//*[@id="tblBox"]/div/div[1]/div/div[3]/span/div/ul/li[14]/a/label/input', timeout=10000)
        page.click('//*[@id="tblBox"]/div/div[1]/div/div[3]/span/div/ul/li[14]/a/label/input')
        time.sleep(1)  # Chờ 1 giây sau khi chọn tickbox

        # Xóa trắng ô tìm kiếm
        page.wait_for_selector('//*[@id="tblBox"]/div/div[1]/div/div[3]/span/div/ul/li[1]/div/input')
        page.fill('//*[@id="tblBox"]/div/div[1]/div/div[3]/span/div/ul/li[1]/div/input', '')
        time.sleep(1)  # Chờ 1 giây sau khi xóa trắng form

        # Tìm và điền giá trị "TG CLR" vào ô tìm kiếm
        page.wait_for_selector('//*[@id="tblBox"]/div/div[1]/div/div[3]/span/div/ul/li[1]/div/input')
        page.fill('//*[@id="tblBox"]/div/div[1]/div/div[3]/span/div/ul/li[1]/div/input', 'TG CLR')
        time.sleep(1)  # Chờ 1 giây sau khi điền giá trị

        # Chọn tickbox cho "TG CLR"
        page.wait_for_selector('//*[@id="tblBox"]/div/div[1]/div/div[3]/span/div/ul/li[15]/a/label/input', timeout=10000)
        page.click('//*[@id="tblBox"]/div/div[1]/div/div[3]/span/div/ul/li[15]/a/label/input')
        time.sleep(1)  # Chờ 1 giây sau khi chọn tickbox

        # Xóa trắng ô tìm kiếm
        page.wait_for_selector('//*[@id="tblBox"]/div/div[1]/div/div[3]/span/div/ul/li[1]/div/input')
        page.fill('//*[@id="tblBox"]/div/div[1]/div/div[3]/span/div/ul/li[1]/div/input', '')
        time.sleep(1)  # Chờ 1 giây sau khi xóa trắng form

        # Tìm và điền giá trị "TG C.Báo" vào ô tìm kiếm
        page.wait_for_selector('//*[@id="tblBox"]/div/div[1]/div/div[3]/span/div/ul/li[1]/div/input')
        page.fill('//*[@id="tblBox"]/div/div[1]/div/div[3]/span/div/ul/li[1]/div/input', 'TG C.Báo')
        time.sleep(1)  # Chờ 1 giây sau khi điền giá trị

        # Chọn tickbox cho "TG C.Báo"
        page.wait_for_selector('//*[@id="tblBox"]/div/div[1]/div/div[3]/span/div/ul/li[16]/a/label/input', timeout=10000)
        page.click('//*[@id="tblBox"]/div/div[1]/div/div[3]/span/div/ul/li[16]/a/label/input')
        time.sleep(1)  # Chờ 1 giây sau khi chọn tickbox

        # Xóa trắng ô tìm kiếm
        page.wait_for_selector('//*[@id="tblBox"]/div/div[1]/div/div[3]/span/div/ul/li[1]/div/input')
        page.fill('//*[@id="tblBox"]/div/div[1]/div/div[3]/span/div/ul/li[1]/div/input', '')
        time.sleep(1)  # Chờ 1 giây sau khi xóa trắng form

        # Tìm và điền giá trị "Tỉnh ghi chú" vào ô tìm kiếm
        page.wait_for_selector('//*[@id="tblBox"]/div/div[1]/div/div[3]/span/div/ul/li[1]/div/input')
        page.fill('//*[@id="tblBox"]/div/div[1]/div/div[3]/span/div/ul/li[1]/div/input', 'Tỉnh ghi chú')
        time.sleep(1)  # Chờ 1 giây sau khi điền giá trị

        # Chọn tickbox cho "Tỉnh ghi chú"
        page.wait_for_selector('//*[@id="tblBox"]/div/div[1]/div/div[3]/span/div/ul/li[24]/a/label/input', timeout=10000)
        page.click('//*[@id="tblBox"]/div/div[1]/div/div[3]/span/div/ul/li[24]/a/label/input')
        time.sleep(1)  # Chờ 1 giây sau khi chọn tickbox

        # Xóa trắng ô tìm kiếm
        page.wait_for_selector('//*[@id="tblBox"]/div/div[1]/div/div[3]/span/div/ul/li[1]/div/input')
        page.fill('//*[@id="tblBox"]/div/div[1]/div/div[3]/span/div/ul/li[1]/div/input', '')
        time.sleep(1)  # Chờ 1 giây sau khi xóa trắng form

        # Tìm và điền giá trị "Phân Loại Trạm" vào ô tìm kiếm
        page.wait_for_selector('//*[@id="tblBox"]/div/div[1]/div/div[3]/span/div/ul/li[1]/div/input')
        page.fill('//*[@id="tblBox"]/div/div[1]/div/div[3]/span/div/ul/li[1]/div/input', 'Phân Loại Trạm')
        time.sleep(1)  # Chờ 1 giây sau khi điền giá trị

        # Chọn tickbox cho "Phân Loại Trạm"
        page.wait_for_selector('//*[@id="tblBox"]/div/div[1]/div/div[3]/span/div/ul/li[29]/a/label/input', timeout=10000)
        page.click('//*[@id="tblBox"]/div/div[1]/div/div[3]/span/div/ul/li[29]/a/label/input')
        time.sleep(1)  # Chờ 1 giây sau khi chọn tickbox




        # Xóa trắng ô tìm kiếm
        page.wait_for_selector('//*[@id="tblBox"]/div/div[1]/div/div[3]/span/div/ul/li[1]/div/input')
        page.fill('//*[@id="tblBox"]/div/div[1]/div/div[3]/span/div/ul/li[1]/div/input', '')
        time.sleep(1)  # Chờ 1 giây sau khi xóa trắng form

        # Tìm và điền giá trị "Quận/Huyện" vào ô tìm kiếm
        page.wait_for_selector('//*[@id="tblBox"]/div/div[1]/div/div[3]/span/div/ul/li[1]/div/input')
        page.fill('//*[@id="tblBox"]/div/div[1]/div/div[3]/span/div/ul/li[1]/div/input', 'Quận/Huyện')
        time.sleep(1)  # Chờ 1 giây sau khi điền giá trị

        # Chọn tickbox cho "Quận/Huyện"
        page.wait_for_selector('//*[@id="tblBox"]/div/div[1]/div/div[3]/span/div/ul/li[22]/a/label/input', timeout=10000)
        page.click('//*[@id="tblBox"]/div/div[1]/div/div[3]/span/div/ul/li[22]/a/label/input')
        time.sleep(1)  # Chờ 1 giây sau khi chọn tickbox





        return True
    except Exception as e:
        print(f"❌ Lỗi khi chọn tiêu chí tìm kiếm: {e}")
        return False