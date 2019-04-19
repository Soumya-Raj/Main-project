


function photo(){

  var pic=document.getElementById('file').files[0];


  var a='Date ::'+pic.date;
  a+='<br> Name ::'+pic.name;
  a+='<br> Size ::'+pic.size;
  a+='<br> Type ::'+pic.type;

  var filetype= 'application/*';

  if (!pic.type.match(filetype))
    {document.getElementById('res').innerHTML="Invalid File Format"}

  else{

    document.getElementById('res').innerHTML= a;


    }


}
