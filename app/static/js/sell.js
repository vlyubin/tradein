$(document).ready(function(){
  var $thumbs = $("#thumbnails");
  var $form = $("#submitForm");

  $("#submitButton").click(function(){
    var images = getImages();
    while(images.length < 4) {
      images.push("");
    }
    if ($('#addedit').val() === 'add') {
      request = $.ajax({
        url: '/add',
        type: "post",
        data: {
          desc: $('#descf').val(),
          title: $('#titlef').val(),
          category: $('#categoryf').val(),
          price: $('#pricef').val(),
          imgLink: images[0],
          imgLink2: images[1],
          imgLink3: images[2],
          imgLink4: images[3]
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

  IMG.submit(function() {
    console.log("Submit");
  });

  IMG.complete(function(file) {
    console.log("Complete " + file);
    var div = $("<div/>", {class: "image-container"});
    var title = $("<div/>").append($("<a/>", {href: file, text: "[Full picture]", target: "_blank"}))
    .append(" - ")
    .append($("<a/>", {href: "#", text: "[Remove]"}).click(
      function(event){
        $(this).parent().parent().remove();
        event.preventDefault();
      }));
    div.append(title);
    div.append($("<img/>", {"src": file, style: "max-width:400px; max-height:300px;"}));
    $thumbs.append(div);
  });

  function getImages() {
    var images = new Array();
    $thumbs.find("img").each(function() {
      images.push($(this).attr("src"));
    });
    return images;
  }
});