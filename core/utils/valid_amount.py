def valid_amount(amount):
	if amount == 0:
		return False
		
	if len(str(amount)) >= 2:
		amount = int(str(amount)[len(str(amount))-2:])

	if amount % 3 == 0 or amount % 5 == 0:
		return True

	return False