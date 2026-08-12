import sys


def calc_tax_rate(rate, income):
    tmp_tax_amount = rate * income
    tmp_tax_rate = tmp_tax_amount / income
    return tmp_tax_amount, tmp_tax_rate


class TaxBracket:
    def __init__(self, user_income):
        self.rates = [0.0,
                      0.15,
                      0.25,
                      0.28]

        self.brackets = [(0,15527),
                         (15528,42707),
                         (42708,132406),
                         (0,132407)]
        self.user_income = user_income

    def progressive_rate_amount(self):
        tmp_income = self.user_income
        if tmp_income >= self.brackets[3][1]:
            b_num = 4
            tax_amount, tax_rate = calc_tax_rate(self.rates[b_num-1],tmp_income)
            return tax_amount, tax_rate

        if tmp_income >= self.brackets[2][0]:
            b_num = 3
            tax_amount, tax_rate = calc_tax_rate(self.rates[b_num - 1], tmp_income)
            return tax_amount, tax_rate

        if tmp_income >= self.brackets[1][0]:
            b_num = 2
            tax_amount, tax_rate = calc_tax_rate(self.rates[b_num - 1], tmp_income)
            return tax_amount, tax_rate
        else:
            return 0,0

    def calculate_rate_amount(self):
        if self.user_income >= self.brackets[1][0]:
            tax_amount = 0.0
            tmp_income = self.user_income

            def calculate_tax_amount(tmp_inc, bracket_num):
                def return_tax_amount(user_inc, sel):
                    inc_in_bracket = user_inc - self.brackets[bracket_num - 1][sel]
                    tax_amt = inc_in_bracket * self.rates[bracket_num - 1]
                    return tax_amt
                if self.brackets[bracket_num - 1][0] <= tmp_inc <= self.brackets[bracket_num - 1][1]:
                    selector = 0
                    return return_tax_amount(tmp_inc, selector)
                else:
                    selector = 1
                    return return_tax_amount(tmp_inc, selector)
            while tmp_income > self.brackets[0][1]:
                if tmp_income > self.brackets[3][1]:
                    b_num = 4
                    tmp_tax = calculate_tax_amount(tmp_income, b_num)
                    tax_amount += tmp_tax
                    tmp_income = self.brackets[2][1]
                if tmp_income >= self.brackets[2][0]:
                    b_num = 3
                    tmp_tax = calculate_tax_amount(tmp_income,b_num)
                    tax_amount += tmp_tax
                    tmp_income = self.brackets[1][1]
                if tmp_income >= self.brackets[1][0]:
                    b_num = 2
                    tmp_tax = calculate_tax_amount(tmp_income,b_num)
                    tax_amount += tmp_tax
                    tmp_income = self.brackets[0][1]
            tax_rate = tax_amount / self.user_income
            return tax_amount, tax_rate
        else:
            return 0,0


def main():
    #user_income = int(sys.stdin.readline())
    user_income = int(input())
    tax_amount, tax_rate = TaxBracket(user_income).progressive_rate_amount()
    tax_rate  *= 100
    tax_rate = int(tax_rate)
    tax_amount = round(tax_amount)
    statement = f"The tax for {user_income} is {tax_rate}%. That is {int(tax_amount)} dollars!"
    print(statement)


main()