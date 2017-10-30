<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>0bin - encrypted pastebin</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description"
          content="0bin is a client-side-encrypted
                   pastebin featuring burn after reading, an history and
                   a clipboard">

    <link rel="shortcut icon" href="/favicon.ico">

    %if settings.COMPRESSED_STATIC_FILES:
      <link href="/static/css/style.min.css?{{ settings.VERSION }}"
            rel="stylesheet" />
    %else:
      <link href="/static/css/prettify.css" rel="stylesheet" />
      <link href="/static/css/bootstrap.css" rel="stylesheet">
      <link href="/static/css/style.css?{{ settings.VERSION }}"
            rel="stylesheet">
    %end

    <!-- Le HTML5 shim, for IE7-8 support of HTML5 elements -->
    <!--[if lt IE 9]>
      <script src="http://html5shim.googlecode.com/svn/trunk/html5.js"></script>
    <![endif]-->

    %if settings.COMPRESSED_STATIC_FILES:
      <script src="/static/js/main.min.js?{{ settings.VERSION }}"></script>
    %else:
      <script src="/static/js/jquery-1.7.2.min.js"></script>
      <script src="/static/js/sjcl.js"></script>
      <script src="/static/js/behavior.js?{{ settings.VERSION }}"></script>
    %end

    <script type="text/javascript">
      zerobin.max_size = {{ settings.MAX_SIZE }};
      %if settings.SHORTENER_API_KEY:
        zerobin.shortener_api_key = "{{ settings.SHORTENER_API_KEY }}";
      %end
    </script>

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

              %for i, entry in enumerate(settings.MENU):
                <li
                %if not i:
                  class="active"
                %end
                >
                  %if "mailto:" in entry[1]:
                    <span title="{{ entry[1].replace('mailto:', '').replace('@', '__AT__') }}"
                          class="email-link" >
                      {{ entry[0] }}
                    </span>
                  %else:
                    <a href="{{ entry[1] }}">{{ entry[0] }}</a>
                  %end

                </li>
              %end

            </ul>
            <p class="about pull-right">
              "A client side encrypted PasteBin"<br>
              <span>All pastes are AES256 encrypted, we cannot know what you paste...</span>
            </p>
          </div><!--/.nav-collapse -->
        </div>
      </div>
    </div>

    <noscript class="container noscript">
          <p>This pastebin uses client-side encryption. Therefore, it needs JavaScript enabled.</p>
          <p>It seems like your browser doesn't have JavaScript enable.</p>
          <p>Please enable JavaScript for this website or use a JavaScript-capable web browser.</p>
    </noscript>

    <div class="container" id="wrap-content">
      <div class="row">
        <div class="span2">
          <div class="well sidebar-nav">
            <ul class="nav nav-list previous-pastes">
              <li class="nav-header">Previous pastes</li>
              <li class="item local-storage">
                <em class="grey">
                  Your previous pastes will be saved in  your browser using
                  <a href="http://www.w3.org/TR/webstorage/">localStorage</a>.
                </em>
              </li>
              <li class="item no-local-storage">
                <em class="grey">
                  Sorry your browser does not support
                  <a href="http://www.w3.org/TR/webstorage/">LocalStorage</a>,
                  We cannot display your previous pastes.
                </em>
              </li>
            </ul>
          </div><!--/.well -->
        </div><!--/span-->

        <div id='main' class="span10">
           {{!base}}

        </div><!--/span-->

      </div><!--/row-->

      <hr>

      <footer>
       <blockquote>
        <p>“Few persons can be made to believe that it is not quite an easy thing to invent a method of secret writing which shall baffle investigation. Yet it may be roundly asserted that human ingenuity cannot concoct a cipher which human ingenuity cannot resolve...”</p>
        <small>Edgar Allan Poe</small>
      </blockquote>


      %if settings.DISPLAY_COUNTER:
        <h4 id="pixels-total" >
          <p>ø</p>
          <strong>{{ pastes_count }}</strong> <br/>pastes øbinned
        </h4>
      %end


      </br>
        <p class="greetings span12">
            Based on an original idea from
           <a href="http://sebsauvage.net/paste/">sebsauvage.net</a><br>
           <a href="http://sametmax.com">Sam &amp; Max</a>
       </p>
      </footer>

      %if settings.COMPRESSED_STATIC_FILES:
        <script src="/static/js/additional.min.js?{{ settings.VERSION }}"></script>
      %else:
        <script src="/static/js/jquery.elastic.source.js"></script>
        <script src="/static/js/lzw.js"></script>
        <script src="/static/js/prettify.min.js"></script>
        <script src="/static/js/ZeroClipboard.js"></script>
      %end

    <p id="alert-template">
      <a class="close" data-dismiss="alert" href="#">×</a>
      <strong class="title"></strong>
      <span class="message"></span>
    </p>
  </div><!--/wrap-content-->

  </body>

</html>
