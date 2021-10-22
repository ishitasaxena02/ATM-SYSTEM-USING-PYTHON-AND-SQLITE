import sqlite3
import sys

def term() :
    print("YOUR TRANSACTION IS TERMINATED")

def withdraw(c) :
    print("ENTER THE AMOUNT YOU WANT TO WITHDRAW")
    a = float(input())
    if a > 50000 :
        print("TRANSACTION LIMIT EXCEEDED")
        term()
        sys.exit()
    if c[6] - a < c[0] :
        print("INSUFFICIENT BALANCE")
        term()
    else :
        print("PLEASE WAIT WHILE YOUR TRANSACTION IS BEING PROCESSED")
        c[6] = c[6] - a
        con.execute("UPDATE BANKLIST SET BAL = ? WHERE ACCNO = ?", (c[6], c[3]))
        con.commit()
        print("YOUR TRANSACTION IS COMPLETE\nDO YOU WANT TO KNOW YOUR CURRENT BALANCE?\nPRESS 1 FOR YES AND 2 FOR NO")
        y = int(input())
        if y not in [1,2] :
            sys.exit("WRONG INPUT ENTERED")
        if y == 1 :
            balance(c)

def deposit(c) :
    print("ENTER THE AMOUNT YOU WANT TO DEPOSIT")
    a = float(input())
    c[6] = c[6] + a
    con.execute("UPDATE BANKLIST SET BAL = ? WHERE ACCNO = ?", (c[6], c[3]))
    con.commit()
    print("YOUR TRANSACTION IS COMPLETE\nDO YOU WANT TO KNOW YOUR CURRENT BALANCE?\nPRESS 1 FOR YES AND 2 FOR NO")
    y = int(input())
    if y not in [1,2] :
        sys.exit("WRONG INPUT ENTERED")
    if y == 1 :
        balance(c)

def balance(c) :
    print("DEAR CUSTOMER, \nYOUR ACCOUNT BALANCE IS RS.", c[6], "ONLY")

def pinch(c) :
    print("PLEASE ENTER THE CURRENT PIN")
    p = int(input())
    if p == c[4] :
        print("PLEASE ENTER THE NEW PIN")
        a = int(input())
        if a >= 1000 and a <= 9999 :
            flag = False
            for i in range(2):
                print("PLEASE RE-ENTER THE NEW PIN")
                b = int(input())
                if a == b :
                    flag = True
                    break
                else :
                    print("PIN DOESN'T MATCH\nYOU HAVE",1-i,"ATTEMPT LEFT")
            if flag == False :
                print("PIN DOESN'T MATCH")
                term()
            else :
                con.execute("UPDATE BANKLIST SET PIN = ? WHERE ACCNO = ?", (a,c[3]))
                con.commit()
                print("PIN CHANGED SUCCESSFULLY")
        else :
            print("ENTER A 4 DIGIT NUMBER")
            term()
    else :
        print("WRONG PIN ENTERED\nPLEASE TRY AGAIN")
        term()

con = sqlite3.connect('atmdb.db')
print("WELCOME TO THIS ATM")
print("PRESS ENTER TO CONTINUE")
input()
print("PLEASE ENTER THE ATM CARD NUMBER")
n = input()
if len(n) != 4 :
    sys.exit("THIS CARD NUMBER IS INVALID. \nPLEASE ENTER THE CORRECT CARD NUMBER \nOR \nKINDLY CONTACT YOUR BANK FOR FURTHER DETAILS")
n = int(n)
cursor = con.execute("SELECT BANKS.MINBAL, BANKS.BANK, BANKLIST.NAME, BANKLIST.ACCNO, BANKLIST.PIN, BANKLIST.WRONGPIN, BANKLIST.BAL FROM BANKS INNER JOIN BANKLIST ON BANKS.DIGIT = BANKLIST.BANKID WHERE CARDNO = ?", (n,))
c = []
for row in cursor :
    c = [row[0], row[1], row[2], row[3], row[4], row[5], row[6]]
if len(c) == 0 :
    print("THIS CARD DOESN'T EXIST")
    sys.exit("KINDLY ENTER A VALID CARD NUMBER")
if c[5] == 0 :
    sys.exit("THIS CARD IS BLOCKED")
print("PLEASE ENTER THE PIN NUMBER")
t = c[5]
p = int(input())
if p != c[4] :
    t -= 1
    con.execute("UPDATE BANKLIST SET WRONGPIN = ? WHERE CARDNO = ?", (t,n))
    con.commit()
    if t != 0:
        print("THE PIN IS INCORRECT. YOU HAVE",t,"ATTEMPTS LEFT")
        sys.exit("TRY AGAIN")
    else :
        sys.exit("THE CARD IS NOW BLOCKED. CONTACT YOUR BANK FOR FURTHER DETAILS")
if t != 3 :
    con.execute("UPDATE BANKLIST SET WRONGPIN = 3 WHERE CARDNO = ?", (n,))
    con.commit()
print("HELLO", c[2], "\nWELCOME TO", c[1])
print("PLEASE ENTER THE NUMBER YOU WANT TO CHOOSE \n1. WITHDRAWAL \t\t\t\t\t2. DEPOSIT \n3. BALANCE ENQUIRY \t\t\t\t4. PIN CHANGE \n5. TERMINATE")
a = int(input())
if a not in [1,2,3,4,5] :
    sys.exit("THE OPERATION YOU WANT TO PERFORM IS INVALID\nKINDLY CHOOSE A VALID NUMBER")
if a == 1 :
    withdraw(c)
elif a == 2 :
    deposit(c)
elif a == 3 :
    balance(c)
elif a == 4 :
    pinch(c)
else :
    term()
print("THANK YOU FOR USING OUR ATM")
con.close()
