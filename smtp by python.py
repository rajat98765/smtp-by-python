import string
from random import *

import pymysql
import cgi

connection = pymysql.connect(host='localhost', user='root',
                             password='', db='',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

cursor = connection.cursor()

sql = "select email from users"

cursor.execute(sql)
result = cursor.fetchall()

sql1="select * from users where forsmtp=0"
cursor.execute(sql1)
result1 = cursor.fetchall()

import smtplib
smtpid=[]
passwordlist=[]
def gmail():
    
    print("CONNECTING TO GMAIL")
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        print("CONNECTED")
        print("STARTING SECURE CONNECTION")
        try:
            server.starttls()
            print("SECURED CONNECTION REACHED")
        except:
            print("WARNING: ITS NOT SAFE SEND THIS EMAIL")
        gmailUser = str(input("USERNAME: "))
        gmailPasswd = str(input("PASSWORD: "))
        print("CHECKING USERNAME AND PASSWORD")
        try:
            server.login(gmailUser, gmailPasswd)
            print("YOUR USERNAME AND PASSWORD ARE CORRECT")
        except:
            print("YOUR USERNAME, PASSWORD OR BOTH IS INCORRECT")
            quit

        recipient = result
        recipient1=result1
        l = len(recipient1)
        #print(recipient)
        
        count = 1       
        for i in range(l):

            if  count<490 :
                #recipient = str(input("RECIPIENT: "))
                min_char = 6
                max_char = 10
                allchar = string.ascii_letters  + string.digits
                password = "".join(choice(allchar) for x in range(randint(min_char, max_char)))
                
                password1 = ("Your new password is ")+password
                print ("This is your password : ")
                print(password)
                #message1 = str(input("MESSAGE:\n"))
                message = 'Subject : Password For Yearbook  \n\n '+ password1
        
                print("SENDING EMAIL")
                try:
                    server.sendmail(gmailUser, recipient1[i]['email'], message)
                    print("MESSAGE SENT FROM: " + gmailUser)
                    count = count+1
                    #smtpid.apppend(recipient1[i]['id'])
                    smtpid.append(recipient1[i]['id'])
                    print(smtpid)
                    #sql4="Update users set password = %s"
                    cursor.execute ("UPDATE users SET password=%s WHERE id =%s", (password,recipient1[i]['id']))
                    passwordlist.append(password)
                    print(passwordlist)

                
                    quit
                except:
                    print("AN ERROR OCCURED WHILE SENDING YOUR E-MAIL OR EMAIL ADDRESS PROVIDED IS NOT CORRECT")
                    quit
            else:
                print("You have REACHED YOUR LIMIT FROM THIS EMAIL PLEASE USE NEW EMAIL TO SEND MORE MESSAGE")
                break
    except:
        print("CANNOT CONNECT TO GMAIL")
        quit


    l1=len(smtpid)
  
    if l1 > 0 :

        sql2 = 'UPDATE users SET forsmtp=1  WHERE id in (' + ','.join(map(str, smtpid)) + ')'

        cursor.execute(sql2)

    else:
        print("You have no Email to be send")
        
    connection.commit()
    print("good")  

gmail()

cursor.close()
connection.close()
