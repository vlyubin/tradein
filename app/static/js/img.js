$(document).ready(function(){
  var thumb = $("#thumb");
  new AjaxUpload('imageUpload', {
    action: $('form#imageUploadForm').attr('action'),
    name: 'image',
    onSubmit: function(file, extension) {
      thumb.addClass('loading');
    },
    onComplete: function(file, response) {
      thumb.removeClass('loading');
      response = JSON.parse(response);
      thumb.attr("src", response.file);
      console.log(response.file);
      $("#imgLink").attr("value", response.file)
      //TODO Save the response.file to the DB afterwards
    }
  });
});

$(document).ready(function(){
  var thumb = $("#thumb2");
  new AjaxUpload('imageUpload2', {
    action: $('form#imageUploadForm2').attr('action'),
    name: 'image',
    onSubmit: function(file, extension) {
      thumb.addClass('loading');
    },
    onComplete: function(file, response) {
      thumb.removeClass('loading');
      response = JSON.parse(response);
      thumb.attr("src", response.file);
      console.log(response.file);
      $("#imgLink2").attr("value", response.file)
      //TODO Save the response.file to the DB afterwards
    }
  });
});

$(document).ready(function(){
  var thumb = $("#thumb3");
  new AjaxUpload('imageUpload3', {
    action: $('form#imageUploadForm3').attr('action'),
    name: 'image',
    onSubmit: function(file, extension) {
      thumb.addClass('loading');
    },
    onComplete: function(file, response) {
      thumb.removeClass('loading');
      response = JSON.parse(response);
      thumb.attr("src", response.file);
      console.log(response.file);
      $("#imgLink3").attr("value", response.file)
      //TODO Save the response.file to the DB afterwards
    }
  });
});

$(document).ready(function(){
  var thumb = $("#thumb4");
  new AjaxUpload('imageUpload4', {
    action: $('form#imageUploadForm4').attr('action'),
    name: 'image',
    onSubmit: function(file, extension) {
      thumb.addClass('loading');
    },
    onComplete: function(file, response) {
      thumb.removeClass('loading');
      response = JSON.parse(response);
      thumb.attr("src", response.file);
      console.log(response.file);
      $("#imgLink4").attr("value", response.file)
      //TODO Save the response.file to the DB afterwards
    }
  });
});
/*

Usage:

<form id="imageUploadForm" action="/img" method="post">
  <img id="thumb" />
  <input type="file" size="20" id="imageUpload">
  <a class="button">Save</a>
</form>

<script src="static/js/ajaxupload.js"></script>
<script src="static/js/img.js"></script>

*/