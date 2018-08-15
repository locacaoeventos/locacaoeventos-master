from locacaoeventos.apps.user.sellerprofile.models import SellerProfile
from locacaoeventos.apps.user.buyerprofile.models import BuyerProfile


def base_context(user):
	context = {}
	if not user.is_anonymous:
		sellers = SellerProfile.objects.filter(user=user)
		buyers = BuyerProfile.objects.filter(user=user)
		if sellers:
			context["seller"] = sellers[0]
			profile = sellers[0]
			context["user_type"] = "seller"
		elif buyers:
			context["buyer"] = buyers[0]
			profile = buyers[0]
			context["user_type"] = "buyer"
		context["profile"] = profile
	return context