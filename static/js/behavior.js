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
  }
};


document.documentElement.className += " no-data-uri";
$(function(){

var language = null;

$('button[type=submit]').click(function(e){

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
        window.location = ('/paste/' + data['paste'] + '#' + key);
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
$('#content').live('keyup change', function(){
   if($('#content').height() < 600 ){
      $('.paste-option.down').remove();
   }
   else {
    if ($('.paste-option').length == 1) {
      $('.paste-option').clone().addClass('down').appendTo('form.well');
    }
   };
});


});