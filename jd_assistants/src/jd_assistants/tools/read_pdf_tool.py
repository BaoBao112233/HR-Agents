from langchain_core.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
import fitz
import pdfplumber
import re 
import calendar
import json

class ReadPDFToolInput(BaseModel):
    """Input schema for ReadPDFTool."""
    pdf_path: str = Field(..., description="Đường dẫn đến file PDF.")

class ReadPDFTool(BaseTool):
    name: str = "Read PDF Tool"
    description: str = (
        """
        Tool này sử dụng PyMuPDF và pdfplumber để đọc nội dung trong file pdf.
        Đầu vào là đường dẫn của file pdf.
        Đầu ra là nội dung của file pdf.
        """
    )
    args_schema: Type[BaseModel] = ReadPDFToolInput


    def _run(self, pdf_path: str) -> str:
        # Đọc nội dung từ file PDF
        pages = []
        if isinstance(pdf_path, tuple) and len(pdf_path) == 1:  # Check if pdf_path is a tuple with one element
            pdf_path = pdf_path[0]  # Extract the string from the tuple
        if not isinstance(pdf_path, str):  # Check if pdf_path is a string
            print(f"Invalid pdf_path: {pdf_path}")
            return "Error"
        try:
            document = fitz.open(pdf_path)
            
            for page_number in range(document.page_count):
                page = document.load_page(page_number)
                text = page.get_text()
                pages.append(text)
            document.close()
        except Exception as e:  # Bắt lỗi cụ thể từ PyMuPDF
            try:
                with pdfplumber.open(pdf_path) as document:  # Mở tài liệu PDF bằng pdfplumber
                    for page in document.pages:  # Lặp qua các trang
                        text = page.extract_text()  # Lấy văn bản từ trang
                        pages.append(text)
            except Exception as e:
                print(f"Lỗi không thể đọc được nội dung từ PDF bằng PyMuPDF và pdfplumber:\n{e}\nPath: {pdf_path}")
                err = "Error"
                return err
        return "\n\n".join(pages).strip()

def parse_dates(date_str, last_date=False):
    # Thêm trường hợp cho định dạng "Month YYYY"
    month_map = {month: f"{index:02d}" for index, month in enumerate(calendar.month_name) if month}
    
    # Thêm trường hợp cho định dạng "Month YYYY" với viết tắt
    month_map.update({month[:3]: f"{index:02d}" for index, month in enumerate(calendar.month_name) if month})  # Thêm viết tắt
    month_map.update({month[:4] + '.': f"{index:02d}" for index, month in enumerate(calendar.month_name) if month})  # Thêm viết tắt với dấu chấm
    month_map.update({month[:3] + '.': f"{index:02d}" for index, month in enumerate(calendar.month_name) if month})  # Thêm viết tắt
    # print(month_map)
    
    # Thêm trường hợp cho định dạng "YYYY-M"
    if re.match(r'^\d{4}-\d{1,2}$', date_str):  # Kiểm tra định dạng "YYYY-M"
        year, month = date_str.split('-')
        date_str = f"{year}-{int(month):02d}"  # Trả về định dạng "YYYY-MM"

    if re.match(r'^[A-Za-z]+\.? \d{4}$', date_str):  # Kiểm tra định dạng "Month YYYY" với hoặc không có dấu chấm
        month_name, year = date_str.split()
        month = month_map.get(month_name)
        if month:
            date_str = f"{year}-{month}"  # Trả về định dạng "YYYY-MM"

    if re.match(r'^\d{4}(-\d{2}(-\d{2})?)?$', date_str):  # Skip non-date strings
        try:
            if last_date:                # Handle the case for just the year
                last_day = 31
                if len(date_str) == 4:  # Format "YYYY"
                    year = int(date_str) # Default to the last day of December
                    if year >= 9000: return "Hiện tại"
                    date_str = f"{year}-12-31"  # Use December 31st of that year

                # Handle the case for year and month
                elif len(date_str) == 7:  # Format "YYYY-MM"
                    year, month = map(int, date_str.split('-'))
                    if year >= 9000: return "Hiện tại"
                    last_day = calendar.monthrange(year, month)[1]  # Get the last day of the month
                    date_str = f"{year}-{month:02d}-{last_day:02d}"  # Format as YYYY-MM-DD

                # Handle the case for full date
                elif len(date_str) == 10:  # Format "YYYY-MM-DD"
                    year, month, day = map(int, date_str.split('-'))
                    if year >= 9000: return "Hiện tại"
                    if day != 0:
                        # print(day)
                        last_day = day
                    # print(last_day, "-", type(last_day))
                    date_str = f"{year}-{month:02d}-{last_day:02d}"  # Format as YYYY-MM-DD
            else:
                last_day = 1  # Default to the last day of December
                # Handle the case for just the year
                if len(date_str) == 4:  # Format "YYYY"
                    year = int(date_str)
                    date_str = f"{year}-01-{last_day:02d}"  # Use December 31st of that year

                # Handle the case for year and month
                elif len(date_str) in [6, 7]:  # Format "YYYY-MM"
                    year, month = map(int, date_str.split('-'))
                    date_str = f"{year}-{month:02d}-{last_day:02d}"  # Format as YYYY-MM-DD

                # Handle the case for full date
                elif len(date_str) in [8, 9, 10]:  # Format "YYYY-MM-DD"
                    year, month, day = map(int, date_str.split('-'))
                    if day != 0:
                        last_day = day
                        
                    date_str = f"{year}-{month:02d}-{last_day:02d}"  # Format as YYYY-MM-DD
        except ValueError:
            print(f"Invalid date format: {date_str}")
        return date_str
    
    elif re.match(r'^(\d{1,2}/\d{1,2}/\d{4}|\d{1,2}/\d{4}|\d{4})$', date_str):
        if len(date_str) == 4:
            year = int(date_str)
            date_str = f"{year}"  # Use December 31st of that year
        elif len(date_str) in [6, 7]:  # Format "YYYY-MM"
            month, year = map(int, date_str.split('/'))
            date_str = f"{year}-{month:02d}"  # Format as YYYY-MM-DD
        elif len(date_str) in [8, 9, 10]:
            day, month, year = map(int, date_str.split('/'))
            if day != 0:
                last_day = day
            else: date_str = f"{year}-{month:02d}"
                
            date_str = f"{year}-{month:02d}-{last_day:02d}"  # Format as YYYY-MM-DD  # Format as YYYY-MM-DD
    
        return parse_dates(date_str, last_date)
    elif re.match(r'^T\d{1,2}/\d{4}$', date_str):  # Thêm trường hợp cho định dạng "T6/2023"
        month, year = date_str[1:].split('/')  # Bỏ 'T' và tách tháng và năm
        date_str = parse_dates(f"{year}-{int(month):02d}",last_date)  # Trả về định dạng "YYYY-MM"
        return date_str
 
    else:
        # Thêm trường hợp cho định dạng "MM-YYYY"
        if re.match(r'^\d{1,2}-\d{4}$', date_str):  # Kiểm tra định dạng "MM-YYYY"
            month, year = date_str.split('-')
            date_str = parse_dates(f"{year}-{int(month):02d}",last_date)  # Trả về định dạng "YYYY-MM"

        return date_str

