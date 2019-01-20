def buyer_can_purchase(context):
	if context["user_type"] == "buyer":
		profile = context["profile"]
		print("profile")
		print(profile)
		birthday = profile.birthday
		print("birthday")
		print(birthday)
		cellphone = profile.cellphone
		print("cellphone")
		print(cellphone)
		gender = profile.gender
		print("gender")
		print(gender)
		civil_status = profile.civil_status
		print("civil_status")
		print(civil_status)
		cpf = profile.cpf
		print("cpf")
		print(cpf)

		if birthday != None and cellphone != None and gender != None and civil_status != None and cpf != None and birthday != "" and cellphone != "" and gender != "" and civil_status != "" and cpf != "":
			return True
		else:
			return False
	return False