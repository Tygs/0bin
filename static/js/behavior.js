;

/* Start random number generator seeding ASAP *%
sjcl.random.startCollectors();
/* Ensure jquery use cache for ajax requests */
$.ajaxSetup({ cache: true });

zerobin = {
  encrypt: function(key, content) {
    return sjcl.encrypt(key, lzw.compress(content));
  },
  decrypt: function(key, content) {
    return lzw.decompress(sjcl.decrypt(key, content));
  },
  make_key: function() {
    return sjcl.codec.base64.fromBits(sjcl.random.randomWords(8, 0), 0);
  }
};


$(function(){

/**
  On the create paste page:
  On click on the send button, compress and encrypt data before
   posting it using ajax. Then redirect to the address of the
   newly created paste, adding the key in the hash.
*/
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
        window.location = ('/paste/' + data['paste'] + '#' + key);
     });
  }

});

/** On the display paste page.
    Decrypt and decompress the paste content, add syntax coloration
    then insert the flash code to download the paste.
*/
var content = $('#paste-content').text().trim();
var key = window.location.hash.substring(1);
if (content && key) {
    try {
        $('#paste-content').text(zerobin.decrypt(key, content));
    } catch(err) {
        alert('Could not decrypt data (Wrong key ?)');
    }
    prettyPrint();

    /** Load dynamically the flash code (it's pretty heavy so doing it
       now will make the page appear to load faster)
       And create the download button.
    */
    $.getScript("/static/js/swfobject.js", function(script, textStatus) {
      $.getScript("/static/js/downloadify.min.js", function(){
        Downloadify.create('downloadify',{
          filename: function(){
            return 'test.txt';
          },
          data: function(){
            return $('#paste-content').text();
          },
          onError: function(){ alert("Sorry, the file couldn't be downloaded. :("); },
          swf: '/static/js/downloadify.swf',
          downloadImage: '/static/img/download.png',
          width: 96,
          height: 28,
          transparent: true,
          append: false
        });
      });
    });
}

/* Synchronize expiration select boxes value */
$('.paste-option select').live('change', function(){
  var value = $(this).val();
  $('.paste-option select').val(value);
});


/* Resize Textarea according to content */
$('#content').elastic();


/* Display bottom paste option buttons when needed */
$('#content').live('keyup change', function(){
   if($('#content').height() < 400 ){
      $('.paste-option.down').remove();
   }
   else {
    if ($('.paste-option').length == 1) {
      $('.paste-option').clone().addClass('down').appendTo('form.well');
    }
   };
});

});