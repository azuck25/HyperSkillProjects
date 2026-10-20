import sys


def calc_tax_rate(rate, income):
    tmp_tax_amount = rate * income
    tmp_tax_rate = tmp_tax_amount / income
    return tmp_tax_amount, tmp_tax_rate


def rent_allocation(income):
    rates = ( .33, .25, .20, .15)
    rent_schedule = []
    for i in rates:
        tmp_allowance = income * i
        rent_schedule.append(float(tmp_allowance))
    return rent_schedule


class TaxBracket:
    def __init__(self, user_income):

        self.brackets = [(0,12400, 0.10),
                         (12401,50400, 0.12),
                         (50401,105700, 0.22),
                         (105701,201775, 0.24),
                         (201776,256225, 0.32),
                         (256226,640600, 0.35),
                         (640601,9999999999, 0.37)]
        self.user_income = user_income
        self.monthly_income = user_income / 12
        self.tax_amount, self.tax_rate = self.calculate_rate_amount()
        self.after_tax_amount = self.user_income - self.tax_amount
        self.rent_allocation_gross = [*rent_allocation(self.user_income)]
        self.rent_allocation_net = [*rent_allocation(self.after_tax_amount)]


    def simple_rate_amount(self):
        tmp_income = self.user_income
        if tmp_income >= self.brackets[3][1]:
            b_num = 4
            tax_amount, tax_rate = calc_tax_rate(self.brackets[b_num-1][2],tmp_income)
            return tax_amount, tax_rate

        if tmp_income >= self.brackets[2][0]:
            b_num = 3
            tax_amount, tax_rate = calc_tax_rate(self.brackets[b_num - 1][2], tmp_income)
            return tax_amount, tax_rate

        if tmp_income >= self.brackets[1][0]:
            b_num = 2
            tax_amount, tax_rate = calc_tax_rate(self.brackets[b_num - 1][2], tmp_income)
            return tax_amount, tax_rate
        else:
            return 0,0

    def calculate_rate_amount(self):
        if self.user_income >= self.brackets[1][0]:
            tax_amount = 0.0
            tmp_income = self.user_income
            bracket_size = len(self.brackets)
            current_position = bracket_size-1
            def calculate_tax_amount(tmp_inc, bracket_num):
                def return_tax_amount(user_inc, sel):
                    inc_in_bracket = user_inc - self.brackets[bracket_num][sel]
                    tax_amt = inc_in_bracket * self.brackets[bracket_num][2]
                    return tax_amt
                if self.brackets[bracket_num][0] <= tmp_inc <= self.brackets[bracket_num][1]:
                    selector = 0
                    return return_tax_amount(tmp_inc, selector)
                else:
                    selector = 1
                    return return_tax_amount(tmp_inc, selector)
            while tmp_income > self.brackets[0][1]:
                if tmp_income > self.brackets[current_position][0]:
                    tmp_tax = calculate_tax_amount(tmp_income,current_position)
                    tax_amount += tmp_tax
                    tmp_income = self.brackets[current_position][1]
                current_position -= 1
            tax_rate = tax_amount / self.user_income
            return tax_amount, tax_rate
        else:
            return 0,0


def main():
    #user_income = int(sys.stdin.readline())
    t = TaxBracket(100000)
    print(t.user_income)
    print("Enter your current income : ", end="")
    user_income = int(input())
    tax_amount, tax_rate = TaxBracket(user_income).calculate_rate_amount()
    tax_rate  *= 100
    tax_amount = round(tax_amount)
    statement = f"Federal Income Tax for ${user_income:.2f} is {tax_rate:.2f}%. That is ${tax_amount:.2f} dollars\n"
    print(statement)
    net_income = user_income - tax_amount
    monthly_gross = float(user_income) / 12
    monthly_net = float(net_income / 12)
    print(f"Gross Income : ${user_income:.2f}")
    print(f"Net Income : ${net_income:.2f}")
    print(f"Monthly Gross Income: ${monthly_gross:.2f}")
    print(f"Monthly Net Income : ${monthly_net:.2f}\n")
    rent_allocation_gross = [*rent_allocation(monthly_gross)]
    rent_allocation_net = [*rent_allocation(monthly_net)]
    print("Monthly Rent Allocation (Gross Rate)")
    for i in rent_allocation_net:
        print(f"rate : {float(i/monthly_gross)*100:.2f}% : rent : ${float(i):.2f}")
    print("\nMonthly Rent Allocation (Net Rate / Post Tax Availability)")
    for i in rent_allocation_gross:
        print(f"rate : {float(i/monthly_net)*100:.2f}% : rent : ${float(i):.2f}")


