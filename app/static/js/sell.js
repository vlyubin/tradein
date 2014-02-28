var SELL;

$(document).ready(function(){
	var $thumbs = $("#thumbnails");
	var $form = $("#submitForm");

	$(".sellInput").focus(function() {
		$("#errorLabel").html("&nbsp;");
	});

	$("#submitButton").click(function(){

		if ($("#titlef").val() == '' || $("#categoryf").val() == '' ||
				$("#descf").val() == '' || $("#pricef").val() == '') {
			$("#errorLabel").html("Error! One of the mandatory fields was left empty!");
			return;
		}

		var images = getImages();
		var data = {
					desc: $('#descf').val(),
					title: $('#titlef').val(),
					category: $('#categoryf').val(),
					price: $('#pricef').val(),
					imglist: images.join(),
					imgcount: images.length
				};
		if ($('#addedit').val() === 'add') {
			request = $.ajax({
				url: '/add',
				type: "post",
				data: data,
			});
		} else {
			request = $.ajax({
				url: '/edit/' + $('#productId').val(),
				type: "post",
				data: data,
			});
		}

		request.success(function (response, textStatus, jqXHR){
			window.location.assign(response);
		});

		request.fail(function (jqXHR, textStatus, errorThrown){
			alert("Something went wrong :(");
		});
	});

	function addImage(file_url) {
		if(!file_url || file_url.trim() == "") {
			return;
		}
		var div = $("<div/>", {class: "panel panel-default"});
		var title = $("<div/>", {class: "panel-heading"})
			.append($("<a/>", {href: file_url, text: "[Full picture]", target: "_blank"}))
			.append(" - ")
			.append($("<a/>", {href: "#", text: "[Remove]"}).click(
				function(event){
					$(this).parent().parent().remove();
					event.preventDefault();
				}));
		var body = $("<div/>")
			.append($("<img/>", {class: "panel-body", src: file_url, style: "max-width:400px; max-height:300px;"}));
		div.append(title);
		div.append(body);
		$thumbs.append(div);
	}

	function getImages() {
		var images = new Array();
		$thumbs.find("img").each(function() {
			images.push($(this).attr("src"));
		});
		return images;
	}

	IMG.submit(function() {
		//TODO: Show uploading progress bar or something
	});

	IMG.complete(function(file_url) {
		//TODO: Hide uploading progress bar
		addImage(file_url);
	});

	SELL = {
		addImage : addImage
	};
});