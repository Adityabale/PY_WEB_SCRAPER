import requests
import xlwt #helps working with excel spreadsheets
from xlwt import Workbook
import smtplib
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate

BASE_URL = "https://remoteok.com/api/"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:107.0) Gecko/20100101 Firefox/107.0"
#get user agent of your browser from https://www.whatismybrowser.com/detect/what-is-my-user-agent/
REQUEST_HEADER = { 

    'User-Agent':USER_AGENT,
    'Accept-Language':'en-US, en;q=0.5',

}

def get_job_postings():
    response = requests.get(url=BASE_URL, headers=REQUEST_HEADER)
    return response.json()

def output_jobs_to_xls(data):
    wb = Workbook()
    job_sheet = wb.add_sheet('Jobs')
    headers = list(data[0].keys())
    for i in range(0,len(headers)):
        job_sheet.write(0,i,headers[i]) #(row,column,data) will provide header to the spreadsheet
    for j in range(0,len(data)):
        job = data[j]
        values = list(job.values())
        for x in range(0,len(values)):
            job_sheet.write(j+1,x,values[x]) # (row,column,data) as first row is header we use i+1
    wb.save('remote_jobs.xls')

def send_email(send_from, send_to, subject, text, files=None):
    assert isinstance(send_to,list)
    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = COMMASPACE.join(send_to)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject

    msg.attach(MIMEText(text))

    for f in files or []:
        with open(f,"rb") as fil:
            part = MIMEApplication(fil.read(),Name=basename(f))
        part['Content-Disposition'] = f'attachment; filename="{basename(f)}"'
        msg.attach(part)

    smtp = smtplib.SMTP('smtp@gmail.com:587')
    smtp.starttls()
    smtp.login(send_from,'#######Write your password')
    smtp.sendmail(send_from, send_to, msg.as_string())
    smtp.close()


if __name__ == "__main__":
    json = get_job_postings()[1:]
    output_jobs_to_xls(json)
    send_email("adityabale94@gmail.com", ['contact@email.com'],'Jobs posting', 'Please find attache a list of job openings', files='remote_jobs.xls')


#https://myaccount.google.com/lesssecureapps