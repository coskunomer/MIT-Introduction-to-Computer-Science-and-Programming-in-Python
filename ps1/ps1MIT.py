def calc_profit(salary):
    profit = salary
    i = 1
    while i < 36:
        if i % 6 != 0:
            profit += profit * (0.04 / 12) + salary
            i += 1
        else:
            salary = salary * 1.07
            profit += profit * (0.04 / 12) + salary
            i += 1
    return profit
income = calc_profit(float(float(input("Enter the starting salary: ")) / 12))
down_payment = float(250000)
st, end = float(0), float(100)
rate = float(50)
c = 1
ct = 0
total = 0
while abs(total - down_payment) > float(100):
    total = income * rate
    if total < down_payment:
        st = rate
        rate = (st + end) / 2.0
    else:
        end = rate
        rate = (st + end) / 2.0
    ct += 1
if rate > 1: print("It is not possible to pay the down payment in three years.")
else:
    print("{:.4f}".format(rate))
    print(ct)
