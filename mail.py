import smtplib
#import getpass

HOST = "smtp.gmail.com"
PORT = 587
FROM_EMAIL = "webseo42@gmail.com"
TO_EMAIL = "zainlokhandwala21@gmail.com"
PASSWORD = "zhlu iihq qkuc qlru"

SUBJECT="""Subject:Thank You for Registering",

                Dear,

                Thank you for registering.  We are excited to have you as part of our community.

                You've taken the first step towards.

                If you have any feedback or suggestions on how we can improve your experience, 
                please feel free to share them with us. We're always looking for ways to enhance our platform for our users.

                Once again, thank you for choosing US. We look forward to serving you.

                Warm regards,
                The [SEO Analysis] Team."""

smtp = smtplib.SMTP(HOST, PORT)

status_code, response = smtp.ehlo()
print(f"[*] Echoing the server: {status_code} {response}")

status_code, response = smtp.starttls()
print(f"[*] Starting TLS connection: {status_code} {response}")

status_code, response = smtp.login(FROM_EMAIL, PASSWORD)
print(f"[*] Logging in: {status_code} {response}")

smtp.sendmail(FROM_EMAIL, TO_EMAIL, SUBJECT)
smtp.quit()
