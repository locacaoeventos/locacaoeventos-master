function create_card(pk, photo, name, price_min, address) {
	var card = '<div style="width:100%;height:300px; border-bottom:1px solid #00A9B7;" pk='+pk+'>'+
			'<div style="width:100%; height:150px; background-image:url(/media/'+photo+'); background-size:cover"> </div>'+
			'<div class="separador-10"> </div>'+
			'<div style="width:100%">'+
				'<div style="font-weight:bold; text-transform:uppercase; font-size:18px; color:#00A9B7;">'+name+'</div>'+
				'<div class="separador-10"> </div>'+
				'<div class="row">'+
					'<div class="col-md-12" style="font-size:12px; color:#5E6164;min-height:40px">'+
						'<i class="fa fa-map-marker" style="font-size:22px;vertical-align:middle;color:#00A9B7"></i>'+
						'&nbsp;'+address+
					'</div>'+
				'</div>'+
				'<div class="separador-10"> </div>'+
				'<div class="row">'+
					'<div class="col-md-6" style="font-size:12px; color:#5E6164;">'+
						'<i class="fa fa-usd" style="font-size:22px;vertical-align:middle;color:#00A9B7"></i>'+
						'&nbsp;'+price_min+
					'</div>'+
					'<div class="col-md-6" style="font-size:12px; color:#5E6164;">'+
						'<i class="fa fa-star" style="font-size:22px;vertical-align:middle;color:#00A9B7"></i>'+
						'&nbsp;'+rating+
					'</div>'+
				'</div>'+
			'</div>'+
				'<div style=""></div>'+
		'</div>'
	return card	
}
