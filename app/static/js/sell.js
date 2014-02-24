$("#submitButton").click(function(){
  var $form = $("#submitForm");
  
  if ($('#addedit').val() === 'add') {
    request = $.ajax({
      url: '/add',
      type: "post",
      data: {
        desc: $('#descf').val(),
        title: $('#titlef').val(),
        category: $('#categoryf').val(),
        price: $('#pricef').val(),
        imgLink: $('#imgLink').val(),
        imgLink2: $('#imgLink2').val(),
        imgLink3: $('#imgLink3').val(),
        imgLink4: $('#imgLink4').val()
      },
    });
  } else {
    request = $.ajax({
      url: '/edit/' + $('#productId').val(),
      type: "post",
      data: {
        desc: $('#descf').val(),
        title: $('#titlef').val(),
        category: $('#categoryf').val(),
        price: $('#pricef').val(),
      },
    });
  }

  request.success(function (response, textStatus, jqXHR){
    window.location.replace(response);
  });

  request.fail(function (jqXHR, textStatus, errorThrown){
    alert("Something went wrong :(");
  });
});
