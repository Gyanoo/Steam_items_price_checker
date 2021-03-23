import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import get_all_prices as gap
from datetime import date


def send_mail():
    sticker_dict_un, total_price = gap.get_all_prices()
    sticker_dict = sorted(sticker_dict_un.items(), key=lambda x: x[1][1], reverse=True)
    msg_HTML = "<!DOCTYPE html> <html> <head> <style> table, th, td { border: 1px solid black; border-collapse: collapse; \
                text-align: center; padding: 10px;} </style> </head>"
    msg_HTML += "<h1> total price: " + total_price + "USD </h1><br><h4> Set of all prices: <br></h4>" + \
                " <table> <tr> <th> No. </th><th> quantity </th> <th> name </th> " \
                "<th> price </th> <th> total </th> </tr>"
    for idx in range(0, len(sticker_dict)):
        msg_HTML += "<tr> <td>" + str(idx+1) + "</td><td> " + str(sticker_dict[idx][1][0]) + "</td> <td> " + str(sticker_dict[idx][0]) + \
                    " </td> <td> " + str(sticker_dict[idx][1][1]) + "USD </td> <td>" + \
                    str(float(sticker_dict[idx][1][0]) * float(sticker_dict[idx][1][1])) + \
                    " USD</td> </tr>"
        idx += 1
    msg_HTML += " </table>"
    message = MIMEMultipart('alternative')
    message['From'] = 'gyanobot@gmail.com'
    message['To'] = 'oogyano@gmail.com'
    message['Subject'] = "Stickers prices on " + str(date.today())
    message.attach(MIMEText(msg_HTML, 'html'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    login = input("Enter mail: ")
    server.login(login, input("Enter password: "))
    text = message.as_string()
    server.sendmail(login, input("Enter receiver's mail: "), text)
    server.close()
