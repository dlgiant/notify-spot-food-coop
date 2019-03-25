from bs4 import BeautifulSoup
from string import Template
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import requests
import smtplib
import os

contacts = "contacts.txt"
message = "message.txt"
sent_by = os.environ['EMAILGMAIL']
password = os.environ['PASSGMAIL']

def check():
	page = requests.get("https://ort.foodcoop.com/join/register")
	soup = BeautifulSoup(page.content, 'html.parser')
	any_spots = soup.find_all('h1')[1]

	if str(any_spots)=="<h1> Sorry, there are no sessions available at this time.</h1>":
		False
	else:
		True

def get_contacts(filename):
	names = []
	emails = []
	with open(filename, mode='r', encoding='utf-8') as contacts_file:
		for a_contact in contacts_file:
			names.append(a_contact.split()[0])
			emails.append(a_contact.split()[1])
	return names, emails

def read_template(filename):
	with open(filename, 'r', encoding='utf-8') as template_file:
		template_file_content = template_file.read()
	return Template(template_file_content)

if check():
	print("THERE ARE SPOTS, RUN!")
	names, emails = get_contacts(contacts)
	template_file = read_template(message)
	try:
		# Assuming the host is GMAIL
		s = smtplib.SMTP_SSL(host='smtp.gmail.com', port=465)
		s.ehlo()
		s.login(sent_by, password)

		for i in range(len(emails)):
			name = names[i]
			email = emails[i]
			msg = MIMEMultipart()
			message = template_file.substitute(PERSON_NAME=name.title())
			msg['From'] = sent_by
			msg['To'] = email
			msg['Subject'] = 'QUICK! Sign up for orientation now!'
			msg.attach(MIMEText(message, 'plain'))
			s.send_message(msg)
		s.close()
	except:
		print("Something went wrong.")
else:
	print("No spots available at this time.")

# TODO: Allow unsafe apps on Gmail setting
# TODO: Disallow when no longer at use
