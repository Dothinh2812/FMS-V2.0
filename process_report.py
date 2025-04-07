import pandas as pd
from datetime import datetime

def process_report(input_file: str = "fms_data.xlsx", output_file: str = "report_summary.xlsx") -> bool:
    """
    Xử lý dữ liệu từ file fms_data và tạo báo cáo tổng hợp với thời gian kéo dài
    """
    
    try:
        # Đọc file input
        df = pd.read_excel(input_file)
        
        # Chọn các cột cần thiết
        selected_columns = ['Tên NE', 'Tên gợi nhớ', 'N.Nhân', 'TG Sự cố', 'Tỉnh ghi chú', 'Phân Loại Trạm', 'Quận/Huyện']
        df_report = df[selected_columns].copy()
        
        # Lọc dữ liệu theo Quận/Huyện
        filtered_districts = ['Phúc Thọ', 'Sơn Tây', 'Thạch Thất', 'Đan Phượng', 'Ba Vì']
        df_report = df_report[df_report['Quận/Huyện'].isin(filtered_districts)]
        
        # Chuyển cột TG Sự cố sang định dạng datetime
        df_report['TG Sự cố'] = pd.to_datetime(df_report['TG Sự cố'], format='%d/%m/%Y %H:%M:%S', errors='coerce')
        
        # Tính thời gian kéo dài
        current_time = datetime.now()
        df_report['Kéo dài'] = df_report['TG Sự cố'].apply(
            lambda x: round((current_time - x).total_seconds() / 3600, 2) if pd.notnull(x) else 0
        )
        
        # Thay thế các giá trị NaN bằng chuỗi rỗng
        df_report = df_report.fillna('')
        
        # Xuất ra file Excel mới
        with pd.ExcelWriter(output_file, engine='xlsxwriter', engine_kwargs={'options': {'nan_inf_to_errors': True}}) as writer:
            # Chuyển đổi cột TG Sự cố về định dạng chuỗi trước khi xuất ra Excel
            df_report_excel = df_report.copy()
            df_report_excel['TG Sự cố'] = df_report['TG Sự cố'].dt.strftime('%d/%m/%Y %H:%M:%S')
            
            df_report_excel.to_excel(writer, sheet_name='Report', index=False)
            
            # Định dạng workbook
            workbook = writer.book
            worksheet = writer.sheets['Report']
            
            # Định dạng header
            header_format = workbook.add_format({
                'bold': True,
                'text_wrap': True,
                'valign': 'vcenter',
                'align': 'center',
                'bg_color': '#D9E1F2',
                'border': 1
            })
            
            # Định dạng dữ liệu
            data_format = workbook.add_format({
                'text_wrap': True,
                'valign': 'vcenter',
                'align': 'left',
                'border': 1
            })
            
            # Định dạng số giờ
            time_format = workbook.add_format({
                'num_format': '0.00',
                'valign': 'vcenter',
                'align': 'right',
                'border': 1
            })
            
            # Định dạng ngày tháng
            date_format = workbook.add_format({
                'text_wrap': True,
                'valign': 'vcenter',
                'align': 'center',
                'border': 1
            })
            
            # Áp dụng định dạng cho header
            for col_num, value in enumerate(df_report_excel.columns):
                worksheet.write(0, col_num, value, header_format)
            
            # Áp dụng định dạng cho dữ liệu
            for row in range(len(df_report_excel)):
                for col in range(len(df_report_excel.columns)):
                    value = df_report_excel.iloc[row, col]
                    if pd.isna(value):  # Kiểm tra giá trị NaN
                        value = ''
                    if col == len(df_report_excel.columns) - 2:  # Cột Kéo dài
                        worksheet.write(row + 1, col, value, time_format)
                    elif df_report_excel.columns[col] == 'TG Sự cố':  # Cột TG Sự cố
                        worksheet.write(row + 1, col, value, date_format)
                    else:
                        worksheet.write(row + 1, col, value, data_format)
            
            # Tự động điều chỉnh độ rộng cột
            for i, col in enumerate(df_report_excel.columns):
                max_length = max(
                    df_report_excel[col].astype(str).apply(len).max(),
                    len(str(col))
                )
                worksheet.set_column(i, i, max_length + 2)

        print(f"✅ Đã tạo file báo cáo: {output_file}")
        return True

    except Exception as e:
        print(f"❌ Lỗi khi xử lý báo cáo: {str(e)}")
        return False