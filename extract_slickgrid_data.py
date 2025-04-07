from playwright.sync_api import Page
import time
import pandas as pd
from bs4 import BeautifulSoup
import traceback

def extract_slickgrid_data(page: Page, output_file: str) -> bool:
    """
    Trích xuất dữ liệu từ Slick Grid và lưu vào file Excel
    """
    try:
        # Đợi grid load xong
        page.wait_for_selector('.slick-cell', timeout=30000)
        time.sleep(2)  # Đợi dữ liệu load hoàn toàn

        # Định nghĩa headers cần lấy
        expected_headers = [
            'STT', 'Chuông', 'TT', 'Mức', 'Loại NE', 'Tên NE', 
            'Tên gợi nhớ', 'Object', 'BSC/RNC', 'N.Nhân', 
            'Nhà CC', 'TG Sự cố', 'TG CLR', 'TG C.Báo',
            'TG Giảm Trừ', 'T.thái CLR', 'Mã C.Báo', 'Chi tiết',
            'Tỉnh/TP', 'Quận/Huyện', 'VNP.Ghi chú', 'Tỉnh ghi chú',
            'Loại sự cố', 'Time AC', 'Địa Chỉ NE', 'Đơn Vị Quản Lý',
            'Phân Loại Trạm', 'H.Thống', 'TG Tạo Trên FM'
        ]

        # Lấy và parse HTML
        html_content = page.content()
        soup = BeautifulSoup(html_content, 'html.parser')

        # Tìm tất cả các header cells
        header_cells = soup.find_all('div', class_='slick-header-column')
        if not header_cells:
            print("❌ Không tìm thấy headers")
            return False

        # Lấy text của headers và tìm index của các cột cần thiết
        header_texts = [cell.get_text(strip=True) for cell in header_cells]
        
        # In ra tất cả các header thực tế để debug
        print("Headers thực tế trong trang:")
        for idx, header in enumerate(header_texts):
            print(f"{idx}: {header}")

        # Lấy tất cả các cột có trong grid, không chỉ giới hạn ở expected_headers
        column_indices = {}
        for idx, header in enumerate(header_texts):
            column_indices[idx] = header
            if header not in expected_headers:
                expected_headers.append(header)
                print(f"✅ Đã thêm cột mới: {header}")

        if not column_indices:
            print("❌ Không tìm thấy cột nào phù hợp")
            return False

        # Tìm tất cả các hàng trong grid
        rows = soup.find_all('div', class_='slick-row')
        if not rows:
            print("Hiện không còn cảnh báo nào!")
            return False

        # Kiểm tra xem có dữ liệu thực sự trong các hàng không
        data_found = False
        for row in rows:
            cells = row.find_all('div', class_='slick-cell')
            if cells and any(cell.get_text(strip=True) for cell in cells):
                data_found = True
                break
                
        if not data_found:
            print("Hiện không còn cảnh báo nào!")
            return False

        # Chuẩn bị dữ liệu cho DataFrame
        data = []
        for row in rows:
            cells = row.find_all('div', class_='slick-cell')
            if cells:
                row_data = {}
                for idx, header_name in column_indices.items():
                    if idx < len(cells):
                        cell_text = cells[idx].get_text(strip=True)
                        row_data[header_name] = cell_text
                    else:
                        row_data[header_name] = ''
                data.append(row_data)

        # Tạo DataFrame
        df = pd.DataFrame(data)
        
        # Đảm bảo tất cả các cột mong muốn đều có trong DataFrame
        for header in expected_headers:
            if header not in df.columns:
                df[header] = ''

        # Sắp xếp các cột theo thứ tự mong muốn
        # Chỉ sắp xếp các cột có trong expected_headers
        available_headers = [h for h in expected_headers if h in df.columns]
        df = df[available_headers]

        # Định dạng và xuất ra file Excel
        with pd.ExcelWriter(output_file, engine='xlsxwriter') as writer:
            df.to_excel(writer, sheet_name='Data', index=False)
            
            # Lấy workbook và worksheet để định dạng
            workbook = writer.book
            worksheet = writer.sheets['Data']

            # Định dạng header
            header_format = workbook.add_format({
                'bold': True,
                'text_wrap': True,
                'valign': 'vcenter',
                'align': 'center',
                'bg_color': '#D9E1F2',
                'border': 1
            })

            # Định dạng các cột dữ liệu
            data_format = workbook.add_format({
                'text_wrap': True,
                'valign': 'vcenter',
                'align': 'left',
                'border': 1
            })

            # Áp dụng định dạng cho header
            for col_num, value in enumerate(df.columns):
                worksheet.write(0, col_num, value, header_format)

            # Áp dụng định dạng cho dữ liệu
            for row in range(len(df)):
                for col in range(len(df.columns)):
                    worksheet.write(row + 1, col, df.iloc[row, col], data_format)

            # Tự động điều chỉnh độ rộng cột
            for i, col in enumerate(df.columns):
                max_length = max(
                    df[col].astype(str).apply(len).max(),
                    len(str(col))
                )
                worksheet.set_column(i, i, max_length + 2)

        print(f"✅ Đã lưu dữ liệu vào file {output_file}")
        print(f"✅ Số cột đã trích xuất: {len(df.columns)}")
        print(f"✅ Số dòng đã trích xuất: {len(df)}")
        return True

    except Exception as e:
        print(f"❌ Lỗi khi trích xuất dữ liệu: {e}")
        traceback.print_exc()  # In ra chi tiết lỗi để debug
        return False