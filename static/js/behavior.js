;

/* Start random number generator seeding ASAP */
sjcl.random.startCollectors();
/* Ensure jquery use cache for ajax requests */
$.ajaxSetup({ cache: true });

zerobin = {
    /** Base64 + compress + encrypt, with callbacks before each operation,
        and all of them are executed in a timed continuation to give
        a change to the UI to respond.
    */
    encrypt: function(key, content, toBase64Callback,
                    compressCallback, encryptCallback, doneCallback) {

      setTimeout (function(){

        content = sjcl.codec.utf8String.toBits(content);
        if (toBase64Callback) {toBase64Callback()}

        setTimeout(function(){

          content = sjcl.codec.base64.fromBits(content);
          if (compressCallback) {compressCallback()}

          setTimeout(function(){

            content = lzw.compress(content);
            if (encryptCallback) {encryptCallback()}

            setTimeout(function(){
              content = sjcl.encrypt(key, content);
              if (doneCallback) {doneCallback(content)}
            }, 250);

          }, 250);

        }, 250);

      }, 250);
  },

  /** Base64 decoding + uncompress + decrypt, with callbacks before each operation,
      and all of them are executed in a timed continuation to give
      a change to the UI to respond.

      This is where using a library to fake synchronicity could start to be
      useful, this code is starting be difficult to read. If anyone read this
      and got a suggestion, by all means, speak your mind.
  */
  decrypt: function(key, content, errorCallback, uncompressCallback,
                    fromBase64Callback, toStringCallback, doneCallback) {

    /* Decrypt */
    setTimeout(function(){

      try {

        content = sjcl.decrypt(key, content);
        if (uncompressCallback) {uncompressCallback()}

        /* Decompress */
        setTimeout(function(){

          try {

            content = lzw.decompress(content);
            if (fromBase64Callback) {fromBase64Callback()}

            /* From base 64 to bits */
            setTimeout(function(){

              try {

                content = sjcl.codec.base64.toBits(content);
                if (toStringCallback) {toStringCallback()}

                /* From bits to string */
                setTimeout(function(){

                  try {
                    content = sjcl.codec.utf8String.fromBits(content);
                    if (doneCallback) {doneCallback(content)}
                  } catch (err) {
                    errorCallback(err);
                  }

                }, 250); /* "End of from bits to string" */

              } catch (err) {
                errorCallback(err);
              }

            }, 250); /* End of "from base 64 to bits" */

          } catch (err) {
            errorCallback(err);
          }

        }, 250); /* End of "decompress" */

      } catch (err) {
        errorCallback(err);
      }

    }, 250); /* End of "decrypt" */
  },

  /** Create a random base64 string long enought to be suitable as
  an encryption key */
  makeKey: function() {
    return sjcl.codec.base64.fromBits(sjcl.random.randomWords(8, 0), 0);
  },

  getDate: function(){
    var date = new Date();
    return date.getDate()+"-"+(date.getMonth()+1)+"-"+date.getFullYear();
  },

  getTime: function(){
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

  getKeys: function(){
    var keys = new Array();
    for(i=0; i<=localStorage.length; i++){
      if(localStorage.key(i) != null)
        keys[i] = parseInt(localStorage.key(i),10);
    }
    return keys.sort(zerobin.numOrdA);
  },
  /** Get a tinyurl using JSONP */
  getTinyURL: function(longURL, success) {
    var api = 'http://json-tinyurl.appspot.com/?url=';
    $.getJSON(api + encodeURIComponent(longURL) + '&callback=?', function(data){
      success(data.tinyurl);
    });
  },

  support: {
    localstorage: function(){
      return !!(localStorage);
    },
    history: function(){
      return !!(window.history && history.pushState);
    }
  },

  storatePaste: function(url){
    if (zerobin.support.localstorage){
      var date = new Date();
      var paste = zerobin.getDate()+" "+zerobin.getTime()+";"+url;
      var keys = zerobin.getKeys();

      if(keys.length < 1)
        keys[0] = 0;

      if (localStorage.length > 19)
        void localStorage.removeItem(keys[0]);
      localStorage.setItem(keys.reverse()[0]+1, paste);
    }
  },

  getPastes: function(){
    if (zerobin.support.localstorage){
      var pastes = '';
      var keys = zerobin.getKeys();
      keys.reverse();

      for (i=0; i<=keys.length-1; i++)
      {
        var paste = localStorage.getItem(keys[i]);
        if (paste.split(';')[0].split(' ')[0] == zerobin.getDate()){
          var display_date = paste.split(';')[0].split(' ')[1];
          var on_at = 'at ';
        }else{
          var display_date = zerobin.getDate();
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

  getPasteContent: function(){
    var content_clone = '' ;
    $("#paste-content li").each(function(index) {
      content_clone = content_clone + $(this).text() + '\n';
    });
    return content_clone;
  },
  count: function(text, options) {
    // Set option defaults
    var crlf = /(\r?\n|\r)/g;
    var whitespace = /(\r?\n|\r|\s+)/g;
    options = options || {};
    options.lineBreaks = options.lineBreaks || 1;

    var length = text.length,
      nonAscii = length - text.replace(/[\u0100-\uFFFF]/g, '').length,
        lineBreaks = length - text.replace(crlf, '').length;

      return length + nonAscii + Math.max(0, options.lineBreaks * (lineBreaks - 1));
  },
  message: function(type, message, title, flush, callback) {

    if (flush) {$('.alert-'+type).remove()}

    $message = $('#alert-template').clone().attr('id', null)
                                   .addClass('alert alert-' + type);
    $('.message', $message).html(message);

    if (title) {$('.title', $message).html(title)}
    else {$('.title', $message).remove()}

    $message.prependTo($('#main')).show('fadeUp', callback);
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

  var sizebytes = zerobin.count($('#content').val(), { });
  var oversized = sizebytes > zerobin.max_size;
  var readable_fsize = Math.round(sizebytes/1024);
  var readable_maxsize = Math.round(zerobin.max_size/1024)
  if (oversized){
    zerobin.message('error',
                    ('Your file is <strong class="file-size">' + readable_fsize +
                    '</strong>KB. You have reached the maximum size limit of ' +
                    readable_maxsize + 'KB.'),
                    'Warning!', true)
  }

  if (!oversized && paste.trim()) {

    $form = $('input, textarea, select, button').prop('disabled', true);
    $form.prop('disabled', true);
    $bar = $('form.well .progress').show();
    var $loading = $('form.well .progress .bar')
                    .css('width', '25%')
                    .text('Converting paste to bits...');

    /* Encode, compress, encrypt and send the paste then redirect the user
       to the new paste. We ensure a loading animation is updated
       during the process by passing callbacks.
    */
    try {

      var expiration = $('#expiration').val();
      var key = zerobin.makeKey();

      zerobin.encrypt(key, paste,

        function(){$loading.text('Encoding to base64...').css('width', '45%')},
        function(){$loading.text('Compressing...').css('width', '65%')},
        function(){$loading.text('Encrypting...').css('width', '85%')},

        /* This block deal with sending the data, redirection or error handling */
        function(content){

          $loading.text('Sending...').css('width', '95%');
          var data = {content: content, expiration: expiration};

          $.post('/paste/create', data)
           .error(function(error) {
              $form.prop('disabled', false);
              $loading.hide();
              zerobin.message(
                'error',
                'Paste could not be saved. Please try again later.',
                'Error'
              );

           })
           .success(function(data) {
              $loading.text('Redirecting to new paste...').css('width', '100%');

              if (data['status'] == 'error') {
                zerobin.message('error', data['message'], 'Error');
                $form.prop('disabled', false);
                $bar.hide();
              } else {
                var paste_url = '/paste/' + data['paste'] + '#' + key;
                zerobin.storatePaste(paste_url);
                window.location = (paste_url);
              }
           });
        }
      );
    } catch (err) {
      $form.prop('disabled', false);
      $bar.hide();
      zerobin.message('error', 'Paste could not be encrypted. Aborting.',
                      'Error');
    }
  }

});

/**
    DECRYPTION:
    On the display paste page, decrypt and decompress the paste content,
    add syntax coloration then setup the copy to clipboard button.
*/
var content = $('#paste-content').text().trim();
var key = window.location.hash.substring(1);
var error = false;
if (content && key) {

  var $bar = $('.well form .progress').show();
  var $loading = $('.well form .progress .bar').css('width', '25%')
                                               .text('Decrypting paste...');

  zerobin.decrypt(key, content,

    /* On error*/
    function(){
      $bar.hide();
      zerobin.message('error', 'Could not decrypt data (Wrong key ?)',
                      'Error');
    },

    /* Update progress bar */
    function(){$loading.text('Decompressing...').css('width', '45%')},
    function(){$loading.text('Base64 decoding...').css('width', '65%')},
    function(){$loading.text('From bits to string...').css('width', '85%')},

    /* When done */
    function(content){

      /* Decrypted content goes back to initial container*/
      $('#paste-content').text(content);
      content = '';

      $loading.text('Code coloration...').css('width', '95%');

      /* Add a continuation to let the UI redraw */
      setTimeout(function(){

        /* Setup link to get the paste short url*/
        $('#short-url').click(function(e) {
          e.preventDefault();
          $('#short-url').text('Loading short url...');
          zerobin.getTinyURL(window.location.toString(), function(tinyurl){
            clip.setText(tinyurl);
            $('#copy-success').hide();
            zerobin.message('success',
                            '<a href="' + tinyurl + '">' + tinyurl + '</a>',
                            'Short url'
            )
            $('#short-url').text('Get short url');
          });
        });

        /* Setup flash clipboard button */
        ZeroClipboard.setMoviePath('/static/js/ZeroClipboard.swf');

        var clip = new ZeroClipboard.Client();
        clip.addEventListener('mouseup', function(){
          clip.setText(zerobin.getPasteContent());
        });
        clip.addEventListener('complete', function(){
          zerobin.message('info', 'The paste is now in your clipboard',
                          '', false, function(){clip.reposition()});
        });
        clip.glue('clip-button');

        window.onresize = clip.reposition;

        /** Syntaxic coloration */
        prettyPrint();

        /* Display result */
        $loading.text('Done').css('width', '100%');
        $bar.hide();
      }, 250);

    }
  );

} /* End of "DECRYPTION" */

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
$('.previous-pastes .items').html(zerobin.getPastes());

/* clone a paste */
$('.btn-clone').click(function(e){
  e.preventDefault();
  var content_clone = zerobin.getPasteContent();
  $('.submit-form').show();
  $('.paste-form').remove();
  $('#content').val(content_clone);
  $('#content').trigger('change');

});


/* Upload file using HTML5 File API */

if (window.File && window.FileReader && window.FileList && window.Blob) {
  $('.file-upload').show();
}

var file_upload = function(file) {
  var reader = new FileReader();
  reader.onload = function(event) {
    var content = event.target.result;
    $('#content').val(content);
    $('#content').trigger('change');
  };

  reader.readAsText(file[0]);
}

try {
  $('#file-upload').change(function() {
    file_upload(this.files);
  });
}
catch (e) {
  zerobin.message('error', 'Could no upload the file', 'Error');
}

$('#file-upload').mouseover(function(){
  $(this).css( 'cursor', 'pointer' );
});


/* Alerts */

$(".close").live('click', function(){
  $(this).parent().fadeOut();
});

}); /* End of "document ready" jquery callback */



