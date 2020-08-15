/*global sjcl:true, jQuery:true, lzw:true, zerobin:true, prettyPrint:true */

/*
  This file has been migrated away from jQuery, to Vue. Because of the way
  the code base used to be, a lot of the operations are still using imperative
   DOM manipulation instead of the Vue declarative style. We haven't had the
   time to rewrite it completly and it's a bit of a mixed bag at the moment.
*/

/* Start random number generator seeding ASAP */
sjcl.random.startCollectors();

// Vue template syntax conflicts with bottle template syntax
Vue.options.delimiters = ['{%', '%}'];

// Force focus for textarea (firefox hack)
setTimeout(function () {
  document.getElementById('content').focus();
}, 100)

var app = new Vue({

  el: '#app',
  data: {
    previousPastes: [],
    displayBottomToolBar: false,
    openPreviousPastesMenu: false,
    readerMode: false,
    isUploading: false,
    btcCopied: false,
    currentPaste: {
      ownerKey: '',
      id: '',
      type: '',
      content: '',
      downloadLink: {},
      title: '',
      btcTipAddress: ''
    },
    newPaste: {
      expiration: '1_day',
      content: '',
      title: '',
      btcTipAddress: ''
    },
    messages: [],
    /** Check for browser support of the named featured. Store the result
    and add a class to the html tag with the result */
    support: {

      clipboard: !!(isSecureContext && navigator.clipboard && navigator.clipboard.writeText),

      URLSearchParams: !!window.URLSearchParams,

      localStorage: (function () {
        var val = !!(localStorage);
        document.querySelector('html').classList.add((val ? '' : 'no-') + 'local-storage');
        return val;
      })(),

      history: (function () {
        var val = !!(window.history && history.pushState);
        document.querySelector('html').classList.add((val ? '' : 'no-') + 'history');
        return val;
      })(),

      fileUpload: (function () {
        var w = window;
        var val = !!(w.File && w.FileReader && w.FileList && w.Blob);
        document.querySelector('html').classList.add((val ? '' : 'no-') + 'file-upload');
        return val;
      })()
    },
    isLoading: false
  },
  methods: {

    toggleReaderMode: function () {
      if (!this.readerMode) {
        this.messages = [];
        if (this.support.URLSearchParams) {
          var searchParams = new URLSearchParams(window.location.search);
          searchParams.set('readerMode', 1);
          window.location.search = searchParams.toString();
        }
      } else {
        if (this.support.URLSearchParams) {
          var searchParams = new URLSearchParams(window.location.search);
          searchParams.delete('readerMode');
          window.location.search = searchParams.toString();
        }
      }

      this.readerMode = !this.readerMode;
    },

    increaseFontSize: function (amount) {
      var readableModeContent = document.getElementById('readable-paste-content');

      var fontSize = window.getComputedStyle(readableModeContent, null).getPropertyValue('font-size');

      amount = amount || 5;
      readableModeContent.style.fontSize = (parseFloat(fontSize) + amount) + "px";
    },

    decreaseFontSize: function () {
      this.increaseFontSize(-5);
    },

    formatEmail: function (email) {
      return "mailto:" + email.replace('__AT__', '@');
    },

    forceLoad: function (link) {
      window.location = link;
      window.location.reload();
    },

    handleClone: function () {

      document.querySelector('.submit-form').style.display = "inherit";
      document.querySelector('.paste-form').style.display = "none";
      var title = document.querySelector('h1');
      if (title) {
        title.style.display = "none";
      }
      var content = document.getElementById('content');
      content.value = zerobin.getPasteContent();
      content.dispatchEvent(new Event('change'));
      this.newPaste.title = this.currentPaste.title;
      this.newPaste.btcTipAddress = this.currentPaste.btcTipAddress;
    },

    handleCancelClone: function () {
      document.querySelector('.submit-form').style.display = "none";
      document.querySelector('.paste-form').style.display = "inherit";
      document.querySelector('h1').style.display = "inherit";
    },

    handleUpload: function (files) {
      try {
        app.isUploading = true;
        zerobin.upload(files);
      } catch (e) {
        zerobin.message('danger', 'Could no upload the file', 'Error');
      }
      app.isUploading = false;
    },

    handleForceColoration: function (e) {
      var content = document.getElementById('paste-content');
      content.classList.add('linenums');
      e.target.innerHTML = 'Applying coloration';
      prettyPrint();
      e.target.parentNode.remove()
    },

    handleSendByEmail: function (e) {
      window.location = 'mailto:friend@example.com?body=' + window.location.toString();
    },

    handleDeletePaste: function () {
      if (window.confirm("Delete this paste?")) {
        app.isLoading = true;
        bar.set('Deleting paste...', '50%');

        fetch('/paste/' + app.currentPaste.id, {
          method: "DELETE",
          body: new URLSearchParams({
            "owner_key": app.currentPaste.ownerKey
          })
        }).then(function (response) {
          if (response.ok) {
            window.location = "/";
          } else {
            form.forEach(function (node) {
              node.disabled = false;
            });
            app.isLoading = false
            zerobin.message(
              'danger',
              'Paste could not be deleted. Please try again later.',
              'Error');
          }
          app.isLoading = false;
        }).catch(function (error) {
          zerobin.message(
            'danger',
            'Paste could not be delete. Please try again later.',
            'Error');
          app.isLoading = false;
        });
      }
    },

    copyToClipboard: function () {

      var pasteContent = zerobin.getPasteContent();
      var promise = navigator.clipboard.writeText(pasteContent);

      promise.then(function () {
        zerobin.message('primary', 'The paste is now in your clipboard', '', true);
      }, function (err) {
        zerobin.message('danger', 'The paste could not be copied', '', true);
      });

    },

    copyBTCAdressToClipboard: function () {

      var promise = navigator.clipboard.writeText(this.currentPaste.btcTipAddress);

      app.btcCopied = true;

      promise.then(function () {

        if (app.btcCopied) {
          clearTimeout(app.btcCopied);
        }
        app.btcCopied = setTimeout(function () {
          app.btcCopied = false;
        }, 3000)
      }, function (err) {
        zerobin.message('danger', 'The BTC addresse could not be copied', '', true);
      });

    },

    compressImage: function (base64) {
      var canvas = document.createElement('canvas')
      var img = document.createElement('img')

      return new Promise(function (resolve, reject) {
        img.onload = function () {
          var width = img.width;
          var height = img.height;
          var biggest = width > height ? width : height;
          var maxHeight = height;
          var maxWidth = width;

          if (width > height) {
            if (width > maxWidth) {
              height = Math.round((height *= maxWidth / width));
              width = maxWidth;
            }
          } else {
            if (height > maxHeight) {
              width = Math.round((width *= maxHeight / height));
              height = maxHeight;
            }
          }
          canvas.width = width;
          canvas.height = height;

          var ctx = canvas.getContext('2d');
          ctx.drawImage(img, 0, 0, width, height);

          resolve(canvas.toDataURL('image/jpeg', 0.7));
        }
        img.onerror = function (err) {
          reject(err);
        }
        img.src = base64;

      })
    },

    /**
      On the create paste page:
      On click on the send button, compress and encrypt data before
      posting it using ajax. Then redirect to the address of the
      newly created paste, adding the key in the hash.
    */

    encryptAndSendPaste: function () {

      var paste = document.querySelector('textarea').value;

      if (paste.trim()) {

        var form = document.querySelectorAll('input, textarea, select, button');

        form.forEach(function (node) {
          node.disabled = true;
        });

        // set up progress bar
        var bar = zerobin.progressBar('form.well .progress');
        app.isLoading = true;
        bar.set('Converting paste to bits...', '25%');

        /* Encode, compress, encrypt and send the paste then redirect the user
          to the new paste. We ensure a loading animation is updated
          during the process by passing callbacks.
        */
        try {

          var key = zerobin.makeKey(256);

          var promise = new Promise(function (resolve, reject) {
            resolve(paste);
          }); // noop to avoid branching
          if (paste.indexOf('data:image') == 0) {
            promise = app.compressImage(paste);
          }

          promise.then(function (base64) {
              zerobin.encrypt(key, base64,

                function () {
                  bar.set('Encoding to base64...', '45%')
                },
                function () {
                  bar.set('Compressing...', '65%')
                },
                function () {
                  bar.set('Encrypting...', '85%')
                },

                /* This block deals with sending the data, redirection or error handling */
                function (content) {

                  bar.set('Sending...', '95%');
                  var data = {
                    content: content,
                    expiration: app.newPaste.expiration,
                    title: app.newPaste.title,
                    btcTipAddress: app.newPaste.btcTipAddress
                  };
                  var sizebytes = zerobin.count(JSON.stringify(data));
                  var oversized = sizebytes > zerobin.max_size; // 100kb - the others header information
                  var readableFsize = Math.round(sizebytes / 1024);
                  var readableMaxsize = Math.round(zerobin.max_size / 1024);

                  if (oversized) {
                    app.isLoading = false
                    form.forEach(function (node) {
                      node.disabled = false;
                    });

                    zerobin.message('danger', ('The file was <strong class="file-size">' + readableFsize +
                        '</strong>KB after encryption. You have reached the maximum size limit of ' + readableMaxsize + 'KB.'),
                      'Warning!', true);
                    return;
                  }

                  fetch('/paste/create', {
                    method: "POST",
                    body: new URLSearchParams(data)
                  }).then(function (response) {
                    if (response.ok) {
                      bar.set('Redirecting to new paste...', '100%');

                      response.json().then(function (data) {
                        if (data.status === 'error') {
                          zerobin.message('danger', data.message, 'Error');
                          form.forEach(function (node) {
                            node.disabled = false;
                          });
                          app.isLoading = false;
                        } else {
                          if (app.support.localStorage) {
                            zerobin.storePaste('/paste/' + data.paste + "?owner_key=" + data.owner_key + '#' + key);
                          }
                          window.location = ('/paste/' + data.paste + '#' + key);
                        }
                      })

                    } else {
                      form.forEach(function (node) {
                        node.disabled = false
                      });
                      app.isLoading = false;
                      zerobin.message(
                        'danger',
                        'Paste could not be saved. Please try again later.',
                        'Error');
                    }
                  }).catch(function (error) {
                    form.forEach(function (node) {
                      node.disabled = false;
                    });
                    app.isLoading = false;
                    zerobin.message(
                      'danger',
                      'Paste could not be saved. Please try again later.',
                      'Error');
                  });

                })
            }),
            function (err) {
              debugger;
              form.forEach(function (node) {
                node.disabled = false;
              });
              app.isLoading = false;
              zerobin.message('danger', 'Paste could not be encrypted. Aborting.',
                'Error');
            };

        } catch (err) {
          form.forEach(function (node) {
            node.disabled = false;
          });
          app.isLoading = false;
          zerobin.message('danger', 'Paste could not be encrypted. Aborting.',
            'Error');
        }
      }
    }
  }
})

