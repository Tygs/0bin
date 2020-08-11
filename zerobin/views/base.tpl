<!DOCTYPE html>
<html lang="en">

<head>
  <meta charset="utf-8">
  <title>0bin - encrypted pastebin</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="0bin is a client-side-encrypted
                   pastebin featuring burn after reading, history, and
                   a clipboard">

  <link rel="shortcut icon" href="/favicon.ico">

  %if settings.COMPRESSED_STATIC_FILES:
  <link href="/static/css/style.min.css?{{ VERSION }}" rel="stylesheet" />
  %else:
  <link href="/static/css/prettify.css" rel="stylesheet" />
  <link href="/static/css/bootstrap.css" rel="stylesheet">
  <link href="/static/css/style.css?{{ VERSION }}" rel="stylesheet">
  %end

  <!-- Le HTML5 shim, for IE7-8 support of HTML5 elements -->
  <!--[if lt IE 9]>
      <script src="http://html5shim.googlecode.com/svn/trunk/html5.js"></script>
    <![endif]-->

</head>

<body>

  <div class="navbar navbar-fixed-top" id="menu-top">
    <div class="navbar-inner">
      <div class="container">
        <a class="btn btn-navbar" data-toggle="collapse" data-target=".nav-collapse">
          <span class="icon-bar"></span>
          <span class="icon-bar"></span>
          <span class="icon-bar"></span>
        </a>
        <a class="brand" href="/"><span>ø</span>bin<em>.net</em></a>
        <div class="nav-collapse">
          <ul class="nav">

            %for i, entry in enumerate(settings.MENU):
            <li>
              %if "mailto:" in entry[1]:
              <a :href="formatEmail('{{ entry[1].replace('mailto:', '').replace('@', '__AT__') }}')" class="email-link">
                {{ entry[0] }}
              </a>
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
        </div>
        <!--/.nav-collapse -->
      </div>
    </div>
  </div>

  <noscript class="noscript">

    <div class="container jumbotron">
      <h1 class="display-4">This site requires Javascript</h1>
      <p class="lead">This pastebin uses client-side encryption, and therefore, it needs JavaScript to work.</p>
      <p>It seems like your browser doesn't have JavaScript enabled.</p>
      <p>Please enable JavaScript for this website or use a JavaScript-capable web browser.</p>
    </div>

  </noscript>

  <div class="container app" id="wrap-content" v-cloak>
    <div class="row">
      <div class="span2">
        <div class="well sidebar-nav">
          <ul class="nav nav-list previous-pastes">
            <li class="nav-header">Previous pastes</li>
            <li class="item local-storage" v-if="previousPastes.length === 0">
              <em class="grey">
                Your previous pastes will be saved in your browser using
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
            <li :class="{item: true, active: paste.isCurrent}" v-for="paste in previousPastes">
              <a :href="paste.link" @click="forceLoadPaste(paste.link)">
                {% paste.prefix %}{% paste.displayDate %}
              </a>
            </li>
          </ul>
        </div>
        <!--/.well -->
      </div>
      <!--/span-->

      <div id='main' class="span10">


        <p :class="'alert alert-' + msg.type" v-for="msg in messages">
          <a class="close" data-dismiss="alert" href="#" @click.prevent="$event.target.parentNode.remove()">×</a>
          <strong class="title" v-if="msg.title" v-html="msg.title"></strong>
          <span class="message" v-html="msg.content"></span>
          <a v-if="msg.action.message" href="#"
            @click.once.prevent="msg.action.callback($event)">{% msg.action.message %}</a>
        </p>

        {{!base}}

      </div>
      <!--/span-->

    </div>
    <!--/row-->

    <hr>

    <footer>
      <blockquote>
        <p>“Few persons can be made to believe that it is not quite an easy thing to invent a method of secret writing
          which shall baffle investigation. Yet it may be roundly asserted that human ingenuity cannot concoct a cipher
          which human ingenuity cannot resolve...”</p>
        <small>Edgar Allan Poe</small>
      </blockquote>


      %if settings.DISPLAY_COUNTER:
      <h4 id="pixels-total">
        <p>ø</p>
        <strong>{{ pastes_count }}</strong> <br />pastes øbinned
      </h4>
      %end


      <br>
      <p class="greetings span12">
        Based on an original idea from
        <a href="http://sebsauvage.net/paste/">sebsauvage.net</a><br>
        <a href="http://sametmax.com">Sam &amp; Max</a>
      </p>
    </footer>

  </div>
  <!--/wrap-content-->

  <script src="/static/js/vue.js"></script>
  %if settings.COMPRESSED_STATIC_FILES:
  <script src="/static/js/main.min.js?{{ VERSION }}"></script>
  %else:
  <script src="/static/js/sjcl.js"></script>
  <script src="/static/js/behavior.js?{{ VERSION }}"></script>
  %end

  <script type="text/javascript">
    zerobin.max_size = {{ settings.MAX_SIZE }};

  </script>

  %if settings.COMPRESSED_STATIC_FILES:
  <script src="/static/js/additional.min.js?{{ VERSION }}"></script>
  %else:

  <script src="/static/js/lzw.js"></script>
  <script src="/static/js/prettify.min.js"></script>
  %end

</body>

</html>
