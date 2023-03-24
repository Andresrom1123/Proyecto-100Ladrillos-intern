def valid_amount(amount):
	bills = [50, 10, 5, 3]
	if amount == 0: return False
		
	if len(str(amount)) >= 2:
		amount = int(str(amount)[len(str(amount))-2:])

	if amount % 3 == 0 or amount % 5 == 0:
		return True

	numbers_are_valid = []
	for x in range(len(str(amount)) -1 , -1, -1):
		number = int(str(amount)[::-1][x]+ '0'*x)
		number_in_bills = any([number % bill == 0 for bill in bills])
		if number_in_bills or number == 8:
			numbers_are_valid.append(True)    
			continue
		else:
			return False
	return False if not all(numbers_are_valid) else True

def withdraw_amount(amount):
    bills = [200, 100, 50, 10, 5, 3]
    dict_bills = {}
    
    for x in range(len(str(amount)) -1 , -1, -1):
        number = int(str(amount)[::-1][x]+ '0'*x)

        if number == 0: break
        
        if amount in list(range(1, 30)) and amount % 3 == 0:
            dict_bills[3] = amount // 3
            break
        
        if number == 8:
            dict_bills[3] = 1
            dict_bills[5] = 1
            break
        
        for bill in bills:
            if number % bill == 0:
                if not bill in dict_bills.keys():
                    dict_bills[bill] = number // bill
                    break
                else:
                    dict_bills[bill] += number // bill
                    break

    return dict_bills
