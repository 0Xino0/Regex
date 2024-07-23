import re
from persiantools.jdatetime import JalaliDate
import datetime

def  validate_email(input):
    #الگو regex برای استخراج ایمیل ها
    pattern_email = re.compile(r'\w+\@\w+\.\w+')
    # افزدون ایمیل ها به یک لیست
    validate_email = re.findall(pattern_email,input)
    return validate_email

# تابع استخراج تاریخ‌ها از متن
def extract_dates(text):
    # الگوی regex برای شناسایی تاریخ‌ها در فرمت‌های مختلف
    date_pattern = r'\b(\d{1,2})[-/](\d{1,2}|[A-Za-z]+)[-/](\d{2,4})\b'

    # جستجو و استخراج تاریخ‌ها
    dates = re.findall(date_pattern, text)
    
    extracted_dates = []
    for date in dates:
        day, month, year = date
        # اگر سال به صورت دو رقمی بود، فرض می‌کنیم مربوط به قرن 21 است
        if len(year) == 2:
            year = int(year)
            if year < 50:  # فرض می‌کنیم تاریخ‌های دو رقمی کمتر از 50 مربوط به 2000 تا 2049 هستند
                year += 2000
            else:
                year += 1900
        else:
            year = int(year)

        extracted_dates.append((day, month, year))

    return extracted_dates

# تابع تبدیل تاریخ میلادی به هجری شمسی
def convert_to_jalali(day, month, year):
    
    # تعریف دیکشنری برای تبدیل نام ماه به عدد مربوطه
    months = {
        "January": 1, "February": 2, "March": 3, "April": 4,
        "May": 5, "June": 6, "July": 7, "August": 8,
        "September": 9, "October": 10, "November": 11, "December": 12,
        "Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4,
        "May": 5, "Jun": 6, "Jul": 7, "Aug": 8,
        "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12
    }
    # بررسی و تبدیل ماه
    try:
        # اگر ماه عدد باشد، مستقیماً استفاده می‌شود
        month_number = int(month)
    except ValueError:
        # اگر ماه نام متنی باشد، تبدیل به عدد
        month_number = months.get(month.capitalize(), None)
        if not month_number:
            raise ValueError(f"Invalid month name: {month}")

    # ایجاد شیء تاریخ میلادی
    gregorian_date = datetime.date(year, month_number, int(day))
    
    # تبدیل به تاریخ هجری شمسی
    jalali_date = JalaliDate.to_jalali(gregorian_date)
    
    return jalali_date

def parse_log1(text):
    #الگو regex برای تجزیه لاگ
    pattern = re.compile(r"(\d{4}\/\d{2}\/\d{2}) (\d{2}\:\d{2}\:\d{2}) \[(\w+)\] (\d{4})\#(\d{4})\: (\*\d{5}) (\w+\(\)[\w+|\s]+\(\d+\:[\w+|\s]+\)[\s|\w+]+)\, client\:\s?(\d{1,4}\.\d{1,4}\.\d{1,4}\.\d{1,4}),\s+?server\:\s?(\w+\.\w+),\s+?request\:\s?\“([\w|\s]+\/[\w|\s]+\/[\w|\s]+\/[\d|\.]+)\”,\s+?upstream\:\s?\“(\w+\:\/\/\d{1,4}\.\d{1,4}\.\d{1,4}\.\d{1,4}\:\d+\/\w+\/\w+)\”\,\s+?host\:\s?\“(\w+\.\w+)\”\,\s+?referrer\:\s?\“(\w+\:\/\/\w+\.\w+\/)\”")
    #متن تجزیه شده
    Parsed_text = re.search(pattern,text)

    date , time , level , proccesID , threadID , unique_identifier , error_message , ip , server , request , upstream , host , referrer = Parsed_text.groups()
    parsed_log = {
        "date": date,
        "time": time,
        "level": level,
        "proccedID": proccesID,
        "threadID" : threadID,
        "unique_identifier": unique_identifier,
        "error_message" : error_message,
        "ip" : ip,
        "server" : server,
        "request" : request,
        "upstream" : upstream,
        "host" : host,
        "referrer" : referrer
    }
    return parsed_log

def parse_log2(text):
    #الگو regex برای تجزیه لاگ
    pattern = re.compile(r"(\d{4}\/\d{2}\/\d{2}) (\d{2}\:\d{2}\:\d{2}) \[(\w+)\] (\d{4})\#(\d{4})\: (\*\d{5}) (.*?)\, client\:\s?(\d{1,4}\.\d{1,4}\.\d{1,4}\.\d{1,4}),\s+?server\:\s?(\w+\.\w+),\s+?request\:\s?\“([\w|\s]+\/[\w|\-|\s|]+\/[\d|\.]+)\”\,\s+?host\:\s?\“(\w+\.\w+)\”\,\s+?referrer\:\s?\“(\w+\:\/\/\w+\.\w+\/)\”")
    #متن تجزیه شده
    Parsed_text = re.search(pattern,text)

    date , time , level , proccesID , threadID , unique_identifier , error_message , ip , server , request , host , referrer = Parsed_text.groups()

    parsed_log = {
        "date": date,
        "time": time,
        "level": level,
        "proccedID": proccesID,
        "threadID" : threadID,
        "unique_identifier": unique_identifier,
        "error_message" : error_message,
        "ip" : ip,
        "server" : server,
        "request" : request,
        "host" : host,
        "referrer" : referrer
    }
    return parsed_log


if __name__ == "__main__":
    #گرفتن ایمیل از کاربر
    email_address = input("Please enter your email address")
    #اعتبار سنجی ایمیل ها
    validate_emails = validate_email(email_address)
    #خروجی
    for email in validate_emails:
        print(email)

    # نمونه متن شامل تاریخ‌های مختلف
    text = """
    11-07-2024
    9-7-2024
    9/7/2024
    9/7/24
    29-july-2024
    29/July/2024
    """ 

    dates = extract_dates(text)
    for day, month, year in dates:
        jalali_date = convert_to_jalali(day, month, year)
        print(f'Miladi: {day}-{month}-{year} => Jalali: {jalali_date}')

    nginx_accesslog = """
    2024/07/11 15:30:45 [error] 1234#1234: *56789 connect() failed (111: Connection refused) while connecting to upstream, client: 192.168.1.100, server: example.com, request: “GET /api/data HTTP/1.1”, upstream: “http://127.0.0.1:8000/api/data”, host: “example.com”, referrer: “https://example.com/”
    """  
    parsed_log_dic1 = parse_log1(nginx_accesslog)
    print(parsed_log_dic1)


    nginx_accesslog2 = """
    2024/07/11 16:15:20 [error] 1234#1234: *67890 open() “/usr/share/nginx/html/not_found.html” failed (2: No such file or directory), client: 192.168.1.101, server: example.com, request: “GET /nonexistent-page HTTP/1.1”, host: “example.com”, referrer: “https://example.com/”
    """
    parsed_log_dic2 = parse_log2(nginx_accesslog2)
    print(parsed_log_dic2)