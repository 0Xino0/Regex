import re

def  validate_email(input):
    #الگو regex برای استخراج ایمیل ها
    pattern_email = re.compile(r'\w+\@\w+\.\w+')
    # افزدون ایمیل ها به یک لیست
    validate_email = re.findall(pattern_email,input)
    return validate_email


if __name__ == "__main__":
    #گرفتن ایمیل از کاربر
    email_address = input("Please enter your email address")
    #اعتبار سنجی ایمیل ها
    validate_emails = validate_email(email_address)
    #خروجی
    for email in validate_emails:
        print(email)

