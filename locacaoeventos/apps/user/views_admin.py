from django.views.generic import View
from django.shortcuts import render, redirect
from django.http import HttpResponse

import xlwt, json

from locacaoeventos.utils.main import *
from locacaoeventos.utils.feature import *
from locacaoeventos.utils.excel import *

from locacaoeventos.apps.place.placecore.models import Place, PlaceFeature

class AdminHome(View):
    def get(self, request, *args, **kwargs):
        context = base_context(request.user)
        verify_place = False
        for place in Place.objects.all():
            if not place.is_authorized_by_admin:
                verify_place = True
        context["verify_place"] = verify_place
        return render(request, "admin/home.html", context)


class AdminListBuffet(View):
    def get(self, request, *args, **kwargs):
        context = base_context(request.user)
        context["place_list"] = Place.objects.all()
        return render(request, "admin/buffet_list.html", context)

class AdminVerifyBuffet(View):
    def get(self, request, *args, **kwargs):
        context = base_context(request.user)
        context["place_list"] = Place.objects.all()
        return render(request, "admin/buffet_verify.html", context)



class UploadBuffet(View):
    def get(self, request, *args, **kwargs):
        context = base_context(request.user)
        return render(request, "admin/buffet_upload.html", context)


class AdminFeaturedBuffet(View):
    def get(self, request, *args, **kwargs):
        context = base_context(request.user)
        place_list = update_feature_places()

        # Remove Creation and None, as bugs JS

        context["place_list"] = place_list
        context["place_list_js"] = json.dumps(place_list, indent=4, sort_keys=True, default=str)
        placefeature = PlaceFeature.objects.all()[0]
        context["visualization"] = {
            "factor": str(placefeature.visualization_factor).replace(",","."),
            "factor_firstday": str(placefeature.visualization_factor_firstday).replace(",","."),
        }
        context["review"] = {
            "factor": str(placefeature.review_factor).replace(",","."),
            "factor_firstday": str(placefeature.review_factor_firstday).replace(",","."),
        }


        return render(request, "admin/buffet_featured.html", context)



    def post(self, request, *args, **kwargs):
        visualization_factor = request.POST.get("visualization_factor")
        visualization_factor_firstday = request.POST.get("visualization_factor_firstday")
        review_factor = request.POST.get("review_factor_firstday")
        review_factor_firstday = request.POST.get("review_factor_firstday")

        placefeature = PlaceFeature.objects.all()[0]
        placefeature.visualization_factor = visualization_factor
        placefeature.visualization_factor_firstday = visualization_factor_firstday
        placefeature.review_factor = review_factor
        placefeature.review_factor_firstday = review_factor_firstday
        placefeature.save()


        return self.get(request, *args, **kwargs)














































































class DownloadExcelFrame(View):
    def get(self, request, *args, **kwargs):
        context = base_context(request.user)
        wb = xlwt.Workbook() # Create file


        # ============================================================================
        # Style Cells
        # ============================================================================
        xlwt.add_palette_colour("custom_colour", 0x21)
        rgba_list = convert_rgba_to_list(context["rgba_button"])
        wb.set_colour_RGB(0x21, rgba_list[0], rgba_list[1], rgba_list[2])

        style_header_str = "" \
            + "align: wrap on, vert centre, horiz center;" \
            + "font: bold on, height 200, colour white;" \
            + "pattern: pattern solid, fore_colour custom_colour;"

        style_content_str = "" \
            + "align: wrap on, vert centre, horiz center;" \
            + "font: height 160;" \

        style_header = xlwt.easyxf(style_header_str)
        style_content = xlwt.easyxf(style_content_str)



        # ========================
        # Example Sheet
        # ========================
        # Header
        example_sheet = wb.add_sheet("<exemplo_nao_editar>")


    
#creation
#modified
#is_active
#relevance
#visualization
#name
#address
#description
#capacity
#size
#video
#children_rides
#decoration
#menu








        example_sheet.write(0, 0, "<Nome do Participante>", style_header)
        example_sheet.write(0, 1, "<Celular do Participante>", style_header)
        example_sheet.write(0, 2, "<E-mail do Participante>", style_header)
        example_sheet.write(0, 3, "<CPF do Participante>", style_header)
        example_sheet.write(0, 4, "<Ano de Entrada do Participante>", style_header)
        example_sheet.write(0, 5, "<PK do Curso do Participante>", style_header)
        example_sheet.write(0, 6, "<PK do Instituto de Educação do Participante>", style_header)
        example_sheet.write(0, 7, "<Faltaram dados>", style_header)
        # Content
        example_sheet.write(1, 0, "Ex: André Carneiro", style_content)
        example_sheet.write(1, 1, "Todos caracteres especiais serão removidos, então não faz diferença do formato, desde que seja acompanhado com o (DDD) na frente; 11 dígitos", style_content)
        example_sheet.write(1, 2, "Ex: eventos@polijunior.com.br", style_content)
        example_sheet.write(1, 3, "Todos caracteres especiais serão removidos, então não faz diferença do formato 11 dígitos", style_content)
        example_sheet.write(1, 4, "Ex: 2009", style_content)
        example_sheet.write(1, 5, 'Na planilha deste arquivo, consultar o PK correspondente em "Cursos"', style_content)
        example_sheet.write(1, 6, 'Na planilha deste arquivo, consultar o PK correspondente em "Institutos de Educação"', style_content)
        example_sheet.write(1, 7, "Caso não temos dados suficientes desse participante para preencher essa planilha, marcar essa coluna (com algum caráctere)", style_content)
        set_width_sheet(example_sheet, 5000, 8)



        # ========================
        # Buffets Sheet
        # ========================
        buffet_sheet = wb.add_sheet("INSERIR")
        # Header
        buffet_sheet.write(0, 0, "Nome do Participante", style_header)
        buffet_sheet.write(0, 1, "Celular do Participante", style_header)
        buffet_sheet.write(0, 2, "E-mail do Participante", style_header)
        buffet_sheet.write(0, 3, "CPF do Participante", style_header)
        buffet_sheet.write(0, 4, "Ano de Entrada do Participante", style_header)
        buffet_sheet.write(0, 5, "PK do Curso do Participante", style_header)
        buffet_sheet.write(0, 6, "PK do Instituto de Educação do Participante", style_header)
        buffet_sheet.write(0, 7, "Faltaram dados", style_header)
        set_width_sheet(buffet_sheet, 5000, 8)














        # Final Adjustments to export
        filename = "LocacaoEventos - Importar Buffets"
        response = HttpResponse(content_type="application/force-download")
        response["Content-Disposition"] = "attachment; filename = " + filename + ".xls"
        wb.save(response)
        return response





















