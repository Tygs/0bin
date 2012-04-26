;
// Start random number generator seeding ASAP
sjcl.random.startCollectors();

var zerobin = function() {
  that = {};
  that.base64 =  {
    decode: function(content) {
      return sjcl.codec.utf8String.fromBits(sjcl.codec.base64.toBits(content));
    },
    encode: function(content) {
      return sjcl.codec.base64.fromBits(sjcl.codec.utf8String.toBits(content));
    }
  };
  that.encrypt = function(key, content) {
    var encrypted = sjcl.encrypt(key, content);
    return lzw.compress(encrypted);
  };
  that.decrypt = function(key, content) {
    var uncompressed = lzw.decompress(content)
    return sjcl.decrypt(key, uncompressed);
  };
  that.make_key = function() {
    return sjcl.codec.base64.fromBits(sjcl.random.randomWords(8, 0), 0);
  };
  return that;
}();

$(function(){

$('button[type=submit]').click(function(e){

  e.preventDefault();
  var paste = $('textarea').val();

  if (paste.trim()) {
    var expiration = $('#expiration').val();
    var key = zerobin.make_key();
    var data = {content: zerobin.encrypt(key, paste), expiration: expiration}

    $.post('/paste/create', data)
     .error(function() {
        alert('Paste could not be saved. Please try again later.');
     })
     .success(function(data) {
        alert('success');
        window.location = '/paste/' + data + '#' + key;
     });
  }

});

var content = $('#paste-content').text().trim();
var key = window.location.hash.substring(1);
if (content && key) {
    try {
        $('#paste-content').text(zerobin.decrypt(key, content));
    } catch(err) {
        alert('Could not decrypt data (Wrong key ?)');
    }
}

});