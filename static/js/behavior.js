;

/* Start random number generator seeding ASAP *%
sjcl.random.startCollectors();
/* Ensure jquery use cache for ajax requests */
$.ajaxSetup({ cache: true });



zerobin = {
  encrypt: function(key, content) {
    content = sjcl.codec.base64.fromBits(sjcl.codec.utf8String.toBits(content));
    return sjcl.encrypt(key, lzw.compress(content));
  },
  decrypt: function(key, content) {
    content = lzw.decompress(sjcl.decrypt(key, content));
    return sjcl.codec.utf8String.fromBits(sjcl.codec.base64.toBits(content));
  },
  make_key: function() {
    return sjcl.codec.base64.fromBits(sjcl.random.randomWords(8, 0), 0);
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
  numOrdA: function(a, b){ 
    return (a-b); 
  },
  get_keys: function(){
    var keys = new Array();
    for(i=0; i<=localStorage.length; i++){
      if(localStorage.key(i) != null)
        keys[i] = parseInt(localStorage.key(i),10);
    }
    return keys.sort(zerobin.numOrdA);
  },
  /** Get a tinyurl using JSONP */
  getTinyURL: function(longURL, success) {

    callback = 'zerobin_tiny_url_callback';
    window[callback] = function(response){
      success(response.tinyurl);
      delete window[callback];
    };

    var api = 'http://json-tinyurl.appspot.com/?url=';
    $.getJSON(api + encodeURIComponent(longURL) + '&callback=' + callback);
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
      var keys = zerobin.get_keys();

      if(keys.length < 1)
        keys[0] = 0;

      if (localStorage.length > 19)
        void localStorage.removeItem(keys[0]);
      localStorage.setItem(keys.reverse()[0]+1, paste);
    }
  },
  get_pastes: function(){
    if (zerobin.support_localstorage){
      var pastes = ''; 
      var keys = zerobin.get_keys();
      keys.reverse();

      for (i=0; i<=keys.length-1; i++)
      {
        var paste = localStorage.getItem(keys[i]);
        if (paste.split(';')[0].split(' ')[0] == zerobin.get_date()){
          var display_date = paste.split(';')[0].split(' ')[1];
          var on_at = 'at ';
        }else{
          var display_date = zerobin.get_date();
          var on_at = 'on ';
        }
        pastes = pastes + '<li><a class="items" href="' + paste.split(';')[1] + '">' + on_at +  display_date + '</a></li>';
      } 
      if (!pastes){
        return '<i class="grey">Your previous pastes will be saved in your browser using <a href="http://www.w3.org/TR/webstorage/">localStorage</a>.</i>';
      }
      return pastes;
    }else{
      return 'Sorry your browser does not support LocalStorage, We cannot display your previous pastes.';
    }
  },
  get_paste_content: function(){
    var content_clone = '' ;
    $("#paste-content li").each(function(index) {
      content_clone = content_clone + $(this).text() + '\n';
    });
    return content_clone;
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
        var paste_url = '/paste/' + data['paste'] + '#' + key;
        window.location = (paste_url);
        zerobin.store_paste(paste_url);
     });
  }

});

/** On the display paste page.
    Decrypt and decompress the paste content, add syntax coloration then
    setup the copy to clipboard button.
*/
var content = $('#paste-content').text().trim();
var key = window.location.hash.substring(1);
var error = false;
if (content && key) {
    try {
        $('#paste-content').text(zerobin.decrypt(key, content));
    } catch(err) {
        error = true;
        alert('Could not decrypt data (Wrong key ?)');
    }

    content = '';

    if (!error) {

      $('#short-url').click(function(e) {
        e.preventDefault();
        $('#short-url').text('Loading short url...');
        zerobin.getTinyURL(window.location.toString(), function(tinyurl){
          clip.setText(tinyurl);
          $('#copy-success').hide();
          $('#short-url-success')
           .html('Short url: <a href="' + tinyurk + '">' + tinyurk + '</a>')
           .show('fadeUp');
          $('#short-url').text('Get short url');
        });
      });

      prettyPrint();

      /* Setup flash clipboard button */
      ZeroClipboard.setMoviePath('/static/js/ZeroClipboard.swf' );

      var clip = new ZeroClipboard.Client();
      clip.addEventListener('mouseup', function(){
        clip.setText(zerobin.get_paste_content());
      });
      clip.addEventListener('complete', function(){
        $('#copy-success').show('fadeUp', function(){clip.reposition()});
      });
      clip.glue('clip-button');

      window.onresize = clip.reposition;
    }

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
   }
});

/* Display previous pastes */
$('.previous-pastes .items').html(zerobin.get_pastes());



/* clone a paste */
$('.btn-clone').click(function(e){
  e.preventDefault();
  var content_clone = zerobin.get_paste_content();
  $('.submit-form').show();
  $('.paste-form').remove();
  $('#content').val(content_clone);
  $('#content').trigger('change');

});

});
















