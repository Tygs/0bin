// Author: Anthony McKale
//
// Note: modifed to javascript from orginal as2 found below
// basically identical actual to as2
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

