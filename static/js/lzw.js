// Author: Anthony McKale
//
// Note: modifed to javascript from orginal as2 found below
// basically identical actual to as2
//
//
// http://www.razorberry.com/blog/archives/2004/08/22/lzw-compression-methods-in-as2/
//
// A class for LZW compression modified from code posted at the following URL's
// http://www.shoe-box.org/blog/index.php/2004/05/05/13-CompressionLzw
// http://www.lalex.com/blog/comments/200405/164-compression-lzw-actionscript-2.html
//
var lzw = {
    // Change this variable to output an xml safe string
    xmlsafe : false,
    compress : function(str){
        var dico = new Array();
        var skipnum = lzw.xmlsafe?5:0;
        for (var i = 0; i < 256; i++)
        {
            dico[String.fromCharCode(i)] = i;
        }
        if (lzw.xmlsafe)
        {
            dico["<"] = 256;
            dico[">"] = 257;
            dico["&"] = 258;
            dico["\""] = 259;
            dico["'"] = 260;
        }
        var res = "";
        var txt2encode = str;
        var splitStr = txt2encode.split("");
        var len = splitStr.length;
        var nbChar = 256+skipnum;
        var buffer = "";
        for (var i = 0; i <= len; i++)
        {
            var current = splitStr[i];
            if (dico[buffer + current] !== undefined)
            {
                buffer += current;
            }
            else
            {
                res += String.fromCharCode(dico[buffer]);
                dico[buffer + current] = nbChar;
                nbChar++;
                buffer = current;
            }
        }
        return res;
    },
    decompress : function (str)
    {
        var dico = new Array();
        var skipnum = lzw.xmlsafe?5:0;
        for (var i = 0; i < 256; i++)
        {
            var c = String.fromCharCode(i);
            dico[i] = c;
        }
        if (lzw.xmlsafe)
        {
            dico[256] = "<";
            dico[257] = ">";
            dico[258] = "&";
            dico[259] = "\"";
            dico[260] = "'";
        }
        var txt2encode = str;
        var splitStr = txt2encode.split("");
        var length = splitStr.length;
        var nbChar = 256+skipnum;
        var buffer = "";
        var chaine = "";
        var result = "";
        for (var i = 0; i < length; i++)
        {
            var code = txt2encode.charCodeAt(i);
            var current = dico[code];
            if (buffer == "")
            {
                buffer = current;
                result += current;
            }
            else
            {
                if (code <= 255+skipnum)
                {
                    result += current;
                    chaine = buffer + current;
                    dico[nbChar] = chaine;
                    nbChar++;
                    buffer = current;
                }
                else
                {
                    chaine = dico[code];
                    if (chaine == undefined) chaine = buffer + buffer.slice(0,1);
                    result += chaine;
                    dico[nbChar] = buffer + chaine.slice(0, 1);
                    nbChar++;
                    buffer = chaine;

                }
            }
        }
        return result;
    }
}


// LZW-compress a string
function lzw_encode(s) {
    var dict = {};
    var data = (s + "").split("");
    var out = [];
    var currChar;
    var phrase = data[0];
    var code = 256;
    for (var i=1; i<data.length; i++) {
        currChar=data[i];
        if (dict[phrase + currChar] != null) {
            phrase += currChar;
        }
        else {
            out.push(phrase.length > 1 ? dict[phrase] : phrase.charCodeAt(0));
            dict[phrase + currChar] = code;
            code++;
            phrase=currChar;
        }
    }
    out.push(phrase.length > 1 ? dict[phrase] : phrase.charCodeAt(0));
    for (var i=0; i<out.length; i++) {
        out[i] = String.fromCharCode(out[i]);
    }
    return out.join("");
}

// Decompress an LZW-encoded string
function lzw_decode(s) {
    var dict = {};
    var data = (s + "").split("");
    var currChar = data[0];
    var oldPhrase = currChar;
    var out = [currChar];
    var code = 256;
    var phrase;
    for (var i=1; i<data.length; i++) {
        var currCode = data[i].charCodeAt(0);
        if (currCode < 256) {
            phrase = data[i];
        }
        else {
           phrase = dict[currCode] ? dict[currCode] : (oldPhrase + currChar);
        }
        out.push(phrase);
        currChar = phrase.charAt(0);
        dict[code] = oldPhrase + currChar;
        code++;
        oldPhrase = phrase;
    }
    return out.join("");
}



/* utf.js - UTF-8 <=> UTF-16 convertion
 *
 * Copyright (C) 1999 Masanao Izumo <iz@onicos.co.jp>
 * Version: 1.0
 * LastModified: Dec 25 1999
 * This library is free.  You can redistribute it and/or modify it.
 */

/*
 * Interfaces:
 * utf8 = utf16to8(utf16);
 * utf16 = utf16to8(utf8);
 */

function utf16to8(str) {
    var out, i, len, c;

    out = "";
    len = str.length;
    for(i = 0; i < len; i++) {
    c = str.charCodeAt(i);
    if ((c >= 0x0001) && (c <= 0x007F)) {
        out += str.charAt(i);
    } else if (c > 0x07FF) {
        out += String.fromCharCode(0xE0 | ((c >> 12) & 0x0F));
        out += String.fromCharCode(0x80 | ((c >>  6) & 0x3F));
        out += String.fromCharCode(0x80 | ((c >>  0) & 0x3F));
    } else {
        out += String.fromCharCode(0xC0 | ((c >>  6) & 0x1F));
        out += String.fromCharCode(0x80 | ((c >>  0) & 0x3F));
    }
    }
    return out;
}

function utf8to16(str) {
    var out, i, len, c;
    var char2, char3;

    out = "";
    len = str.length;
    i = 0;
    while(i < len) {
    c = str.charCodeAt(i++);
    switch(c >> 4)
    {
      case 0: case 1: case 2: case 3: case 4: case 5: case 6: case 7:
        // 0xxxxxxx
        out += str.charAt(i-1);
        break;
      case 12: case 13:
        // 110x xxxx   10xx xxxx
        char2 = str.charCodeAt(i++);
        out += String.fromCharCode(((c & 0x1F) << 6) | (char2 & 0x3F));
        break;
      case 14:
        // 1110 xxxx  10xx xxxx  10xx xxxx
        char2 = str.charCodeAt(i++);
        char3 = str.charCodeAt(i++);
        out += String.fromCharCode(((c & 0x0F) << 12) |
                       ((char2 & 0x3F) << 6) |
                       ((char3 & 0x3F) << 0));
        break;
    }
    }

    return out;
}