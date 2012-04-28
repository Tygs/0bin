;

// Start random number generator seeding ASAP
sjcl.random.startCollectors();

zerobin = {
  encrypt: function(key, content) {
    return sjcl.encrypt(key, lzw.compress(content));
  },
  decrypt: function(key, content) {
    return lzw.decompress(sjcl.decrypt(key, content));
  },
  make_key: function() {
    return sjcl.codec.base64.fromBits(sjcl.random.randomWords(8, 0), 0);
  },
  /**
  Check for data uri support by trying to insert a 1x1px image.
  You can pass optional callbacks: "yes" for success, "no" for no support.
  Default behavior is to add data-uri or no-data-uri as a class in the body
  */
  support_data_uri: function(yes, no){
    var data = new Image();
    var yes = yes || function(){ document.body.className += " data-uri"; };
    var no = no || function(){ document.body.className += " no-data-uri"; };
    data.onload = data.onerror = function(){
      if(this.width + this.height != 2){no()} else {yes()}
    }
    data.src = "data:image/gif;base64,R0lGODlhAQABAAD/ACwAAAAAAQABAAACADs=";
  },
  get_date: function(){
    var date = new Date();
    return date.getDate()+"-"+(date.getMonth()+1)+"-"+date.getFullYear();
  },
  get_time: function(){
    var date = new Date();
    var h=date.getHours();
    var m=date.getMinutes();
    var s=date.getSeconds();
    if (h<10) {h = "0" + h}
    if (m<10) {m = "0" + m}
    if (s<10) {s = "0" + s}
    return h+":"+m+":"+s;
  },
  support_localstorage: function(){
    if (localStorage){
      return true;  
    }else{  
      return false;  
    }
  },
  store_paste: function(url){
    if (zerobin.support_localstorage){
      var date = new Date();
      var paste = zerobin.get_date()+" "+zerobin.get_time()+";"+url;
      if (localStorage.length > 19)
        void removeItem(0);
      localStorage.setItem(localStorage.length, paste);
    }
  },
  get_pastes: function(){
    if (zerobin.support_localstorage){ 
      var pastes = ''; 

      for (i=localStorage.length-1; i>=0; i--)  
      { 
        if (localStorage.getItem(i).split(';')[0].split(' ')[0] == zerobin.get_date()){
          var display_date = localStorage.getItem(i).split(';')[0].split(' ')[1];
          var on_at = 'at ';
        }else{
          var display_date = zerobin.get_date();
          var on_at = 'on ';
        }
        pastes = pastes + '<li><a class="items" href="' + localStorage.getItem(i).split(';')[1] + '">' + on_at +  display_date + '</a></li>';
      }
      if (!pastes){
        return '<i class="grey">Your previous pastes will be saved in your browser <a href="http://www.w3.org/TR/webstorage/">localStorage</a>.</i>';
      }
      return pastes;
    }else{
      return 'Sorry your browser does not support LocalStorage, We cannot display your previous pastes.';
    }
  }
};


document.documentElement.className += " no-data-uri";
$(function(){

var language = null;

$('button[type=submit]').live("click", function(e){

  e.preventDefault();
  var paste = $('textarea').val();

  if (paste.trim()) {
    var expiration = $('#expiration').val();
    var key = zerobin.make_key();
    var data = {content: zerobin.encrypt(key, paste), expiration: expiration}

    $.post('/paste/create', data)
     .error(function(error) {
        alert('Paste could not be saved. Please try again later.');
     })
     .success(function(data) {
        var paste_url = '/paste/' + data['paste'] + '#' + key;
        window.location = (paste_url);
        zerobin.store_paste(paste_url);
     });
  }

});

var content = $('#paste-content').text().trim();
var key = window.location.hash.substring(1);
if (content && key) {
    try {
        $('#paste-content').text(zerobin.decrypt(key, content));
        prettyPrint();
    } catch(err) {
        alert('Could not decrypt data (Wrong key ?)');
    }
}

/* expiration flip/flop */
$('.paste-option select').live('change', function(){
  var value = $(this).val();
  $('.paste-option select').val(value);
});


/* Resize Textarea content */
$('#content').elastic();


/* Display bottom paste option buttons when needed */
if($('#content').height() < 600 ){
  $('.paste-option.bottom').remove();
}
$('#content').live('keyup change', function(){
   if($('#content').height() < 600 ){
      $('.paste-option.down').remove();
   }
   else {
    if ($('.paste-option').length == 1) {
      $('.paste-option').clone().addClass('down').appendTo('form.well');
    }
   }
});

/* Display previous pastes */
$('.previous-pastes .items').html(zerobin.get_pastes());
 

/* clone a paste */
$('.btn-clone').click(function(e){
  e.preventDefault();
  content_clone = '' ;
  $("#paste-content li").each(function(index) { 
    content_clone = content_clone + $(this).text() + '\n'; 
  });
  $('.submit-form').show();
  $('.paste-form').hide();
  $('#content').val(content_clone);
  $('#content').resize();

});


});
















