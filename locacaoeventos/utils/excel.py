import xlwt


def set_width_sheet(sheet, width, n_columns):
    style_gray_str = "" \
        + "align: wrap on, vert centre, horiz center;" \
        + "pattern: pattern solid, fore_colour gray25;"
    style_gray = xlwt.easyxf(style_gray_str)
    for i in range(50): # Column
        if i < n_columns:
            sheet.col(i).width = width

    for i in range(50): # Column
        if i >= n_columns:
            for j in range(500): # Lines
                sheet.write(j, i, "", style_gray)



def convert_rgba_to_list(rgba):
    rgba_new = rgba.replace("rgba(", "").replace(")", "")
    rgba_list = rgba_new.split(",")
    for i in range(len(rgba_list)):
        rgba_list[i] = int(rgba_list[i])
    return rgba_list




