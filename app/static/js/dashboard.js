$(".removeButton").click(function(event) {
  removeId = event.target.id;
  element = $("#" + removeId);
 
  request = $.ajax({
    url: "/remove/" + removeId,
    type: "post",
  });

  request.success(function (response, textStatus, jqXHR){
    element.parent().parent().parent().hide();
  });

  request.fail(function (jqXHR, textStatus, errorThrown){
    alert("Something went wrong :(");
  });
});
