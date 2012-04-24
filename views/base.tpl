<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>0bin - encrypted pastebin</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description"
          content="0bin is a client-side-encrypted
                   pastebin with a burn after reading feature">

    <!-- Le styles -->
    <link href="/static/css/bootstrap.css" rel="stylesheet">
    <link href="/static/css/style.css" rel="stylesheet">
    <link href="/static/css/bootstrap-responsive.css" rel="stylesheet">

    <!-- Le HTML5 shim, for IE6-8 support of HTML5 elements -->
    <!--[if lt IE 9]>
      <script src="http://html5shim.googlecode.com/svn/trunk/html5.js"></script>
    <![endif]-->

    <!-- Le fav and touch icons -->
    <link rel="shortcut icon" href="/static/ico/favicon.ico">
    <link rel="apple-touch-icon-precomposed" sizes="114x114" href="/static/ico/apple-touch-icon-114-precomposed.png">
    <link rel="apple-touch-icon-precomposed" sizes="72x72" href="/static/ico/apple-touch-icon-72-precomposed.png">
    <link rel="apple-touch-icon-precomposed" href="/static/ico/apple-touch-icon-57-precomposed.png">
  </head>

  <body>

    <div class="navbar navbar-fixed-top">
      <div class="navbar-inner">
        <div class="container-fluid">
          <a class="btn btn-navbar" data-toggle="collapse"
             data-target=".nav-collapse">
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
          </a>
          <a class="brand" href="#"><span>ø</span>bin<p>.net</p></a>
          <div class="nav-collapse">
            <ul class="nav">
              <li class="active"><a href="#">Home</a></li>
              <li><a href="#download">Download 0bin</a></li>
            </ul>
            <p class="navbar-text pull-right">Right stuff</p>
          </div><!--/.nav-collapse -->
        </div>
      </div>
    </div>

    <div class="container-fluid">
      <div class="row-fluid">
        <div class="span2">
          <div class="well sidebar-nav">
            <ul class="nav nav-list">
              <li class="nav-header">Mes précédents pastes</li>
              <li class="active"><a href="#">paste 1</a></li> 
              <li><a href="#">Paste 2</a></li>
            </ul>
          </div><!--/.well -->
        </div><!--/span-->
        <div class="span10">
          <div class="hero-unit">
            <h1>Bienvenue sur 0bin.net!</h1>
            <p>Vous copiez, ça encrypte, vous faites passer. Blablablabla...</p>
            <!-- 
            <p><a class="btn btn-primary btn-large">Learn more &raquo;</a></p> -->
            %include
          </div>
          <div class="row-fluid"> 
            <div class="span12">
                <form class="well">
                  <fieldset> 
                    <div class="control-group"> 
                      <label >New Paste:</label>
                        <textarea rows="30"  style="width:800px;" class="input-xlarge" id="paste"></textarea>
                      <label >Syntax Highlighting:</label>
                        <input type="text" class="input-xlarge" id="syntax">
                      <label >Paste expiration:</label>
                        <select id="expiration">
                          <option>Never</option>
                          <option>10 minutes</option>
                          <option></option>
                          <option>4</option>
                          <option>5</option>
                      </select>
                      <button type="submit" class="btn">Submit</button> 
                    </div>
                  </fieldset>
                </form>

            </div><!--/span-->
          </div><!--/row-->
        </div><!--/span-->
      </div><!--/row-->

      <hr>

      <footer>
        <p>
            Based on an original idea from
           <a href="http://sebsauvage.net/paste/">sebsauvage.net</a>
       </p>
      </footer>

    </div><!--/.fluid-container-->

    <!-- Le javascript
    ================================================== -->
    <!-- Placed at the end of the document so the pages load faster -->
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

  </body>
</html>
