<!DOCTYPE html>
<html lang="en">

<head>
  <meta charset="utf-8">
  <title>0bin - encrypted pastebin</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="0bin is a client-side-encrypted
                   pastebin featuring burn after reading, history, and
                   a clipboard">

  <link rel="shortcut icon" href="/favicon.ico">

  %if settings.COMPRESSED_STATIC_FILES:
  <link href="/static/css/style.min.css?{{ VERSION }}" rel="stylesheet" />
  %else:
  <link href="/static/css/prettify.css" rel="stylesheet" />
  <link href="/static/css/desert.css" rel="stylesheet" />
  <link href="/static/css/bootswatch.4.5.css" rel="stylesheet">
  <link href="/static/css/style.css?{{ VERSION }}" rel="stylesheet">
  %end

</head>

<body>

  <div id="app">

    <div class="topnav">
      <a class="brand" href="/"><span>ø</span>bin<em>.net</em></a>
      <span class="tagline">"A client side encrypted PasteBin"<br><span>All pastes are AES256 encrypted, we cannot know
          what you paste...</span>
      </span>

      <nav>
        <ul>
          <li class="submenu"><a href="#" @click.prevent="openPreviousPastesMenu = !openPreviousPastesMenu">Previous
              pastes +</a>
            <ul class="previous-pastes" id="topmenu" v-if="openPreviousPastesMenu"
              @mouseleave="openPreviousPastesMenu =false">
              <li class="item active" v-if="previousPastes.length === 0">
                <a href="#">No paste yet...</a>
              </li>
              <li class="item active" v-for="paste in previousPastes">
                <a :href="paste.link" @click="forceLoad(paste.link)">{% paste.displayDate %}.</a>
              </li>
            </ul>
          </li>
        </ul>
      </nav>

    </div>

    <noscript class="container noscript">
      <p>This pastebin uses client-side encryption. Therefore, it needs JavaScript enabled.</p>
      <p>It seems like your browser doesn't have JavaScript enable.</p>
      <p>Please enable JavaScript for this website or use a JavaScript-capable web browser.</p>
    </noscript>

    <div class="container-md" id="wrap-content">
      <div id='main'>{{!base}}</div>
    </div>

    <footer class="footer">
      <ul>
        %for i, entry in enumerate(settings.MENU):
          <li>
            %if "mailto:" in entry[1]:
              <span :title='formatEmail(`{{ entry[1].replace("mailto:", "").replace("@", "__AT__") }}`)'
                    class="email-link" >
                {{ entry[0] }}
              </span>
            %else:
              <a href="{{ entry[1] }}">{{ entry[0] }}</a>
            %end
          </li>
        %end
      </ul>
      
      %if settings.DISPLAY_COUNTER:
      <strong>{{ pastes_count }}</strong> pastes øbinned
      %end
    </footer>

  </div>


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
  <script src="/static/js/additional.min.js?{{ settings.VERSION }}"></script>
  %else:
  <script src="/static/js/lzw.js"></script>
  <script src="/static/js/prettify.min.js"></script> 
  %end

  <p id="alert-template" class="alert-primary">
    <a class="close" data-dismiss="alert" href="#">×</a>
    <strong class="title"></strong>
    <span class="message"></span>
  </p>


</body>

</html>
