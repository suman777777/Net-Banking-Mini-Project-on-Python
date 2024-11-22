#----------------------------- date - 24/july/2024 -------------------------------------

# importing packages
import sqlite3
import random

# # connecting db file
conn = sqlite3.connect('mydb.db')
# # fetching data from db
# data = list(conn.execute('''select * from SBI_IFSC where ifsc_code="SBIN0021870" '''))
# print(data)
# amount = 1000
# data = list(conn.execute(f'''update AccountDetails set bank_balance = "{amount}" where username = "santhosh@gmail.com"'''))
# print(data)
# conn.commit()
# Registration
def registration():
    full_name = input("Enter your full name : ")
    username = input("Enter username : ")
    allusernames = list(conn.execute('''select username from AccountDetails'''))
    allusernames = [i[0] for i in allusernames]
    if username not in allusernames:
        while True:
            option = int(input("1. Bangalore \n2. Chennai \nEnter your option : "))
            match option:
                case 1:
                    city_name  = "BANGALORE"
                    branches = list(conn.execute(f'''select BRANCH_NAME from SBI_IFSC where city_name = "{city_name}"'''))
                    branches = [i[0] for i in branches]
                    for i in range(1, len(branches)+1):
                        print(f"{i}. {branches[i-1]}")
                    option = int(input("Enter option : "))
                    if 1<=option<=len(branches):
                        branch_name = branches[option-1]
                        ifsc_code = list(conn.execute(f'''select ifsc_code from SBI_IFSC where BRANCH_NAME = "{branch_name}"'''))[0][0]
                        print(ifsc_code)
                        print(branch_name)
                        break
                    else:
                        print("Invalid Option")
                case 2:
                    city_name = "CHENNAI"
                    branches = list(conn.execute(f'''select BRANCH_NAME from SBI_IFSC where city_name = "{city_name}"'''))
                    branches = [i[0] for i in branches]
                    for i in range(1, len(branches)+1):
                        print(f"{i}. {branches[i-1]}")
                    option = int(input("Enter option : "))
                    if 1<=option<=len(branches):
                        branch_name = branches[option-1]
                        ifsc_code = list(conn.execute(f'''select ifsc_code from SBI_IFSC where BRANCH_NAME = "{branch_name}"'''))[0][0]
                        print(ifsc_code)
                        print(branch_name)
                        break
                    else:
                        print("Invalid Option")
                case _:
                    print("InvalidOption... ")
        while True:
            password = input("Enter Password : ")
            confirm_password = input("Confirm Password : ")
            if password == confirm_password:
                account_no = random.randint(10000000000, 99999999999)
                bank_name = 'STATE BANK OF INDIA'
                conn.execute(f'''insert into AccountDetails (username, password, branchname, bankname, branchcode, city_name, account_number, bank_balance, full_name) values("{username}", "{password}", "{branch_name}", "{bank_name}", "{ifsc_code}", "{city_name}","{account_no}", "0","{full_name}" )''')
                print("Registration Successfull✅✅✅")
                conn.commit()
                checkloginusername()
                break
            else:
                print("Password miss match ...")
    else:
        print("Username is already present")
        registration()
                
# Net Banking
def netbanking(userdetails, username):
    print("Welcome to Net Banking 😊")
    receiverusername = input("Enter Receiver Username : ")
    allusernames = list(conn.execute('''select username from AccountDetails'''))
    # print(allusernames)
    allusernames = [i[0] for i in allusernames]
    # print(allusernames)
    if receiverusername in allusernames:
        while True:
            amount = int(input("Enter amount : 0 - 10000 : "))
            if 0<=amount<=10000:
                sender_balance = list(conn.execute(f'''select bank_balance from AccountDetails where username = "{username}"'''))[0][0]
                if amount <= sender_balance:
                    while True:
                        g_otp = random.randint(1000, 9999)
                        u_otp = int(input(f"OTP : {g_otp}\nEnter your OTP : "))
                        if g_otp == u_otp:
                            print("OTP Validation Successfull")
                            receiver_balance = list(conn.execute(f'''select bank_balance from AccountDetails where username ="{receiverusername}"'''))[0][0]
                            sender_balance -= amount
                            receiver_balance += amount
                            conn.execute(f'''update AccountDetails set bank_balance = {sender_balance} where username = "{username}"''')
                            conn.commit()
                            conn.execute(f'''update AccountDetails set bank_balance = {receiver_balance} where username = "{receiverusername}"''')
                            conn.commit()
                            check_balance(userdetails, username)
                            break
                        else:
                            print("Invalid OTP")
                    break
                else:
                    print("Not having enough balance") 
            else:
                print("Enter amount 0 - 10000")
    else:
        print("Sender username is not present")
        netbanking(userdetails, username)
    
