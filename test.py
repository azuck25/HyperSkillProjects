from card_verification import *


simulations = 25
sequence_size = 9
db = CustAccountDatabase()

# c = create_card()
# print(len(c.card_number))
c = "400000681830780"

# seq, val = luhn_algorithm(c)
# print(seq,val)
sequence = "400000848847474"
sequence1 = "400000844943340"
x = luhn_algorithm(sequence1)
print(x)