var clickSell = function() {
	window.location = "/sell";
}

var clickDashboard = function() {
	window.location = "/dashboard";
}

var searchRequest = function() {
	if ($('#searchf').val() != '') {
		var $form = $("#searchbar");
		var $inputs = $form.find("input");
		$inputs.prop("disabled", true);
		window.location = "/search/" + $('#searchf').val();
		return false;
	} else {
		return true;
	}
}