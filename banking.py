import random
import sqlite3
import sys

def createDatabase():
    conn = sqlite3.connect("card.s3db")
    cur = conn.cursor()
    cur.execute('CREATE TABLE card(id INTEGER, number TEXT,pin TEXT,balance INTEGER DEFAULT 0);')

def saveData(card, pin, balance):
    conn = sqlite3.connect("card.s3db")
    cur = conn.cursor()
    cur.execute('INSERT INTO card(number, pin, balance) VALUES({}, {}, {});'.format(card, pin, balance))
    conn.commit()

def checkValidity(card_num, pin):
    conn = sqlite3.connect('card.s3db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM card WHERE number = {} AND pin = {};'.format(str(card_num), str(pin)))
    valid = cur.fetchone()
    return valid

def checkLuhn(cardNo):
    cardNo = str(cardNo)
    nDigits = len(cardNo)
    nSum = 0
    isSecond = False

    for i in range(nDigits - 1, -1, -1):
        d = ord(cardNo[i]) - ord('0')

        if (isSecond == True):
            d = d * 2
        nSum += d // 10
        nSum += d % 10

        isSecond = not isSecond

    if (nSum % 10 == 0):
        return False
    else:
        return True

def checkCardNumber(r_num):
    conn = sqlite3.connect("card.s3db")
    cur = conn.cursor()
    cur.execute('SELECT * FROM card WHERE number = {};'.format(r_num))
    result = cur.fetchone()
    if result == None:
        return True
    else:
        return False

def doTransfer(card_num):
    conn = sqlite3.connect("card.s3db")
    cur = conn.cursor()
    print("Enter receiver's card number")
    r_num = int(input())
    if r_num == card_num:
        print("You can't transfer money to the same account!")
    elif checkLuhn(r_num):
        print("Probably you made a mistake in the card number. Please try again!")
    elif checkCardNumber(r_num):
        print("Such a card does not exist.")
    else:
        print("Enter Transfer Amount")
        amount = int(input())
        cur.execute('SELECT balance FROM card WHERE number = {};'.format(card_num))
        bal = int(cur.fetchone()[0])
        print(bal)
        if bal >= amount:
            cur.execute('UPDATE card SET balance = balance - {} WHERE number = {};'.format(amount, card_num))
            conn.commit()
            cur.execute('UPDATE card SET balance = balance + {} WHERE number = {};'.format(amount, r_num))
            conn.commit()
        else:
            print("Not enough money!")

def getBalance(card_num):
    conn = sqlite3.connect('card.s3db')
    cur = conn.cursor()
    cur.execute('SELECT balance FROM card WHERE number = {};'.format(card_num))
    return cur.fetchone()[0]

def closeAccount(number):
    conn = sqlite3.connect("card.s3db")
    cur = conn.cursor()
    cur.execute('DELETE FROM card WHERE number = {};'.format(number))
    conn.commit()

def addIncome(number, amount):
    conn = sqlite3.connect("card.s3db")
    cur = conn.cursor()
    cur.execute('SELECT balance FROM card WHERE number = {};'.format(card_num))
    bal = cur.fetchone()
    total = int(bal[0]) + amount
    cur.execute('UPDATE card SET balance = {} WHERE number = {};'.format(total, number))
    conn.commit()

def generateCardNumber():
    first_6 = "400000"
    card_no = [int(i) for i in str(first_6)]  # To find the checksum digit on
    card_num = [int(i) for i in str(first_6)]  # Actual account number
    seventh_15 = random.sample(range(9), 9)  # Acc no (9 digits)
    for i in seventh_15:
        card_no.append(i)
        card_num.append(i)
    for t in range(0, 15, 2):  # odd position digits
        card_no[t] = card_no[t] * 2
    for i in range(len(card_no)):
        if card_no[i] > 9:  # deduct 9 from numbers greater than 9
            card_no[i] -= 9
    s = sum(card_no)
    mod = s % 10
    check_sum = 0 if mod == 0 else (10 - mod)
    card_num.append(check_sum)
    card_num = [str(i) for i in card_num]
    return ''.join(card_num)

def generatePinNumber():
    lst = [random.randint(0, 9) for i in range(4)]
    pin = ""
    for num in lst:
        pin += str(num)
    return pin

if __name__ == '__main__':
    while True:
        try:
            createDatabase()
        except:
            b = 0
        print("1. Create an account\n2. Log into account\n0. Exit")
        u_input = int(input())
        if u_input == 1:
            print("\nYour card has been created\nYour card number:", )
            card_number = generateCardNumber()
            print(card_number, end="\n")
            print("Your card PIN:")
            pin = generatePinNumber()
            Balance = 0
            print(pin, end="\n")
            saveData(card_number, pin, Balance)
        elif u_input == 2:
            print("Enter your card number:\n")
            card_num = input()
            print("Enter your PIN:\n")
            pin_num = input()
            if checkValidity(card_num, pin_num) == None:
                print("Wrong card number or PIN!")
            else:
                print("You have successfully logged in!")
                print("1. Balance\n2. Add income\n3. Do Transfer\n4. Close Account\n5. Log out\n0. Exit\n")
                while True:
                    u_input2 = int(input())
                    if u_input2 == 1:
                        print("Balance: {}".format(getBalance(card_num)))
                    elif u_input2 == 5:
                        print("You have successfully logged out!")
                    elif u_input2 == 3:
                        doTransfer(card_num)
                    elif u_input2 == 4:
                        closeAccount(card_num)
                    elif u_input2 == 2:
                        print("Enter Deposit Amount")
                        amount = int(input())
                        addIncome(card_num, amount)
                    elif u_input2 == 0:
                        print("Bye!")
                        sys.exit()
        elif u_input == 0:
            break
    print("Bye!")

