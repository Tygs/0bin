;
// Start random number generator seeding ASAP
sjcl.random.startCollectors();

$(function(){

function encrypt(key, content) {
  content = lzw.compress(sjcl.encrypt(key, content));
  content = sjcl.codec.utf8String.toBits(content);
  return sjcl.codec.base64.fromBits(content);
}

function decrypt(key, content) {
  content = sjcl.codec.base64.toBits(content);
  content = sjcl.codec.utf8String.fromBits(content);
  return sjcl.decrypt(key, lzw.decompress(content));
}

function make_key() {
  return sjcl.codec.base64.fromBits(sjcl.random.randomWords(8, 0), 0);
}

$('button[type=submit]').click(function(e){

  e.preventDefault();
  var paste = $('textarea').val();

  if (paste.trim()) {
    var expiration = $('#expiration').val();
    var key = make_key();
    var data = {content: encrypt(key, paste), expiration: expiration}

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


});