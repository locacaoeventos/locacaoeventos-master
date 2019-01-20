def buyer_can_purchase(context):
	if context["user_type"] == "buyer":
		profile = context["profile"]
		birthday = profile.birthday
		cellphone = profile.cellphone
		gender = profile.gender
		civil_status = profile.civil_status
		cpf = profile.cpf

		if birthday != None and cellphone != None and gender != None and civil_status != None and cpf != None and birthday != "" and cellphone != "" and gender != "" and civil_status != "" and cpf != "":
			return True
		else:
			return False
	return False