def clean_data(data):
    """Xóa các trường không có thông tin."""
    if isinstance(data, str):
        return data.replace('\n',' ')
    if isinstance(data, dict):
        return {k: clean_data(v) for k, v in data.items() if v not in (None, [], {}, "", )}
    elif isinstance(data, list):
        return [clean_data(item) for item in data if item not in (None, [], {}, "")]
    return data

def edit_date(data, file_path):
    """Chỉnh sửa các trường ngày tháng trong dữ liệu.

    Args:
        data (dict): Dữ liệu JSON chứa thông tin ứng viên, bao gồm các trường như 'education', 'work_experience', v.v.
        file_path (str): Đường dẫn đến file chứa dữ liệu, dùng để ghi lại các lỗi nếu có.

    Returns:
        dict: Dữ liệu đã được chỉnh sửa với các trường ngày tháng được định dạng lại.
    """
    error_path = ""
    # Iterate over the keys of the dictionary
    for item in data:  # Giả sử data là một đối tượng JSON\
        # print(111)
        if item in ['education', 'work_experience', 'certificates', 'awards', 'courses', 'projects', 'products', 'activities']:  # Check if 'work_experience' exists
            # print(111)
            if isinstance(data[item], list):  # Check if the item is a list
                for elm in range(len(data[item])):  # Iterate over the list of work experiences
                    if 'start_date' in data[item][elm]:
                        # print(111)
                        date = data[item][elm]['start_date']
                        data[item][elm]['start_date'] = parse_dates(date)
                    if 'end_date' in data[item][elm]:
                        # print(111)
                        date = data[item][elm]['end_date']
                        data[item][elm]['end_date'] = parse_dates(date,last_date=True)

            else:
                error_path += file_path + '\n'
    with open("error_path.txt", 'w', encoding='utf-8') as file:  # Specify the output file path
        file.write(error_path)  # Convert data to JSON string
    
    return data

def convert_response_to_json_string(response, file_name):
    output_path = "./src/jd_assistants/results_json/"
    text = response.replace('/n',' ') # Ghi nội dung của biến text vào file

    start_index = text.find('```json') + len('```json')
    end_index = text.find('```', start_index)
    json_string = text[start_index:end_index].strip()
    
    data = json.loads(json_string)
    # print("data load json")
    # print(data)
    data = clean_data(data)
    # print(type(data))
    
    with open(output_path+file_name+'.json', 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)
    
    return data