/****************************
 ****  0bin utilities    ****
 ****************************/

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

              document.querySelectorAll('input, textarea, select, button').forEach(function (node) {
                node.disabled = true
              });

              app.isLoading = false;

              zerobin.message('danger', 'Paste could not be encrypted. Aborting.',
                'Error');
            }
            if (doneCallback) {
              doneCallback(content);
            }
          }, 50);

        }, 50);

      }, 50);

    }, 50);
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
                    debugger;
                    errorCallback(err);
                  }

                }, 50); /* "End of from bits to string" */

              } catch (err) {
                errorCallback(err);
              }

            }, 50); /* End of "from base 64 to bits" */

          } catch (err) {
            errorCallback(err);
          }

        }, 50); /* End of "decompress" */

      } catch (err) {
        errorCallback(err);
      }

    }, 50); /* End of "decrypt" */
  },

  /** Create a random base64-like string long enought to be suitable as
      an encryption key */
  makeKey: function (entropy) {
    entropy = Math.ceil(entropy / 6) * 6; /* non-6-multiple produces same-length base64 */
    var key = sjcl.bitArray.clamp(
      sjcl.random.randomWords(Math.ceil(entropy / 32), 0), entropy);
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
  getLocalStorageURLKeys: function () {
    var version = 'zerobinV' + zerobin.version;
    var keys = [];
    for (var key in localStorage) {
      if (key.indexOf(version) !== -1 && key.indexOf("owner_key") === -1) {
        keys.push(key);
      }
    }
    keys.sort();
    keys.reverse();
    return keys;
  },

  /** Store the paste of a URL in local storate, with a storage format
    version prefix and the paste date as the key */
  storePaste: function (url, date) {

    date = date || new Date();
    date = (date.getFullYear() + '-' + (date.getMonth() + 1) + '-' + date.getDate() + ' ' + zerobin.getFormatedTime(date));

    var keys = zerobin.getLocalStorageURLKeys();

    if (localStorage.length > 19) {
      void localStorage.removeItem(keys[19]);
    }

    localStorage.setItem('zerobinV' + zerobin.version + "#" + date, url);
    localStorage.setItem('zerobinV' + zerobin.version + "#" + zerobin.getPasteId(url) + "#owner_key", zerobin.getPasteOwnerKey(url));
  },

  /** Return a list of the previous paste url with the creation date
      If the paste is from today, date format should be "at hh:ss",
      else it should be "the mm-dd-yyy"
  */
  getPreviousPastes: function () {
    var keys = zerobin.getLocalStorageURLKeys(),
      today = zerobin.getFormatedDate();

    return keys.map(function (key, i) {
      var pasteDateTime = key.replace(/^[^#]+#/, '');
      var displayDate = pasteDateTime.match(/^(\d+)-(\d+)-(\d+)\s/);
      displayDate = displayDate[2] + '-' + displayDate[3] + '-' + displayDate[1];
      var prefix = 'the ';
      if (displayDate === today) {
        displayDate = pasteDateTime.split(' ')[1];
        prefix = 'at ';
      }
      var link = localStorage.getItem(key);

      return {
        displayDate: displayDate,
        prefix: prefix,
        // The owner key is stored in the URL, but we don't want the user
        // to see it
        link: link.replace(/\?[^#]+#/, '#'),
        isCurrent: link.replace(/\?[^?]+/, '') === window.location.pathname
      };
    });

  },

  /** Return a link object with the URL as href so you can extract host,
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

  getPasteOwnerKey: function (url) {
    var loc = url ? zerobin.parseUrl(url) : window.location;
    return (new URLSearchParams(loc.search)).get("owner_key");
  },

  getPasteKey: function (url) {
    var loc = url ? zerobin.parseUrl(url) : window.location;
    return loc.hash.replace('#', '').replace(/(\?|&).*$/, '');
  },

  /** Return the paste content stripted from any code coloration */
  getPasteContent: function () {
    var copy = '';
    document.querySelectorAll("#paste-content li").forEach(function (node) {
      copy = copy + node.textContent.replace(/[\u00a0]+/g, ' ') + '\n';

    });
    if (copy === '') {
      copy = document.querySelector("#paste-content").textContent;
    }
    return copy;
  },

  /** Return an approximate estimate of the number of bytes in a text */
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
  message: function (type, message, title, flush, callback, action) {
    window.scrollTo(0, 0);
    if (flush) {
      app.messages = app.messages.filter(function (msg) {
        msg.type !== type
      });
    }
    app.messages.push({
      title: title,
      content: message,
      type: type,
      action: action || {},
    });
    callback && callback();
  },

  /** Return a progress bar object */
  progressBar: function (selector) {
    var container = document.querySelector(selector);
    var bar = {
      container: container,
      elem: container.childNodes[0]
    };
    bar.set = function (text, rate) {
      bar.elem.innerHTML = text;
      bar.elem.style.width = rate;
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

  ignoreDrag: function (e) {
    e.stopPropagation();
    e.preventDefault();
  },

  handleDrop: function (e) {
    e.preventDefault();
    zerobin.upload(e.dataTransfer.files);
    document.getElementById("content").classList.remove("hover");
  },

  handlePaste: function (e) {
    var items = (event.clipboardData || event.originalEvent.clipboardData).items;
    for (var i = 0; i < items.length; i++) {
      if (items[i].type.indexOf("image") === 0) {
        e.preventDefault()
        return zerobin.upload([items[i].getAsFile()]);
      }
    }

  },

  handleDragOver: function (e) {
    zerobin.ignoreDrag(e);
    document.getElementById("content").classList.add('hover');
  },

  handleDragLeave: function (e) {
    document.getElementById("content").classList.remove("hover");
  },

  upload: function (files) {
    var content = document.getElementById('content');
    var currentFile = files[0];
    var reader = new FileReader();
    if (currentFile.type.indexOf('image') == 0) {
      reader.onload = function (event) {
        var image = new Image();
        image.src = event.target.result;
        content.value = event.target.result

        image.onload = function () {

          app.messages = []
          var previousImage = document.querySelector('.paste-wrapper');
          if (previousImage) {
            previousImage.remove();
          }
          var imgWrapper = document.createElement('div');
          imgWrapper.classList.add('paste-wrapper');
          imgWrapper.appendChild(image)
          content.style.display = "none";
          content.after(imgWrapper);
        }
      }
      reader.readAsDataURL(currentFile);
    } else {
      reader.onload = function (event) {
        content.value = event.target.result
        content.dispatchEvent(new Event('change'));
      };
      reader.readAsText(currentFile);
    }
  }
};

/**
    DECRYPTION:
    On the display paste page, decrypt and decompress the paste content,
    add syntax coloration then setup the copy to clipboard button.
    Also calculate and set the paste visual hash.
*/

var pasteContent = document.querySelector('#paste-content');
var content = '';

if (pasteContent) {
  content = pasteContent.textContent.trim();
  app.currentPaste.id = zerobin.getPasteId(window.location);
}

var key = zerobin.getPasteKey();
var error = false;

if (content && key) {

  var form = document.querySelectorAll('input, textarea, select, button');
  form.forEach(function (node) {
    node.disabled = true;
  });

  var bar = zerobin.progressBar('.well form .progress');
  app.isLoading = true;
  bar.set('Decrypting paste...', '25%');

  zerobin.decrypt(key, content,

    /* On error*/
    function () {
      app.isLoading = false;
      zerobin.message('danger', 'Could not decrypt data (Wrong key ?)', 'Error');
    },

    /* Update progress bar */
    function () {
      bar.set('Decompressing...', '45%');
    },
    function () {
      bar.set('Base64 decoding...', '65%');
    },
    function () {
      bar.set('From bits to string...', '85%');
    },

    /* When done */
    function (content) {

      var readerMode = false;

      if (content.indexOf('data:image') == 0) {
        // Display Image

        app.currentPaste.type = "image";
        var pasteContent = document.querySelector('#paste-content');
        pasteContent.style.display = "none";

        var imgWrapper = document.createElement('div');
        imgWrapper.classList.add('paste-wrapper');
        var img = document.createElement('img');
        img.src = content;

        pasteContent.after(imgWrapper);
        imgWrapper.appendChild(img);

        document.querySelectorAll('.btn-clone').forEach(function (node) {
          node.style.display = "none";
        });

        var extension = /data:image\/([^;]+);base64/.exec(content)[1];

        app.currentPaste.downloadLink = {
          name: '0bin_' + document.location.pathname.split('/').pop() + '.' + extension,
          url: content
        }

      } else {
        app.currentPaste.type = "text";
        /* Decrypted content goes back to initial container*/
        document.querySelector('#paste-content').innerText = content;
        app.currentPaste.content = content;

        app.currentPaste.downloadLink = {
          name: '0bin_' + document.location.pathname.split('/').pop() + ".txt",
          url: "data:text/html;charset=UTF-8," + content
        }

        if (app.support.URLSearchParams) {
          readerMode = (new URLSearchParams(window.location.search)).get('readerMode');
        }

      }
      bar.set('Code coloration...', '95%');

      /* Add a continuation to var the UI redraw */
      setTimeout(function () {

        /** Syntaxic coloration */

        if (zerobin.isCode(content) > 100 && !readerMode) {
          document.getElementById('paste-content').classList.add('linenums');
          prettyPrint();
        } else {
          if (content.indexOf('data:image') != 0) {
            zerobin.message('primary',
              "The paste did not seem to be code, so it " +
              "was not colorized. ",
              '', false, undefined, {
                message: "Click here to force coloration",
                callback: app.handleForceColoration
              });
          }
        }

        /* Class to switch to paste content style with coloration done */
        document.getElementById('paste-content').classList.add('done');

        /* Display result */
        bar.set('Done', '100%');
        app.isLoading = false;

        form.forEach(function (node) {
          node.disabled = false;
        });
        content = '';
        if (readerMode) {
          app.toggleReaderMode();
        }

      }, 100);

    });

} /* End of "DECRYPTION" */

window.onload = function () {

  /* Display bottom paste option buttons when needed */
  ["keyup", "change"].forEach(function (event) {
    var content = document.getElementById("content");
    content.addEventListener(event, function () {
      var height = parseFloat(getComputedStyle(content, null).height.replace("px", ""))
      app.displayBottomToolBar = height > 400;
    })
  })

  /* Remove expired pasted from history **/
  if (app.support.history && app.currentPaste.type === 'not_found') {

    var paste_id = zerobin.getPasteId();
    var keys = zerobin.getLocalStorageURLKeys();
    keys.forEach(function (key, i) {
      if (localStorage[key].indexOf(paste_id) !== -1) {
        localStorage.removeItem(key);
        return false;
      }
    })
  }

  var title = document.querySelector('h1');
  if (title) {
    app.currentPaste.title = title.innerText;
  }

  var btcTipAddress = document.querySelector('.btc-tip-address');
  if (btcTipAddress) {
    app.currentPaste.btcTipAddress = btcTipAddress.innerText;
  }

}

/* Display previous pastes */
if (app.support.localStorage) {
  app.previousPastes = zerobin.getPreviousPastes();
  app.currentPaste.ownerKey = localStorage.getItem('zerobinV' + zerobin.version + "#" + zerobin.getPasteId(window.location) + "#owner_key");
}

/* Upload file using HTML5 File API */
if (app.support.fileUpload) {

  // Implements drag & drop upload
  var content = document.getElementById('content');
  content.addEventListener('drop', zerobin.handleDrop);
  content.addEventListener('paste', zerobin.handlePaste);
  content.addEventListener('dragover', zerobin.handleDragOver);
  content.addEventListener('dragleave', zerobin.handleDragLeave);

}

/* Autofit text area height */
var tx = document.getElementsByTagName('textarea');
for (var i = 0; i < tx.length; i++) {
  tx[i].setAttribute('style', 'height:' + (tx[i].scrollHeight) + 'px;overflow-y:hidden;');
  tx[i].addEventListener("input", OnInput, false);
}

function OnInput() {
  this.style.height = 'auto';
  this.style.height = (this.scrollHeight) + 'px';
}
