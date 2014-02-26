var IMG;

$(document).ready(function(){
	var thumbnails = $("#thumbnails");
	var submitCallback;
	var completeCallback;
	new AjaxUpload('imageUpload', {
		action: $('form#imageUploadForm').attr('action'),
		name: 'image',
		onSubmit: function(file, extension) {
			if(submitCallback) {
				submitCallback();
			}
		},
		onComplete: function(file, response) {
			response = JSON.parse(response);
			if(response.error) {
				alert("Upload error " + response.error);
			}
			else if(completeCallback) {
				completeCallback(response.file)
			}
		}
	});

	IMG = {
		submit: function(func) {
			submitCallback = func;
		},
		complete: function(func) {
			completeCallback = func;
		}
	};
});