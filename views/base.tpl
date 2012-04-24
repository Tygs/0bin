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
        <div class="container">
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
              <li class="active"><a href="#">paste 1</a></li> 
              <li><a href="#">Paste 2</a></li>
            </ul>
          </div><!--/.well -->
        </div><!--/span--> 
          %include 

        <div class="span10">

          <form class="well">  

            <ul class="form-options">
              <li> 
                <div class="btn-group">
                  <button class="btn active">New Paste</button>
                  <button class="btn"><i class="icon-camera"></i>&nbsp;Clone</button> 
                </div> 
              </li>

              <li> 
                  <label >Syntax Highlighting:</label>
                    <select id="syntax">
                      <option>AutoDetect</option>
                      <option>PHP</option>
                      <option>Python</option> 
                  </select>
              </li>
              <li>
                  <label >Paste expiration:</label>
                    <select id="expiration">
                      <option>Never</option>
                      <option>Burn after reading</option>
                      <option>10 minutes</option>
                      <option>1 hour</option>
                      <option>1 day</option>
                      <option>1 month</option>
                  </select>
              </li>
              <li>
                  <button type="submit" class="btn btn-primary">Submit</button>  
              </li>
            </ul>

            <p> 
                <textarea rows="10"  style="width:100%;" class="input-xlarge" id="paste"></textarea>
            </p>


            <ul class="form-options">
              <li> 
                <div class="btn-group">
                  <button class="btn active">New Paste</button>
                  <button class="btn"><i class="icon-camera"></i>&nbsp;Clone</button> 
                </div> 
              </li>

              <li> 
                  <label >Syntax Highlighting:</label>
                    <select id="syntax">
                      <option>AutoDetect</option>
                      <option>PHP</option>
                      <option>Python</option> 
                  </select>
              </li>
              <li>
                  <label >Paste expiration:</label>
                    <select id="expiration">
                      <option>Never</option>
                      <option>Burn after reading</option>
                      <option>10 minutes</option>
                      <option>1 hour</option>
                      <option>1 day</option>
                      <option>1 month</option>
                  </select>
              </li>
              <li>
                  <button type="submit" class="btn btn-primary">Submit</button>  
              </li>
            </ul>

          </form>  

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
