from email.mime.text import MIMEText
import smtplib

def send_email(email, height, average_height, no_users):
	from_email = "devbotalex@gmail.com"
	from_password = "AdevBot!3"
	to_email = email
	subject = "Height data"
	message = f"Hello! Your height is <strong>{height}</strong> cm. The average height of {no_users} users is <strong>{average_height}</strong> cm. "
	
	message_M = MIMEText(message, 'html')
	message_M['Subject'] = subject
	message_M['To'] = to_email
	message_M['From'] = from_email

	gmail = smtplib.SMTP('smtp.gmail.com', 587)
	gmail.ehlo()
	gmail.starttls()
	gmail.login(from_email, from_password)
	gmail.send_message(message_M)
