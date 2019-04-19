Dropzone.options.myDropzone = {

autoProcessQueue: false,

init: function() {
    var submitButton = document.querySelector("#upload-button");
    myDropzone = this;

    submitButton.addEventListener("click", function() {
        myDropzone.processQueue();
    });

    this.on("sending", function() {
        $("#myDropzone").submit()
    });
  }
};
