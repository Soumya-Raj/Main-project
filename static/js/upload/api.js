//JS FUNCTION OF FILE PICKER(GOOGLE API)

function initPicker() {
  var picker = new FilePicker({
    apiKey: 'AIzaSyDTpfIEYydGLzzhKRrm41LaqFssZLiqsjU',
    clientId:'358327259908-80kme5hvb18pajeh2ujtb727cue6fc87.apps.googleusercontent.com',
    buttonEl: document.getElementById('pick'),
    onSelect: function(file) {
      console.log(file);
      //alert('Selected ' + file.downloadUrl);
      var link=file.webContentLink
      var met="drive"
      $.ajax({
  type: "POST",
  contentType: "application/json;charset=utf-8",
  url: "/uploader",
  traditional: "true",
  data: JSON.stringify({link}),
  //data2: JSON.stringify({met}),
  dataType: "json"
  });
    }
  });
}

//JS PART OF CHOOSER(DROPBOX API )


options = {

    // Required. Called when a user selects an item in the Chooser.
    success: function(files) {

      var link=files[0].link
      $.ajax({
  type: "POST",
  contentType: "application/json;charset=utf-8",
  url: "/uploader",
  traditional: "true",
  data: JSON.stringify({link}),
  dataType: "json"
  });
        //alert("Here's the file link: "+ files[0].link )
    },

    // Optional. Called when the user closes the dialog without selecting a file
    // and does not include any parameters.
    cancel: function() {

    },

    // Optional. "preview" (default) is a preview link to the document for sharing,
    // "direct" is an expiring link to download the contents of the file. For more
    // information about link types, see Link types below.
    linkType: "direct", // or "preview"

    // Optional. A value of false (default) limits selection to a single file, while
    // true enables multiple file selection.
    multiselect: false, // or true

    // Optional. This is a list of file extensions. If specified, the user will
    // only be able to select files with these extensions. You may also specify
    // file types, such as "video" or "images" in the list. For more information,
    // see File types below. By default, all extensions are allowed.
    extensions: ['.mhd,.raw'],

    // Optional. A value of false (default) limits selection to files,
    // while true allows the user to select both folders and files.
    // You cannot specify `linkType: "direct"` when using `folderselect: true`.
    folderselect: false, // or true
};
