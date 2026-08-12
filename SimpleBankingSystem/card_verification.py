import random as r
import sqlite3 as sql




class CustAccount:
    def __init__(self, card_number: str, card_pin: int):
        self.card_number = card_number
        self.card_pin = card_pin
        self.bank_id = card_number[:5]
        #9
        self.accountId = card_number[5:14]
        #1
        self.check_sum = card_number[15]

class CustAccountDatabase:
    def __init__(self):
        self.card_database: list[dict[str,str | int]] =  []
        self.account_database = {}

def create_card():
    card = None
    pin = create_sequence(4)
    while card is None:
        card = create_sequence(9)

    print("\nYour card has been created")
    print("Your card number: ")
    print(card)
    print("Your card PIN:")
    print(pin)
    c = CustAccount(str(card),int(pin))
    #a, z = luhn_algorithm(c.card_number)
    #print(f"sequence post function calls : {a}", f"control : {z}")
    return c

def create_sequence(seq_size: int):
    # key * mod N
    generated_seq = ""
    if seq_size == 4: sequence = ""
    else: sequence = "400000"
    for i in range(seq_size):
        generated_seq = "".join(generated_seq + str(r.randint(0,3500000) % 9))
    new_sequence = sequence + generated_seq
    if len(new_sequence) > 4:
        seq,flag = luhn_algorithm(new_sequence)
        print(f"sequence post luhn : {seq}",f"control : {flag}")
        if flag:
            return seq
        else:
            return None
    else: return generated_seq

def luhn_algorithm(sequence: str):
    running_sum = 0
    valid = False
    newString = ""
    for i,j in zip(sequence,range(1,len(sequence)+1)):
        #print(len(sequence)+1)
        temp = int(i)
        if (j%2) == 1:
            temp *= 2
        if temp > 9:
            temp -= 9
        newString = newString + str(temp)
        if j <= len(sequence): running_sum += temp
        if j == 15 and len(sequence) == 15:
            for v in range(9):
                if (running_sum + v)%10 == 0:
                    valid = True
                    sequence = sequence + str(v)
                    return sequence, valid
                elif v==9:
                    valid = False
                    return sequence, valid


        #print(f"Control at step {j}", newString)
        #print(f"Running Sum : {running_sum}")
    if (running_sum%10) == 0: valid = True
    return sequence, valid

def add_card(credit_card: CustAccount, db: CustAccountDatabase):
    dictionary_obj = {'card_number': credit_card.card_number,
                      'card_pin': credit_card.card_pin,
                      'bank_id': credit_card.bank_id,
                      'account_id': credit_card.accountId,
                      'checksum': credit_card.check_sum}

    if check_database(credit_card, db):
        #generate new key/value pair
        print("Card exists... generating new unique card")
        new_card = create_card()
        add_card(new_card,db)
    else:
        #print("Card added to database...")
        db.card_database.append(dictionary_obj)
        acct = {credit_card.accountId: 0}
        db.account_database.update(acct)
    print()


def dict_representation(credit_card: CustAccount):
    dictionary_obj = {'card_number': credit_card.card_number,
                      'card_pin': credit_card.card_pin,
                      'bank_id': credit_card.bank_id,
                      'account_id': credit_card.accountId,
                      'checksum': credit_card.check_sum}
    return dictionary_obj


def check_database(credit_card: CustAccount,db: CustAccountDatabase):
    reference = dict_representation(credit_card)
    check_condition = bool(reference in db.card_database)
    if check_condition:
        #index_loc = db.card_database.index(reference)
        #print("Card Found at index : ", index_loc)
        return True
    else:
        #print("Card not found")
        return False

def login_function(card_number: str, card_pin: str, db: CustAccountDatabase):
    temp_card = CustAccount(card_number,int(card_pin))
    if check_database(temp_card, db):
        logged_in = True
        print("\nYou have successfully logged in!\n")
        while logged_in:
            print("1. Balance")
            print("2. Log out")
            print("0. Exit")
            user_input = int(input(">"))
            match user_input:
                case 1:
                        print("Balance : ", db.account_database[temp_card.accountId],"\n")
                case 2:
                        print("\nYou have successfully logged out!\n")

                        return
                case 0:
                        print("\nBye!")
                        exit()
    else:
        print("Wrong card number or PIN!\n")


def main():

    program_active = True
    database = CustAccountDatabase()

    while program_active:

        print("1. Create an account")
        print("2. Log into account")
        print("0. Exit")
        user_input = int(input(">"))

        match user_input:
            case 1:
                credit_card = create_card()
                add_card(credit_card,database)
                #print("verified added : ", check_database(credit_card,database))
            case 2:
                print("Enter your card number : ")
                temp_num = str(input(">"))
                print("Enter your pin : ")
                temp_pin = str(input(">"))
                if len(temp_num) == 16 and str(temp_num):
                    login_function(temp_num,temp_pin,database)
                else:
                    print("\nWrong card number or PIN!\n")
            case 0:
                print("\nBye!")
                exit()

main()