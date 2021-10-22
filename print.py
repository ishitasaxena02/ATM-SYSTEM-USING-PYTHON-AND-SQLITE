import sqlite3
con  = sqlite3.connect('atmdb.db')
cursor = con.execute("SELECT DIGIT, BANK, MINBAL FROM BANKS")
print("BANK CODE\tBANK NAME\tMIN BALANCE")
for row in cursor:
    print(row[0],"\t\t", row[1],"\t\t", row[2])
print()
d = con.execute("SELECT * FROM BANKLIST")
print("CARD NO.\tBANK CODE\tNAME\t\tACCOUNT NO\tPIN\t\tBALANCE\t\tPIN RETRY LIMIT")
for row in d:
    print(row[0], "\t\t" , row[1], "\t\t" , row[2], "\t\t" , row[3], "\t\t" , row[4], "\t\t" , row[5], "\t\t" , row[6])
con.close()
