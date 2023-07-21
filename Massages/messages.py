def change_message(username, date):
    return f"Hi {username}" \
           f"your password changed : {date}"


def forgot_password(username, code):
    return f"Hi {username} " \
           f"This code for change your account password : {code}"


def email_varification(username, code):
    return f"Hi {username} " \
           f"Your varification code is {code}"
