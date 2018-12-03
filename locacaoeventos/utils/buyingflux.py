from django.conf import settings
import pagarme, datetime

from locacaoeventos.apps.user.sellerprofile.models import SellerProfile
from locacaoeventos.apps.place.placecore.models import Place


def get_account_types():
    return [
        {
            "name": "Conta Corrente",
            "code": "conta_corrente",
        },
        {
            "name": "Conta Poupança",
            "code": "conta_poupanca",
        },
    ]

def check_seller_has_finished_payment(seller_pk, bank_code, agency, account, account_type):
    seller = SellerProfile.objects.get(pk=seller_pk)
    has_finished_payment = True
    if bank_code == None:
        if seller.bank_code == "":
            has_finished_payment = False
        if seller.agency == "":
            has_finished_payment = False
        if seller.account == "":
            has_finished_payment = False
        if seller.account_type == "":
            has_finished_payment = False
        pagarme_id = ""
    # on POST
    else:
        if bank_code == "":
            has_finished_payment = False
        if agency == "":
            has_finished_payment = False
        if account == "":
            has_finished_payment = False
        if account_type == "":
            has_finished_payment = False

        if has_finished_payment == True:
            new_recipient = False
            if seller.bank_code != bank_code:
                new_recipient = True
            if seller.agency != agency:
                new_recipient = True
            if seller.account != account:
                new_recipient = True
            if seller.account_type != account_type:
                new_recipient = True

            # Create PagarMe Recipient
            if new_recipient == True:
                pagarme.authentication_key(settings.PAGARME_API_KEY)

                now = datetime.datetime.now()
            # Criar Recebedor
                params = {
                    'anticipatable_volume_percentage': '0',
                    'automatic_anticipation_enabled': 'false',
                    'transfer_day': '0',
                    'transfer_enabled': 'false',
                    'transfer_interval': 'daily',
                    'bank_account':{
                        'agencia': str(agency),
                        'agencia_dv': '5',
                        'bank_code': str(bank_code),
                        'conta': str(account),
                        'conta_dv': '1',
                        'document_number': int(str(seller.cpf).replace(".","").replace("/","").replace("-","")),
                        'legal_name': str(seller.pk) + " " + str(now.year) + "-" + str(now.month) + "-" + str(now.day) + "-" + str(now.hour) + "-" + str(now.minute) + "-" + str(now.second)
                    }
                }

                recipient = pagarme.recipient.create(params)
                pagarme_id = recipient["id"]
        else:
            pagarme_id = ""
    

    seller.has_finished_payment = has_finished_payment
    seller.save()


    places = Place.objects.filter(sellerprofile=seller).update(has_finished_payment=has_finished_payment)
    return [has_finished_payment, pagarme_id]

