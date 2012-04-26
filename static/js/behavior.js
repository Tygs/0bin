;

// Start random number generator seeding ASAP
sjcl.random.startCollectors();

var zerobin = {
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
        window.location = '/paste/' + data + '#' + key;
     });
  }

});

var content = $('#paste-content').text().trim();
var key = window.location.hash.substring(1);
if (content && key) {
    try {
        $('#paste-content').text(zerobin.decrypt(key, content));
        hljs.highlightBlock($('#paste-content')[0]);
    } catch(err) {
        alert('Could not decrypt data (Wrong key ?)');
    }
}

});