/*global sjcl:true, jQuery:true, $:true, lzw:true, zerobin:true, ZeroClipboard:true, vizhash:true, prettyPrint:true, confirm:true */
;
(function () {
  "use strict";

  /* Start random number generator seeding ASAP */
  sjcl.random.startCollectors();
  /* Ensure jquery use cache for ajax requests */
  $.ajaxSetup({
    cache: true
  });

  /** Create a function that create inline callbacks.
    We use it to create callbacks for onliners with static arguments
    E.G:
      $('stuff').hide(function()(console.log(1, 2, 3)))

      Becomes:

      $('stuff').hide(mkcb(console.log, 1, 2, 3))
  */
  function mkcb(func) {
    var args = arguments;
    return function () {
      return func.apply(func, Array.prototype.slice.call(args, 1));
    };
  }



  /***************************
   ****  0bin utilities    ***
   ***************************/


  window.zerobin = {
    /** Base64 + compress + encrypt, with callbacks before each operation,
        and all of them are executed in a timed continuation to give
        a change to the UI to respond.
    */
    version: '0.1.1',
    encrypt: function (key, content, toBase64Callback,
    compressCallback, encryptCallback, doneCallback) {

      setTimeout(function () {

        content = sjcl.codec.utf8String.toBits(content);
        if (toBase64Callback) {
          toBase64Callback();
        }

        setTimeout(function () {

          content = sjcl.codec.base64.fromBits(content);
          if (compressCallback) {
            compressCallback();
          }

          setTimeout(function () {

            // content = lzw.compress(content); // Create a bug with JPG
            if (encryptCallback) {
              encryptCallback();
            }

            setTimeout(function () {
              try {
                content = sjcl.encrypt(key, content);
              } catch (e) {
 			    $('input, textarea, select, button').prop('disabled', false);
                zerobin.progressBar('form.well .progress').container.hide();

                zerobin.message('error', 'Paste could not be encrypted. Aborting.',
                  'Error');
              }
              if (doneCallback) {
                doneCallback(content);
              }
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
    decrypt: function (key, content, errorCallback, uncompressCallback,
    fromBase64Callback, toStringCallback, doneCallback) {

      /* Decrypt */
      setTimeout(function () {
        try {
          content = sjcl.decrypt(key, content);
          if (uncompressCallback) {
            uncompressCallback();
          }

          /* Decompress */
          setTimeout(function () {
            try {
              content = lzw.decompress(content);
              if (fromBase64Callback) {
                fromBase64Callback();
              }

              /* From base 64 to bits */
              setTimeout(function () {
                try {
                  content = sjcl.codec.base64.toBits(content);
                  if (toStringCallback) {
                    toStringCallback();
                  }

                  /* From bits to string */
                  setTimeout(function () {
                    try {
                      content = sjcl.codec.utf8String.fromBits(content);
                      if (doneCallback) {
                        doneCallback(content);
                      }
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

    /** Create a random base64-like string long enought to be suitable as
        an encryption key */
    makeKey: function (entropy) {
        entropy = Math.ceil(entropy / 6) * 6; /* non-6-multiple produces same-length base64 */
        var key = sjcl.bitArray.clamp(
          sjcl.random.randomWords(Math.ceil(entropy / 32), 0), entropy );
        return sjcl.codec.base64.fromBits(key, 0).replace(/\=+$/, '').replace(/\//, '-');
    },

    getFormatedDate: function (date) {
      date = date || new Date();
      return ((date.getMonth() + 1) + '-' + date.getDate() + '-' + date.getFullYear());
    },

    getFormatedTime: function (date) {
      date = date || new Date();
      var h = date.getHours(),
        m = date.getMinutes(),
        s = date.getSeconds();
      if (h < 10) {
        h = "0" + h;
      }
      if (m < 10) {
        m = "0" + m;
      }
      if (s < 10) {
        s = "0" + s;
      }
      return h + ":" + m + ":" + s;
    },

    numOrdA: function (a, b) {
      return (a - b);
    },

    /** Return a reverse sorted list of all the keys in local storage that
      are prefixed with with the passed version (default being this lib
      version) */
    getLocalStorageKeys: function () {
      var version = 'zerobinV0.1';
      var keys = [];
      for (var key in localStorage) {
        if (key.indexOf(version) !== -1) {
          keys.push(key);
        }
      }
      keys.sort();
      keys.reverse();
      return keys;
    },

    /** Get a tinyurl using JSONP */
    getTinyURL: function(longURL, success) {
        $.ajax({
  		  url: 'https://www.googleapis.com/urlshortener/v1/url',
  		  type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({
                "longUrl": longURL
  		  }),
  		  processData: false,
  		  dataType: 'json'
  	  }).done(function(data){
  		  success(data.id);
        });
    },

    /** Check for browser support of the named featured. Store the result
      and add a class to the html tag with the result */
    support: {
      localStorage: (function () {
        var val = !! (localStorage);
        $('html').addClass((val ? '' : 'no-') + 'local-storage');
        return val;
      })(),

      history: (function () {
        var val = !! (window.history && history.pushState);
        $('html').addClass((val ? '' : 'no-') + 'history');
        return val;
      })(),

      fileUpload: (function () {
        var w = window;
        var val = !! (w.File && w.FileReader && w.FileList && w.Blob);
        $('html').addClass((val ? '' : 'no-') + 'file-upload');
        return val;
      })()
    },

    /** Store the paste of a URL in local storate, with a storage format
      version prefix and the paste date as the key */
    storePaste: function (url, date) {

      date = date || new Date();
      date = (date.getFullYear() + '-' + (date.getMonth() + 1) + '-' + date.getDate() + ' ' + zerobin.getFormatedTime(date));

      var keys = zerobin.getLocalStorageKeys();

      if (localStorage.length > 19) {
        void localStorage.removeItem(keys[19]);
      }

      localStorage.setItem('zerobinV' + zerobin.version + "#" + date, url);
    },

    /** Return a list of the previous paste url with the creation date
      If the paste is from today, date format should be "at hh:ss",
      else it should be "the mm-dd-yyy"
  */
    getPreviousPastes: function () {
      var pastes = [],
        keys = zerobin.getLocalStorageKeys(),
        today = zerobin.getFormatedDate();

      $.each(keys, function (i, key) {
        var pasteDateTime = key.replace(/^[^#]+#/, '');
        var displayDate = pasteDateTime.match(/^(\d+)-(\d+)-(\d+)\s/);
        displayDate = displayDate[2] + '-' + displayDate[3] + '-' + displayDate[1];
        var prefix = 'the ';
        if (displayDate === today) {
          displayDate = pasteDateTime.split(' ')[1];
          prefix = 'at ';
        }
        pastes.push({
          displayDate: displayDate,
          prefix: prefix,
          link: localStorage.getItem(key)
        });
      });

      return pastes;
    },

    /** Return an link object with the URL as href so you can extract host,
      protocol, hash, etc.

      This function use a closure to store a <div> parent for the <a>
      because IE requires the link be processed by it's HTML parser
      for the URL to be parsed. */
    parseUrl: (function () {

      var div = document.createElement('div');
      div.innerHTML = "<a></a>";

      return function (url) {
        div.firstChild.href = url;
        div.innerHTML = div.innerHTML;
        return div.firstChild;
      };

    })(),

    getPasteId: function (url) {
      var loc = url ? zerobin.parseUrl(url) : window.location;
      return loc.pathname.replace(/\/|paste/g, '');
    },

    getPasteKey: function (url) {
      var loc = url ? zerobin.parseUrl(url) : window.location;
      return loc.hash.replace('#', '').replace(/(\?|&).*$/, '');
    },

    /** Return the paste content stripted from any code coloration */
    getPasteContent: function () {
      var copy = '';
      $("#paste-content li").each(function (index) {
        copy = copy + $(this).text().replace(/[\u00a0]+/g, ' ') + '\n';
      });
      if (copy == '') {
          copy = $("#paste-content").text();
      }
      return copy;
    },

    /** Return an approximate estimate the number of bytes in a text */
    count: function (text, options) {
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
    /** Create a message, style it and insert it in the alert box */
    message: function (type, message, title, flush, callback) {
      $(window).scrollTop(0);

      if (flush) {
        $('.alert-' + type).remove();
      }

      var $message = $('#alert-template').clone().attr('id', null)
        .addClass('alert alert-' + type);
      $('.message', $message).html(message);

      if (title) {
        $('.title', $message).html(title);
      } else {
        $('.title', $message).remove();
      }

      $message.prependTo($('#main')).show('fadeUp', callback);
    },

    /** Return a progress bar object */
    progressBar: function (selector) {
      var $container = $(selector);
      var bar = {
        container: $container,
        elem: $container.find('.bar')
      };
      bar.set = function (text, rate) {
        bar.elem.text(text).css('width', rate);
      };
      return bar;
    },

    /** Return an integer ranking the probability this text is any kind of
      source code. */
    isCode: function (text) {

      var code_chars = /[A-Z]{3}[A-Z]+|\.[a-z]|[=:<>{}\[\]$_'"&]| {2}|\t/g;
      var comments = /(:?\/\*|<!--)(:?.|\n)*?(:?\*\/|-->)|(\/\/|#)(.*?)\n/g;
      var formating = /[-*=_+]{4,}/;

      var total = 0;
      var size = 0;
      var m = text.match(comments);
      if (m) {
        total += text.match(comments).length;
      }
      text = text.replace(comments, '');
      text.replace(formating, '');
      text = text.split('\n');
      for (var i = 0; i < text.length; i++) {
        var line = text[i];
        size += line.length;
        var match = line.replace(formating, '').match(code_chars);
        if (match) {
          total += match.length;
        }
      }

      return total * 1000 / size;
    },

    // prevent defaults
    ignoreDrag: function (e) {
      e.originalEvent.stopPropagation();
      e.originalEvent.preventDefault();
    },

    // Handle Drop
    handleDrop: function (e) {
      e.originalEvent.preventDefault();
      zerobin.upload(e.originalEvent.dataTransfer.files);
      $("#content").removeClass('hover');
    },

    handleDragOver: function (e) {
      zerobin.ignoreDrag(e);
      $(this).addClass('hover');
    },

    handleDragLeave: function (e) {
      $(this).removeClass('hover');
    },

    upload: function (files) {
      var current_file = files[0];
      var reader = new FileReader();
      if (current_file.type.indexOf('image') == 0) {
        reader.onload = function (event) {
            var image = new Image();
            image.src = event.target.result;

            image.onload = function() {
              var maxWidth = 1024,
                  maxHeight = 1024,
                  imageWidth = image.width,
                  imageHeight = image.height;


              if (imageWidth > imageHeight) {
                if (imageWidth > maxWidth) {
                  imageHeight *= maxWidth / imageWidth;
                  imageWidth = maxWidth;
                }
              }
              else {
                if (imageHeight > maxHeight) {
                  imageWidth *= maxHeight / imageHeight;
                  imageHeight = maxHeight;
                }
              }

              var canvas = document.createElement('canvas');
              canvas.width = imageWidth;
              canvas.height = imageHeight;
              image.width = imageWidth;
              image.height = imageHeight;
              var ctx = canvas.getContext("2d");
              ctx.drawImage(this, 0, 0, imageWidth, imageHeight);

              var paste = canvas.toDataURL(current_file.type);
              $('#content').val(paste).trigger('change');
              $('#content').hide();
              $(image).css('max-width', '742px');
  			  $('#content').after(image);
            }
          }
        reader.readAsDataURL(current_file);
      } else {
        reader.onload = function (event) {
          $('#content').val(event.target.result).trigger('change');
        };
        reader.readAsText(current_file);
      }
    }
  };


  /***************************
   **** On document ready    ***
   ****************************/


  $(function () {

    /**
  On the create paste page:
  On click on the send button, compress and encrypt data before
   posting it using ajax. Then redirect to the address of the
   newly created paste, adding the key in the hash.
*/
    $('.btn-primary').live("click", function (e) {

      e.preventDefault();
      var paste = $('textarea').val();

      if (paste.trim()) {

        var $form = $('input, textarea, select, button').prop('disabled', true);

        // set up progress bar
        var bar = zerobin.progressBar('form.well .progress');
        bar.container.show();
        bar.set('Converting paste to bits...', '25%');

        /* Encode, compress, encrypt and send the paste then redirect the user
       to the new paste. We ensure a loading animation is updated
       during the process by passing callbacks.
    */
        try {

          var expiration = $('#expiration').val();
          var key = zerobin.makeKey(256);

          zerobin.encrypt(key, paste,

          mkcb(bar.set, 'Encoding to base64...', '45%'),
          mkcb(bar.set, 'Compressing...', '65%'),
          mkcb(bar.set, 'Encrypting...', '85%'),

          /* This block deal with sending the data, redirection or error handling */
          function (content) {

            bar.set('Sending...', '95%');
            var data = {
              content: content,
              expiration: expiration
            };
            var sizebytes = zerobin.count(JSON.stringify(data));
            var oversized = sizebytes > zerobin.max_size; // 100kb - the others header information
            var readableFsize = Math.round(sizebytes / 1024);
            var readableMaxsize = Math.round(zerobin.max_size / 1024);

            if (oversized) {
              bar.container.hide();
              $form.prop('disabled', false);
              zerobin.message('error', ('The encrypted file was <strong class="file-size">' + readableFsize +
                '</strong>KB. You have reached the maximum size limit of ' + readableMaxsize + 'KB.'),
                'Warning!', true);
              return;
            }

            $.post('/paste/create', data)
              .error(function (error) {
              $form.prop('disabled', false);
              bar.container.hide();
              zerobin.message(
                'error',
                'Paste could not be saved. Please try again later.',
                'Error');

            })
              .success(function (data) {
              bar.set('Redirecting to new paste...', '100%');

              if (data.status === 'error') {
                zerobin.message('error', data.message, 'Error');
                $form.prop('disabled', false);
                bar.container.hide();
              } else {
                var paste_url = '/paste/' + data.paste + '#' + key;
                if (zerobin.support.localStorage) {
                  zerobin.storePaste(paste_url);
                }
                window.location = (paste_url);
              }
            });
          });
        } catch (err) {
          $form.prop('disabled', false);
          bar.container.hide();
          zerobin.message('error', 'Paste could not be encrypted. Aborting.',
            'Error');
        }
      }
    });

    /**
    DECRYPTION:
    On the display paste page, decrypt and decompress the paste content,
    add syntax coloration then setup the copy to clipboard button.
    Also calculate and set the paste visual hash.
*/
    var content = $('#paste-content').text().trim();
    var key = zerobin.getPasteKey();
    var error = false;

    if (content && key) {

      /* Load the lib for visual canvas, create one from the paste id and
     insert it */
      $.getScript("/static/js/vizhash.min.js").done(function (script, textStatus) {
        if (vizhash.supportCanvas) {
          var vhash = vizhash.canvasHash(zerobin.getPasteId(), 24, 24);
          $('<a class="vhash" href="#"></a>').click(function (e) {
            e.preventDefault();
            if (confirm("This picture is unique to your paste so you can identify" +
              " it quickly. \n\n Do you want to know more about this?")) {
              window.open("http://is.gd/IJaMRG", "_blank");
            }
          }).prependTo('.lnk-option').append(vhash.canvas);
        }
      });

      var $form = $('input, textarea, select, button').prop('disabled', true);

      var bar = zerobin.progressBar('.well form .progress');
      bar.container.show();
      bar.set('Decrypting paste...', '25%');

      zerobin.decrypt(key, content,

      /* On error*/
      function () {
        bar.container.hide();
        zerobin.message('error', 'Could not decrypt data (Wrong key ?)', 'Error');
      },

      /* Update progress bar */
      mkcb(bar.set, 'Decompressing...', '45%'),
      mkcb(bar.set, 'Base64 decoding...', '65%'),
      mkcb(bar.set, 'From bits to string...', '85%'),

      /* When done */
      function (content) {

        /* Decrypted content goes back to initial container*/
        $('#paste-content').text(content);

        if (content.indexOf('data:image') == 0) {
          // Display Image
          $('#paste-content').hide();
          var img = $('<img/>');
          $(img).attr('src', content);
          $(img).css('max-width', '742px');
          $('#paste-content').after(img);

          // Display Download button
          $('.btn-clone').hide();

          var button = $('<a/>').attr('href', content);
          $(button).attr('download', '0bin_' + document.location.pathname.split('/').pop());
          $(button).addClass('btn');
          $(button).html('<i class="icon-download"></i> Download');
          $('.btn-clone').after(button);

        }
        bar.set('Code coloration...', '95%');

        /* Add a continuation to let the UI redraw */
        setTimeout(function () {

          /* Setup flash clipboard button */
          ZeroClipboard.setMoviePath('/static/js/ZeroClipboard.swf');

          var clip = new ZeroClipboard.Client();

          // Callback to reposition the clibpboad flash animation overlay
          var reposition = function () {
            clip.reposition();
          };

          clip.addEventListener('mouseup', function () {
            $('#clip-button').text('Copying paste...');
            clip.setText(zerobin.getPasteContent());
          });
          clip.addEventListener('complete', function () {
            $('#clip-button').text('Copy to clipboard');
            zerobin.message('info', 'The paste is now in your clipboard', '',
            true, reposition);
          });
          clip.glue('clip-button');

          window.onresize = reposition;


          /* Setup link to get the paste short url*/
          $('#short-url').click(function (e) {
            e.preventDefault();
            $('#short-url').text('Loading short url...');
            zerobin.getTinyURL(window.location.toString(), function (tinyurl) {
              clip.setText(tinyurl);
              $('#copy-success').hide();
              zerobin.message('success',
                '<a href="' + tinyurl + '">' + tinyurl + '</a>',
                'Short url', true, reposition);
              $('#short-url').text('Get short url');
            });
          });

          /* Remap the message close handler to include the clipboard
           flash reposition */
          $(".close").die().live('click', function (e) {
            e.preventDefault();
            $(this).parent().fadeOut(reposition);
          });

          /** Syntaxic coloration */

          if (zerobin.isCode(content) > 100) {
            $('#paste-content').addClass('linenums');
            prettyPrint();
          } else {
            if (content.indexOf('data:image') != 0) {
              zerobin.message('info',
                "The paste did not seem to be code, so it " +
                "was not colorized. " +
                "<a id='force-coloration' href='#'>Force coloration</a>",
                '', false, reposition);
            }
          }

          /* Class to switch to paste content style with coloration done */
          $('#paste-content').addClass('done');

          /* Display result */
          bar.set('Done', '100%');
          bar.container.hide();

          $form.prop('disabled', false);
          content = '';

        }, 250);

      });

    } /* End of "DECRYPTION" */

    /* Synchronize expiration select boxes value */
    $('.paste-option select').live('change', function () {
      $('.paste-option select').val($(this).val());
    });


    /* Resize Textarea according to content */
    $('#content').elastic();


    /* Display bottom paste option buttons when needed */
    $('#content').live('keyup change', function () {
      if ($('#content').height() < 400) {
        $('.paste-option.down').remove();
      } else {

        if ($('.paste-option').length === 1) {
          $('.paste-option').clone().addClass('down').appendTo('form.well');
        }
      }

    });


    /* Display previous pastes */
    if (zerobin.support.localStorage) {

      var $container = $('.previous-pastes'),
        pastes = zerobin.getPreviousPastes();

      if (pastes.length) {

        $.getScript("/static/js/vizhash.min.js").done(function (script, textStatus) {

          $container.find('.item').remove();
          $.each(zerobin.getPreviousPastes(), function (i, paste) {

            var $li = $('<li class="item"></li>').appendTo($container);
            var $link = $('<a></a>').attr('href', paste.link)
              .text(paste.prefix + paste.displayDate)
              .appendTo($li);

            if (vizhash.supportCanvas) {
              var pasteId = zerobin.getPasteId(paste.link);
              var vhash = vizhash.canvasHash(pasteId, 24, 24).canvas;
              $link.prepend($(vhash).addClass('vhash'));
            }

            // hightlite the current link and make sure clicking the link
            // does redirect to the page
            if (paste.link.replace(/#[^#]+/, '') === window.location.pathname) {
              $li.addClass('active');
              $link.click(function () {
                window.location = $link.attr('href');
                window.location.reload();
              });
            }

          });

        });

      }

    }


    /* Event handler for "clone paste" button */
    $('.btn-clone').click(function (e) {
      e.preventDefault();
      $('.submit-form').show();
      $('.paste-form').hide();
      $('#content').val(zerobin.getPasteContent()).trigger('change');
    });

    $('.clone .btn-danger').click(function (e) {
      e.preventDefault();
      $('.submit-form').hide();
      $('.paste-form').show();
    });



    /* Upload file using HTML5 File API */
    if (zerobin.support.fileUpload) {

      var $buttonOverlay = $('#file-upload');
      var $button = $('.btn-upload');

      try {
        $button.val('Uploading...');
        $button.prop('disabled', true);
        $buttonOverlay.change(function () {
          zerobin.upload(this.files);
        });
      } catch (e) {
        zerobin.message('error', 'Could no upload the file', 'Error');
        $button.val('Upload File');
        $button.prop('disabled', false);
      }

      $button.prop('disabled', false);
      $button.val('Upload File');
      $buttonOverlay.mouseover(mkcb($(this).css, 'cursor', 'pointer'));

      // Implements drag & drop upload
      $('#content').bind('drop', zerobin.handleDrop);
      $('#content').bind('dragover', zerobin.handleDragOver);
      $('#content').bind('dragleave', zerobin.handleDragLeave);


    }

    /* Alerts */

    $(".close").live('click', function (e) {
      e.preventDefault();
      $(this).parent().fadeOut();
    });


    /* Parse obfuscaded emails and make them usable */
    $('.email-link').each(function (i, elem) {
      var $obfuscatedEmail = $(this);
      var address = $obfuscatedEmail.attr('title').replace('__AT__', '@');
      var text = $obfuscatedEmail.text().replace('__AT__', '@');
      var $plainTextEmail = $('<a href="mailto:' + address + '">' + text + '</a>');
      $obfuscatedEmail.replaceWith($plainTextEmail);

    });

    /* Show the page using javascript. Non js enabled browser will see an
   error message */
    $('#wrap-content').each(function (i, elem) {
      $(elem).show();
    });

    /* Remove expired pasted from history */
    if (zerobin.support.history && zerobin.paste_not_found) {
      var paste_id = zerobin.getPasteId();
      var keys = zerobin.getLocalStorageKeys();
      $.each(keys, function (i, key) {
        if (localStorage[key].indexOf(paste_id) !== -1) {
          localStorage.removeItem(key);
          return false;
        }
      });
    }


    /* Force text coloration when clickin on link */
    $("#force-coloration").live("click", function (e) {
      e.preventDefault();
      $('#paste-content').addClass('linenums');
      $(this).die(e).text('Applying coloration');
      prettyPrint();
      $(this).remove();
    });

    /* Send the paste by email */
    $('#email-link').click(function() {
    	zerobin.getTinyURL(window.location.toString(), function(tinyurl) {
    		document.location.href= 'mailto:friend@example.com?body=' + tinyurl;
    	});
    	return false;
    });


  }); /* End of "document ready" jquery callback */

})(); /* End of self executing function */
