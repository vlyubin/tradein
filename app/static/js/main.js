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
var user = {};

$(function(){
	request = $.ajax({
		url: "/user",
		type: "get",
	});

	request.success(function (response, textStatus, jqXHR){
		console.log(response);
		if (response.user.name) {
			user = response.user
			$('#user-notice').append("Signed in as " + response.user.name);
		} else {
			user = response.user
		}
	});

	request.fail(function (jqXHR, textStatus, errorThrown){
		console.log("Error getting user :("); // Can happen if token expired. We don't force user
		// to login again unless they go to dashboard or sell pages
	});
});