def get_bank_codes():
    return [
        {
            "name": "01 - Banco do Brasil S.A.",
            "code": "001"
        },
        {
            "name": "03 - Banco da Amazônia S.A.",
            "code": "003"
        },
        {
            "name": "04 - Banco do Nordeste do Brasil S.A.",
            "code": "004"
        },
        {
            "name": "07 - Banco Nacional de Desenvolvimento Econômico e Social – BNDES",
            "code": "007"
        },
        {
            "name": "10 - Credicoamo Crédito Rural Cooperativa",
            "code": "010"
        },
        {
            "name": "11 - Credit Suisse Hedging-Griffo Corretora de Valores S.A.",
            "code": "011"
        },
        {
            "name": "12 - Banco Inbursa S.A.",
            "code": "012"
        },
        {
            "name": "14 - Natixis Brasil S.A. Banco Múltiplo",
            "code": "014"
        },
        {
            "name": "15 - UBS Brasil Corretora de Câmbio, Títulos e Valores Mobiliários S.A.",
            "code": "015"
        },
        {
            "name": "16 - Cooperativa de Crédito Mútuo dos Despachantes de Trânsito de Sta.Catarina e RS",
            "code": "016"
        },
        {
            "name": "17 - BNY Mellon Banco S.A.",
            "code": "017"
        },
        {
            "name": "18 - Banco Tricury S.A.",
            "code": "018"
        },
        {
            "name": "21 - Banco do Estado do Espírito Santo – Baneste S.A.",
            "code": "021"
        },
        {
            "name": "24 - Banco Bandepe S.A.",
            "code": "024"
        },
        {
            "name": "25 - Banco Alfa S.A.",
            "code": "025"
        },
        {
            "name": "29 - Banco Itaú Consignado S.A.",
            "code": "029"
        },
        {
            "name": "33 - Banco Santander (Brasil) S.A.",
            "code": "033"
        },
        {
            "name": "36 - Banco Bradesco BBI S.A.",
            "code": "036"
        },
        {
            "name": "37 - Banco do Estado do Pará S.A.",
            "code": "037"
        },
        {
            "name": "40 - Banco Cargill S.A.",
            "code": "040"
        },
        {
            "name": "41 - Banco do Estado do Rio Grande do Sul S.A.",
            "code": "041"
        },
        {
            "name": "47 - Banco do Estado de Sergipe S.A.",
            "code": "047"
        },
        {
            "name": "60 - Confidence Corretora de Câmbio S.A.",
            "code": "060"
        },
        {
            "name": "62 - Hipercard Banco Múltiplo S.A.",
            "code": "062"
        },
        {
            "name": "63 - Banco Bradescard S.A.",
            "code": "063"
        },
        {
            "name": "64 - Goldman Sachs do Brasil Banco Múltiplo S.A.",
            "code": "064"
        },
        {
            "name": "65 - Banco Andbank (Brasil) S.A.",
            "code": "065"
        },
        {
            "name": "66 - Banco Morgan Stanley S.A.",
            "code": "066"
        },
        {
            "name": "69 - Banco Crefisa S.A.",
            "code": "069"
        },
        {
            "name": "70 - Banco de Brasília S.A. (BRB)",
            "code": "070"
        },
        {
            "name": "74 - Banco J. Safra S.A.",
            "code": "074"
        },
        {
            "name": "75 - Banco ABN Amro S.A.",
            "code": "075"
        },
        {
            "name": "76 - Banco KDB S.A.",
            "code": "076"
        },
        {
            "name": "77 - Banco Inter S.A.",
            "code": "077"
        },
        {
            "name": "78 - Haitong Banco de Investimento do Brasil S.A. ",
            "code": "078"
        },
        {
            "name": "79 - Banco Original do Agronegócio S.A.",
            "code": "079"
        },
        {
            "name": "80 - BT Corretora de Câmbio Ltda. ",
            "code": "080"
        },
        {
            "name": "81 - Banco Brasileiro de Negócios S.A. – BBN",
            "code": "081"
        },
        {
            "name": "82 - Banco Topázio S.A.",
            "code": "082"
        },
        {
            "name": "83 - Banco da China Brasil S.A.",
            "code": "083"
        },
        {
            "name": "84 - Uniprime Norte do Paraná – Cooperativa de Crédito Ltda. ",
            "code": "084"
        },
        {
            "name": "85 - Cooperativa Central de Crédito Urbano – Cecred",
            "code": "085"
        },
        {
            "name": "88 - Banco Randon S.A.",
            "code": "088"
        },
        {
            "name": "89 - Cooperativa de Crédito Rural da Região da Mogiana",
            "code": "089"
        },
        {
            "name": "91 - Central de Cooperativas de Economia e Crédito Mútuo do Estado RS – Unicred ",
            "code": "091"
        },
        {
            "name": "92 - Brickell (BRK) S.A. Crédito, Financiamento e Investimento",
            "code": "092"
        },
        {
            "name": "93 - Pólocred Sociedade de Crédito ao Microempreendedor e Empresa de Pequeno Porte",
            "code": "093"
        },
        {
            "name": "94 - Banco Finaxis S.A.",
            "code": "094"
        },
        {
            "name": "95 - Banco Confidence de Câmbio S.A.",
            "code": "095"
        },
        {
            "name": "96 - Banco BM&FBovespa",
            "code": "096"
        },
        {
            "name": "97 - Cooperativa Central de Crédito Noroeste Brasileiro Ltda. (CentralCredi)",
            "code": "097"
        },
        {
            "name": "99 - Uniprime Central – Central Interestadual de Cooperativas de Crédito Ltda.",
            "code": "099"
        },
        {
            "name": "100 - Planner Corretora de Valores S.A.",
            "code": "100"
        },
        {
            "name": "101 - Renascença Distribuidora de Títulos e Valores Mobiliários Ltda. ",
            "code": "101"
        },
        {
            "name": "102 - XP Investimentos Corretora de Câmbio, Títulos e Valores Mobiliários S/A",
            "code": "102"
        },
        {
            "name": "104 - Caixa Econômica Federal",
            "code": "104"
        },
        {
            "name": "105 - Lecca Crédito, Financiamento e Investimento S/A",
            "code": "105"
        },
        {
            "name": "107 - Banco Bocom BBM S.A. ",
            "code": "107"
        },
        {
            "name": "108 - PortoCred S.A. Crédito, Financiamento e Investimento",
            "code": "108"
        },
        {
            "name": "111 - Oliveira Trust Distribuidora de Títulos e Valores Mobiliários S.A. ",
            "code": "111"
        },
        {
            "name": "113 - Magliano S.A. Corretora de Cambio e Valores Mobiliarios ",
            "code": "113"
        },
        {
            "name": "114 - Central Cooperativa de Crédito no Estado do Espírito Santo – CECOOP",
            "code": "114"
        },
        {
            "name": "117 - Advanced Corretora de Câmbio Ltda. ",
            "code": "117"
        },
        {
            "name": "118 - Standard Chartered Bank (Brasil) S.A. Banco de Investimento",
            "code": "118"
        },
        {
            "name": "119 - Banco Western Union do Brasil S.A.",
            "code": "119"
        },
        {
            "name": "120 - Banco Rodobens S.A.",
            "code": "120"
        },
        {
            "name": "121 - Banco Agibank S.A.",
            "code": "121"
        },
        {
            "name": "122 - Banco Bradesco BERJ S.A.",
            "code": "122"
        },
        {
            "name": "124 - Banco Woori Bank do Brasil S.A.",
            "code": "124"
        },
        {
            "name": "125 - Banco Brasil Plural S.A. – Banco Múltiplo",
            "code": "125"
        },
        {
            "name": "126 - BR Partners Banco de Investimento S.A. ",
            "code": "126"
        },
        {
            "name": "127 - Codepe Corretora de Valores e Câmbio S.A. ",
            "code": "127"
        },
        {
            "name": "128 - MS Bank S.A. Banco de Câmbio",
            "code": "128"
        },
        {
            "name": "129 - UBS Brasil Banco de Investimento S.A.",
            "code": "129"
        },
        {
            "name": "130 - Caruana S.A. Sociedade de Crédito, Financiamento e Investimento ",
            "code": "130"
        },
        {
            "name": "131 - Tullett Prebon Brasil Corretora de Valores e Câmbio Ltda. ",
            "code": "131"
        },
        {
            "name": "132 - ICBC do Brasil Banco Múltiplo S.A.",
            "code": "132"
        },
        {
            "name": "133 - Cresol – Confederação Nacional Cooperativas Centrais de Crédito e Econ Familiar",
            "code": "133"
        },
        {
            "name": "134 - BGC Liquidez Distribuidora de Títulos e Valores Mobiliários Ltda. ",
            "code": "134"
        },
        {
            "name": "135 - Gradual Corretora de Câmbio, Títulos e Valores Mobiliários S.A. ",
            "code": "135"
        },
        {
            "name": "136 - Confederação Nacional das Cooperativas Centrais Unicred Ltda (Unicred do Brasil)",
            "code": "136"
        },
        {
            "name": "137 - Multimoney Corretora de Câmbio Ltda",
            "code": "137"
        },
        {
            "name": "138 - Get Money Corretora de Câmbio S.A.",
            "code": "138"
        },
        {
            "name": "139 - Intesa Sanpaolo Brasil S.A. – Banco Múltiplo",
            "code": "139"
        },
        {
            "name": "140 - Easynvest – Título Corretora de Valores SA ",
            "code": "140"
        },
        {
            "name": "142 - Broker Brasil Corretora de Câmbio Ltda. ",
            "code": "142"
        },
        {
            "name": "143 - Treviso Corretora de Câmbio S.A. ",
            "code": "143"
        },
        {
            "name": "144 - Bexs Banco de Câmbio S.A. ",
            "code": "144"
        },
        {
            "name": "145 - Levycam – Corretora de Câmbio e Valores Ltda. ",
            "code": "145"
        },
        {
            "name": "146 - Guitta Corretora de Câmbio Ltda. ",
            "code": "146"
        },
        {
            "name": "149 - Facta Financeira S.A. – Crédito Financiamento e Investimento",
            "code": "149"
        },
        {
            "name": "157 - ICAP do Brasil Corretora de Títulos e Valores Mobiliários Ltda. ",
            "code": "157"
        },
        {
            "name": "159 - Casa do Crédito S.A. Sociedade de Crédito ao Microempreendedor",
            "code": "159"
        },
        {
            "name": "163 - Commerzbank Brasil S.A. – Banco Múltiplo",
            "code": "163"
        },
        {
            "name": "169 - Banco Olé Bonsucesso Consignado S.A.",
            "code": "169"
        },
        {
            "name": "172 - Albatross Corretora de Câmbio e Valores S.A ",
            "code": "172"
        },
        {
            "name": "173 - BRL Trust Distribuidora de Títulos e Valores Mobiliários S.A. ",
            "code": "173"
        },
        {
            "name": "174 - Pernambucanas Financiadora S.A. Crédito, Financiamento e Investimento",
            "code": "174"
        },
        {
            "name": "177 - Guide Investimentos S.A. Corretora de Valores",
            "code": "177"
        },
        {
            "name": "182 - Dacasa Financeira S/A – Sociedade de Crédito, Financiamento e Investimento ",
            "code": "182"
        },
        {
            "name": "183 - Socred S.A. – Sociedade de Crédito ao Microempreendedor",
            "code": "183"
        },
        {
            "name": "184 - Banco Itaú BBA S.A.",
            "code": "184"
        },
        {
            "name": "188 - Ativa Investimentos S.A. Corretora de Títulos Câmbio e Valores",
            "code": "188"
        },
        {
            "name": "189 - HS Financeira S/A Crédito, Financiamento e Investimentos",
            "code": "189"
        },
        {
            "name": "190 - Servicoop – Cooperativa de Economia e Crédito Mútuo dos Servidores Públicos Estaduais do Rio",
            "code": "190"
        },
        {
            "name": "191 - Nova Futura Corretora de Títulos e Valores Mobiliários Ltda. ",
            "code": "191"
        },
        {
            "name": "194 - Parmetal Distribuidora de Títulos e Valores Mobiliários Ltda. ",
            "code": "194"
        },
        {
            "name": "196 - Fair Corretora de Câmbio S.A. ",
            "code": "196"
        },
        {
            "name": "197 - Stone Pagamentos S.A. ",
            "code": "197"
        },
        {
            "name": "204 - Banco Bradesco Cartões S.A.",
            "code": "204"
        },
        {
            "name": "208 - Banco BTG Pactual S.A.",
            "code": "208"
        },
        {
            "name": "212 - Banco Original S.A.",
            "code": "212"
        },
        {
            "name": "213 - Banco Arbi S.A.",
            "code": "213"
        },
        {
            "name": "217 - Banco John Deere S.A.",
            "code": "217"
        },
        {
            "name": "218 - Banco BS2 S.A.",
            "code": "218"
        },
        {
            "name": "222 - Banco Credit Agricole Brasil S.A.",
            "code": "222"
        },
        {
            "name": "224 - Banco Fibra S.A.",
            "code": "224"
        },
        {
            "name": "233 - Banco Cifra S.A.",
            "code": "233"
        },
        {
            "name": "237 - Banco Bradesco S.A.",
            "code": "237"
        },
        {
            "name": "241 - Banco Clássico S.A.",
            "code": "241"
        },
        {
            "name": "243 - Banco Máxima S.A.",
            "code": "243"
        },
        {
            "name": "246 - Banco ABC Brasil S.A.",
            "code": "246"
        },
        {
            "name": "248 - Banco Boavista Interatlântico S.A.",
            "code": "248"
        },
        {
            "name": "249 - Banco Investcred Unibanco S.A.",
            "code": "249"
        },
        {
            "name": "250 - Banco de Crédito e Varejo S.A. – BCV",
            "code": "250"
        },
        {
            "name": "253 - Bexs Corretora de Câmbio S.A.",
            "code": "253"
        },
        {
            "name": "254 - Paraná Banco S.A.",
            "code": "254"
        },
        {
            "name": "260 - Nu Pagamentos S.A",
            "code": "260"
        },
        {
            "name": "265 - Banco Fator S.A.",
            "code": "265"
        },
        {
            "name": "266 - Banco Cédula S.A.",
            "code": "266"
        },
        {
            "name": "268 - Barigui Companhia Hipotecária",
            "code": "268"
        },
        {
            "name": "269 - HSBC Brasil S.A. Banco de Investimento",
            "code": "269"
        },
        {
            "name": "271 - IB Corretora de Câmbio, Títulos e Valores Mobiliários Ltda. ",
            "code": "271"
        },
        {
            "name": "300 - Banco de La Nacion Argentina",
            "code": "300"
        },
        {
            "name": "318 - Banco BMG S.A.",
            "code": "318"
        },
        {
            "name": "320 - China Construction Bank (Brasil) Banco Múltiplo S.A.",
            "code": "320"
        },
        {
            "name": "341 - Banco Itaú Unibanco S.A.",
            "code": "341"
        },
        {
            "name": "366 - Banco Société Générale Brasil S.A.",
            "code": "366"
        },
        {
            "name": "370 - Banco Mizuho do Brasil S.A.",
            "code": "370"
        },
        {
            "name": "376 - Banco J. P. Morgan S.A.",
            "code": "376"
        },
        {
            "name": "389 - Banco Mercantil do Brasil S.A.",
            "code": "389"
        },
        {
            "name": "394 - Banco Bradesco Financiamentos S.A.",
            "code": "394"
        },
        {
            "name": "399 - Kirton Bank S.A. (Banco Múltiplo)",
            "code": "399"
        },
        {
            "name": "412 - Banco Capital S.A.",
            "code": "412"
        },
        {
            "name": "422 - Banco Safra S.A.",
            "code": "422"
        },
        {
            "name": "456 - Banco MUFG Brasil S.A.",
            "code": "456"
        },
        {
            "name": "464 - Banco Sumitomo Mitsui Brasileiro S.A.",
            "code": "464"
        },
        {
            "name": "473 - Banco Caixa Geral – Brasil S.A.",
            "code": "473"
        },
        {
            "name": "477 - Citibank N.A.",
            "code": "477"
        },
        {
            "name": "479 - Banco ItauBank S.A",
            "code": "479"
        },
        {
            "name": "487 - Deutsche Bank S.A. – Banco Alemão",
            "code": "487"
        },
        {
            "name": "488 - JPMorgan Chase Bank, National Association",
            "code": "488"
        },
        {
            "name": "492 - ING Bank N.V.",
            "code": "492"
        },
        {
            "name": "494 - Banco de La Republica Oriental del Uruguay",
            "code": "494"
        },
        {
            "name": "495 - Banco de La Provincia de Buenos Aires",
            "code": "495"
        },
        {
            "name": "505 - Banco Credit Suisse (Brasil) S.A.",
            "code": "505"
        },
        {
            "name": "505 - Banco de Investimento Credit Suisse (Brasil) S.A.",
            "code": "505"
        },
        {
            "name": "545 - Senso Corretora de Câmbio e Valores Mobiliários S.A. ",
            "code": "545"
        },
        {
            "name": "600 - Banco Luso Brasileiro S.A.",
            "code": "600"
        },
        {
            "name": "604 - Banco Industrial do Brasil S.A.",
            "code": "604"
        },
        {
            "name": "610 - Banco VR S.A.",
            "code": "610"
        },
        {
            "name": "611 - Banco Paulista S.A.",
            "code": "611"
        },
        {
            "name": "612 - Banco Guanabara S.A.",
            "code": "612"
        },
        {
            "name": "613 - Omni Banco S.A. ",
            "code": "613"
        },
        {
            "name": "623 - Banco Pan S.A.",
            "code": "623"
        },
        {
            "name": "626 - Banco Ficsa S.A.",
            "code": "626"
        },
        {
            "name": "630 - Banco Intercap S.A.",
            "code": "630"
        },
        {
            "name": "633 - Banco Rendimento S.A.",
            "code": "633"
        },
        {
            "name": "634 - Banco Triângulo S.A.",
            "code": "634"
        },
        {
            "name": "637 - Banco Sofisa S.A.",
            "code": "637"
        },
        {
            "name": "641 - Banco Alvorada S.A.",
            "code": "641"
        },
        {
            "name": "643 - Banco Pine S.A.",
            "code": "643"
        },
        {
            "name": "652 - Banco Itaú Unibanco Holding S.A.",
            "code": "652"
        },
        {
            "name": "653 - Banco Indusval S.A.",
            "code": "653"
        },
        {
            "name": "654 - Banco A.J. Renner S.A.",
            "code": "654"
        },
        {
            "name": "655 - Banco Votorantim S.A.",
            "code": "655"
        },
        {
            "name": "707 - Banco Daycoval S.A.",
            "code": "707"
        },
        {
            "name": "712 - Banco Ourinvest S.A.",
            "code": "712"
        },
        {
            "name": "719 - Banco Internacional do Funchal (Brasil) S.A. – Banif",
            "code": "719"
        },
        {
            "name": "735 - Banco Neon S.A.",
            "code": "735"
        },
        {
            "name": "739 - Banco Cetelem S.A.",
            "code": "739"
        },
        {
            "name": "740 - Banco Barclays S.A.",
            "code": "740"
        },
        {
            "name": "741 - Banco Ribeirão Preto S.A.",
            "code": "741"
        },
        {
            "name": "743 - Banco Semear S.A.",
            "code": "743"
        },
        {
            "name": "745 - Banco Citibank S.A.",
            "code": "745"
        },
        {
            "name": "746 - Banco Modal S.A.",
            "code": "746"
        },
        {
            "name": "747 - Banco Rabobank International Brasil S.A.",
            "code": "747"
        },
        {
            "name": "748 - Banco Cooperativo Sicredi S.A.",
            "code": "748"
        },
        {
            "name": "751 - Scotiabank Brasil S.A. Banco Múltiplo",
            "code": "751"
        },
        {
            "name": "752 - Banco BNP Paribas Brasil S.A.",
            "code": "752"
        },
        {
            "name": "753 - Novo Banco Continental S.A. – Banco Múltiplo",
            "code": "753"
        },
        {
            "name": "754 - Banco Sistema S.A.",
            "code": "754"
        },
        {
            "name": "755 - Bank of America Merrill Lynch Banco Múltiplo S.A.",
            "code": "755"
        },
        {
            "name": "756 - Banco Cooperativo do Brasil S.A. – Bancoob",
            "code": "756"
        },
        {
            "name": "757 - Banco Keb Hana do Brasil S.A.",
            "code": "757"
        }
    ]


