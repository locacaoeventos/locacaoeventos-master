function drawInfobox(category, infoboxContent, json, i){

    if(json.data[i].color)          { var color = json.data[i].color }
        else                        { color = '' }
    if( json.data[i].price )        { var price = '<div class="price">' + json.data[i].price +  '</div>' }
        else                        { price = '' }
    if(json.data[i].id)             { var id = json.data[i].id }
        else                        { id = '' }
    if(json.data[i].url)            { var url = json.data[i].url }
        else                        { url = '' }
    if(json.data[i].type)           { var type = json.data[i].type }
        else                        { type = '' }
    if(json.data[i].title)          { var title = json.data[i].title }
        else                        { title = '' }
    if(json.data[i].location)       { var location = json.data[i].location }
        else                        { location = '' }
    if(json.data[i].gallery[0])     { var gallery = json.data[i].gallery[0] }
        else                        { gallery[0] = '../img/default-item.jpg' }
    var ibContent = '';
    var place = json.data[i];
    ibContent =
    '<div class="infobox ' + color + ' " style="width:300px">' +
        '<div class="inner">' +
            '<div class="image">' +
                '<div class="overlay">' +
                    '<div class="wrapper">' +
                        '<a href="' + url +  '" class="detail"></a>' +
                        '<hr>' +
                    '</div>' +
                '</div>' +
                '<a href="' + url +  '" class="description">' +
                    '<div class="meta" style="width:300px">' +
                        price +
                        '<h2 style="font-weight:bold; text-transform:uppercase;color:#00A9B7;">' + title +  '</h2>' +
                            '<div class="separador-5"> </div>' +
                            '<div class="row">' +
                                '<div class="col-md-12" style="line-height:16px;">' +
                                    '<i class="fa fa-home" style="position:static"></i>&nbsp;&nbsp;' + location +
                                '</div>' +
                            '</div>' +
                            '<div class="separador-5"> </div>' +
                            '<div class="row">' +
                              '<div class="col-md-6">' +
                                '<i class="fa fa-user" style="position:static"></i>&nbsp;&nbsp;' + place.capacity + ' pessoas' +
                              '</div>' +
                              '<div class="col-md-6">' +
                                '<i class="fa fa-star" style="position:static"></i>&nbsp;&nbsp;' + place.rate_average +
                              '</div>' +
                            '</div>' +
                    '</div>' +
                '</a>' +
                '<div pk="' + gallery + '" class="result_place img-center center-cropped" style="background-image: url(' + place.gallery[0] + '); width:100%; height:200px"></div>' +
            '</div>' +
        '</div>' +
    '</div>';

    return ibContent;
}