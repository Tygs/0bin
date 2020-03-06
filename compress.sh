#! /bin/bash

COMMAND="node node_modules/yui-compressor/lib/index.js";
command -v $COMMAND >/dev/null 2>&1 || { echo >&2 "Error: this script requires the command '$COMMAND' to be available"; exit 1; }

CURDIR=$(dirname $(readlink -f $0));
STATICDIR=$CURDIR'/zerobin/static/'
CSSDIR=$STATICDIR'css/'
JSDIR=$STATICDIR'js/'

MAIN_JS_OUTPUT=$JSDIR"main.min.js";
ADDITIONAL_JS_OUTPUT=$JSDIR"additional.min.js";
CSS_OUTPUT=$CSSDIR"style.min.css"

cat /dev/null > $CSS_OUTPUT;

echo "Compressing CSS..."

echo $'\n''/* Bootstrap */' >> $CSS_OUTPUT;
$COMMAND $CSSDIR'bootstrap.min.css' >> $CSS_OUTPUT;
echo $'\n''/* Prettify */' >> $CSS_OUTPUT;
cat $CSSDIR'prettify.css' >> $CSS_OUTPUT;
echo $'\n''/* Custom */' >> $CSS_OUTPUT;
$COMMAND $CSSDIR'style.css' >> $CSS_OUTPUT;

echo "Compressing JS..."

cat /dev/null > $MAIN_JS_OUTPUT;

echo $'\n''/* jQuery */' >> $MAIN_JS_OUTPUT;
cat $JSDIR'jquery-1.7.2.min.js' >> $MAIN_JS_OUTPUT;
# strip the "use strict" statement because it will apply to all the files
# TODO: file a bug report to SJCL to invite them to use the function syntax
echo $'\n''/* SJCL */' >> $MAIN_JS_OUTPUT;
cat $JSDIR'sjcl.js' | sed 's/"use strict";//' >> $MAIN_JS_OUTPUT;
echo $'\n''/* custom */' >> $MAIN_JS_OUTPUT;
$COMMAND $JSDIR'behavior.js' >> $MAIN_JS_OUTPUT;

cat /dev/null > $ADDITIONAL_JS_OUTPUT;

echo $'\n''/* jQuery Elastic */' >> $ADDITIONAL_JS_OUTPUT;
$COMMAND $JSDIR'jquery.elastic.source.js' >> $ADDITIONAL_JS_OUTPUT;
echo $'\n''/* lzw */' >> $ADDITIONAL_JS_OUTPUT;
$COMMAND $JSDIR'lzw.js' >> $ADDITIONAL_JS_OUTPUT;
echo $'\n''/* prettify */' >> $ADDITIONAL_JS_OUTPUT;
cat $JSDIR'prettify.min.js' >> $ADDITIONAL_JS_OUTPUT;

echo "Done"
