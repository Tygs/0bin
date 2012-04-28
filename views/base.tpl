<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>0bin - encrypted pastebin</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description"
          content="0bin is a client-side-encrypted
                   pastebin with a burn after reading feature">

    <link rel="shortcut icon" href="/static/img/favicon.ico">
    <link href="/static/css/vs.css" rel="stylesheet" />
    <link href="/static/css/bootstrap.css" rel="stylesheet">
    <link href="/static/css/style.css" rel="stylesheet">

    <!-- Le HTML5 shim, for IE6-8 support of HTML5 elements -->
    <!--[if lt IE 9]>
      <script src="http://html5shim.googlecode.com/svn/trunk/html5.js"></script>
    <![endif]-->

    <script src="/static/js/sjcl.js"></script>
    <script src="/static/js/jquery-1.7.2.min.js"></script>
    <script src="/static/js/behavior.js"></script>

  </head>

  <body>

    <div class="navbar navbar-fixed-top">
      <div class="navbar-inner">
        <div class="container">
          <a class="btn btn-navbar" data-toggle="collapse"
             data-target=".nav-collapse">
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
          </a>
          <a class="brand" href="/"><span>ø</span>bin<em>.net</em></a>
          <div class="nav-collapse">
            <ul class="nav">
              <li class="active"><a href="#">Home</a></li>
              <li><a href="https://github.com/sametmax/0bin/downloads">Download 0bin</a></li>
              <li><a href="#faq">Faq</a></li>
            </ul>
            <p class="navbar-text pull-right"><i>"A client side encrypted PasteBin..."</i></p>
          </div><!--/.nav-collapse -->
        </div>
      </div>
    </div>

    <div class="container">
      <div class="row">
        <div class="span2">
          <div class="well sidebar-nav">
            <ul class="nav nav-list">
              <li class="nav-header">Previous pastes</li>
              <li><a href="#">paste 1</a></li>
              <li><a href="#">Paste 2</a></li>
            </ul>
          </div><!--/.well -->
        </div><!--/span-->

        <div class="span10">

           %include

        </div><!--/span-->

      </div><!--/row-->

      <hr>

      <footer>
       <blockquote>
        <p>«Few persons can be made to believe that it is not quite an easy thing to invent a method of secret writing which shall baffle investigation. Yet it may be roundly asserted that human ingenuity cannot concoct a cipher which human ingenuity cannot resolve...»</p>
        <small>Edgar Allan Poe</small>
      </blockquote>
      </br>
        <p>
            Based on an original idea from
           <a href="http://sebsauvage.net/paste/">sebsauvage.net</a>
       </p>

      </footer>
 

    <script src="/static/js/lzw.js"></script>
    <script src="/static/js/highlight.pack.js"></script>
    <script src="/static/js/jquery.elastic.source.js"></script>

    <!--
    <script src="/static/js/jquery.js"></script>
    <script src="/static/js/bootstrap-transition.js"></script>
    <script src="/static/js/bootstrap-alert.js"></script>
    <script src="/static/js/bootstrap-modal.js"></script>
    <script src="/static/js/bootstrap-dropdown.js"></script>
    <script src="/static/js/bootstrap-scrollspy.js"></script>
    <script src="/static/js/bootstrap-tab.js"></script>
    <script src="/static/js/bootstrap-tooltip.js"></script>
    <script src="/static/js/bootstrap-popover.js"></script>
    <script src="/static/js/bootstrap-button.js"></script>
    <script src="/static/js/bootstrap-collapse.js"></script>
    <script src="/static/js/bootstrap-carousel.js"></script>
    <script src="/static/js/bootstrap-typeahead.js"></script>
    -->

  </body>
</html>
