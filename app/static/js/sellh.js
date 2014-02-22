$("#submitButton").click(function(){
  var $form = $("#submitForm");
  var $inputs = $form.find("input, a, textarea");

  $inputs.prop("disabled", true);

  request = $.ajax({
  	url: "/add",
    type: "post",
    data: {
    	description: $('#descf').val(),
    	title: $('#titlef').val(),
	category: $('#category').val(),
	price: $('#pricef' ).val(),
	selltype: $('#ExchangeType').val()
    },
  });

  request.success(function (response, textStatus, jqXHR){
    window.location.replace(response);
  });

  request.fail(function (jqXHR, textStatus, errorThrown){
    $inputs.prop("disabled", false);
    alert("Whoops, something went wrong :(");
  });
});