# Check balance
def check_balance(userdetails, username):
    # method 1
    balance = list(conn.execute(f'''select bank_balance from AccountDetails where username = "{username}"'''))[0][0]
    print(f"Current Balance is : {balance}")
    while True:
        option = int(input("Back to main menu enter 1 : "))
        if option == 1:
            showfeatures(userdetails, username)
            break
        else:
            print("Invalid Option ❌❌❌")
    # method 2
    # print(f"Balance is : {userdetails[8]}")
def addamount(userdetails, username):
    amount = int(input("Enter amount : 0 --> 10000 : "))
    if 0<= amount <=10000:
        old_amount = list(conn.execute(f'''select bank_balance from AccountDetails where username = "{username}"'''))[0][0]
        print("old amount : ", old_amount)
        while True:
            g_otp = random.randint(1000, 9999)
            u_otp = int(input(f"OTP : {g_otp}\nEnter OTP here : "))
            if g_otp == u_otp:
                print("OTP validation successfull")
                old_amount += amount
                conn.execute(f'''update AccountDetails set bank_balance = "{old_amount}" where username = "{username}"''')
                conn.commit()
                check_balance(userdetails, username)
                while True:
                    option = int(input("Back to main menu enter 1 : "))
                    if option == 1:
                        showfeatures(userdetails, username)
                        break
                    else:
                        print("Invalid Option ❌❌❌")
                break
            else:
                print("Invalid OTP ❌❌❌")
    else:
        print("Enter amount range should be 0 to 10000")
        addamount(userdetails, username)
# show profile
def showprofile(userdetails, username):
    print("Profile Details 👇👇👇\n-----------------------")
    print(f"Name : {userdetails[-1]}\nUsername : {userdetails[1]}\nAccount number : {userdetails[7]}\nBank Name : {userdetails[4]}\nBranch Name : {userdetails[3]}\nIFSC CODE : {userdetails[5]}")
    while True:
        option = int(input("Enter 1 to show features \nEnter option : "))
        if option == 1:
            showfeatures(userdetails, username)
            break
        else:
            print("Invalid Option...")
# features
def showfeatures(userdetails, username):
    print("1. Add Amount\n2. Net Banking\n3. Check Balance\n4. Show Profile\n5. Logout")
    option = int(input("Enter your option : "))
    match option:
        case 1:
            addamount(userdetails, username)
        case 2:
            netbanking(userdetails, username)
        case 3:
            check_balance(userdetails, username)
        case 4:
            showprofile(userdetails, username)
        case 5:
            return 0
        case _:
            print("Invalid Option")
            showfeatures(userdetails, username)
# check user password
def checkuserpassword(username):
    print("Enter Password ...")
    print(f"Username : {username}")
    user_db_password = list(conn.execute(f'''select password from AccountDetails where username = "{username}"'''))[0][0]
    # print(user_db_password)
    password = input("Enter password : ")
    if password == user_db_password:
        print("Password validation successfull ✅✅✅")
        userdetails = list(conn.execute(f'''select * from AccountDetails where username = "{username}"'''))
        userdetails = [i for i in userdetails[0]]
        # print(userdetails)
        showfeatures(userdetails, username)
    else:
        print("Password is not matching ❌❌❌")
        checkuserpassword(username)
# check login username
def checkloginusername():
    print("Enter Login . . . . ")
    username = input("Enter username here : ").lower()
    if username.endswith("@gmail.com"):
        allusernames = list(conn.execute('''select username from AccountDetails'''))
        # print(allusernames)
        allusernames = [i[0] for i in allusernames]
        if username in allusernames:
            print("Valid Username ✅✅✅")
            checkuserpassword(username)
        else:
            print("Invalid Username ❌❌❌")
            checkloginusername()
    else:
        print("Incorrect Username ❌❌❌")
        checkloginusername()
# start logic here

def start():
    option = int(input("1. Login\n2. Register\n3. Logout\nEnter Your option : "))
    match option:
        case 1:
            # print("Login Here")
            checkloginusername()
        case 2:
            registration()
        case 3:
            return 0
        case _:
            print("Invalid Option ❌❌❌")
            start()
start()