function get_url_parameter(url_string, url_parameter){
	var url = new URL(url_string);
	var url_parameter = url.searchParams.get(url_parameter);
	return url_parameter
}
