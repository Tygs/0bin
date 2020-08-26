<!DOCTYPE html>
<html lang="en">

<head>
  <meta charset="utf-8">
  <title>0bin - encrypted pastebin</title>
  <meta name="viewport" content="width=device-width, initial-scale=1, minimum-scale=1, maximum-scale=1">
  <meta name="description" content="0bin is a client-side-encrypted alternative pastebin. You can store code/text/images online for a set period of time and share with the world. Featuring burn after reading, history, clipboard.">

  <link rel="icon" href="/static/img/favicon.ico" />
  <link rel="apple-touch-icon" href="/static/img/apple-touch-icon.png" />

  %if not settings.DEBUG:
  <link href="/static/css/style.min.css?{{ VERSION }}" rel="stylesheet" />
  %else:
  <link href="/static/css/prettify.css" rel="stylesheet" />
  <link href="/static/css/desert.css" rel="stylesheet" />
  <link href="/static/css/bootswatch.4.5.css" rel="stylesheet">
  <link href="/static/css/style.css?{{ VERSION }}" rel="stylesheet">
  %end

</head>

<body>

  <div id="app" :class="{ 'reader-mode-bg': readerMode}">

    <div :class="{'topnav': true, 'reader-mode': readerMode}" @mouseleave="openPreviousPastesMenu =false">
      <a class="brand" href="/"><span>ø</span>bin<em>.net</em></a>
      <span class="tagline">"A client side encrypted PasteBin"<br><span>All pastes are AES256 encrypted, we cannot know
          what you paste...</span>
      </span>

      <nav>
        <ul>
          <li class="reader-tools min" v-if="readerMode">
            <a href="#" @click.prevent="decreaseFontSize()">
              <svg height="30" width="30">
                <text x="10" y="20" fill="#eee">A</text>
              </svg>
            </a>
          </li>
          <li class="reader-tools max" v-if="readerMode">
            <a href="#" @click.prevent="increaseFontSize()">
              <svg height="30" width="30">
                <text x="10" y="20" fill="#eee">A</text>
              </svg>
            </a>
          </li>
          <li>
            <a class="reader-book" href="#" v-if="currentPaste.type === 'text'" @click.prevent="toggleReaderMode()">
              <svg width="1em" height="1em" viewBox="0 0 16 16" class="bi bi-book" fill="currentColor"
                xmlns="http://www.w3.org/2000/svg">
                <path fill-rule="evenodd"
                  d="M3.214 1.072C4.813.752 6.916.71 8.354 2.146A.5.5 0 0 1 8.5 2.5v11a.5.5 0 0 1-.854.354c-.843-.844-2.115-1.059-3.47-.92-1.344.14-2.66.617-3.452 1.013A.5.5 0 0 1 0 13.5v-11a.5.5 0 0 1 .276-.447L.5 2.5l-.224-.447.002-.001.004-.002.013-.006a5.017 5.017 0 0 1 .22-.103 12.958 12.958 0 0 1 2.7-.869zM1 2.82v9.908c.846-.343 1.944-.672 3.074-.788 1.143-.118 2.387-.023 3.426.56V2.718c-1.063-.929-2.631-.956-4.09-.664A11.958 11.958 0 0 0 1 2.82z" />
                <path fill-rule="evenodd"
                  d="M12.786 1.072C11.188.752 9.084.71 7.646 2.146A.5.5 0 0 0 7.5 2.5v11a.5.5 0 0 0 .854.354c.843-.844 2.115-1.059 3.47-.92 1.344.14 2.66.617 3.452 1.013A.5.5 0 0 0 16 13.5v-11a.5.5 0 0 0-.276-.447L15.5 2.5l.224-.447-.002-.001-.004-.002-.013-.006-.047-.023a12.582 12.582 0 0 0-.799-.34 12.96 12.96 0 0 0-2.073-.609zM15 2.82v9.908c-.846-.343-1.944-.672-3.074-.788-1.143-.118-2.387-.023-3.426.56V2.718c1.063-.929 2.631-.956 4.09-.664A11.956 11.956 0 0 1 15 2.82z" />
              </svg>
            </a>
          </li>
          <li class="submenu"><a href="#" @click.prevent="openPreviousPastesMenu = !openPreviousPastesMenu">Previous
              pastes <span class="caret"></span></a>

            <ul class="previous-pastes" id="topmenu" v-if="openPreviousPastesMenu">
              <li class="item" v-if="previousPastes.length === 0">
                <a href="#">No paste yet</a>
              </li>
              <li :class="{item: true, active: paste.isCurrent}" v-for="paste in previousPastes">
                <a :href="paste.link" @click="forceLoad(paste.link)">{% paste.displayDate %}</a>
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

      %if defined('paste') and paste.title:
      <h1 :class="{ 'reader-mode-title': readerMode}">{{ paste.title }}</h1>
      %end


      <p :class="'alert alert-' + msg.type" v-for="msg in messages">
        <a class="close" data-dismiss="alert" href="#" @click.prevent="$event.target.parentNode.remove()">×</a>
        <strong class="title" v-if="msg.title" v-html="msg.title"></strong>
        <span class="message" v-html="msg.content"></span>
        <a v-if="msg.action.message" href="#"
          @click.once.prevent="msg.action.callback($event)">{% msg.action.message %}</a>
      </p>

      <div id='main'>{{!base}}</div>
    </div>

    <footer class="footer">
      <ul>
        %for i, entry in enumerate(settings.MENU):
        <li>
          %if "mailto:" in entry[1]:
          <span :title='formatEmail(`{{ entry[1].replace("mailto:", "").replace("@", "__AT__") }}`)' class="email-link">
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

  %if not settings.DEBUG:
  <script src="/static/js/main.min.js?{{ VERSION }}"></script>
  %else:
  <script src="/static/js/vue.js"></script>
  <script src="/static/js/sjcl.js"></script>
  <script src="/static/js/behavior.js?{{ VERSION }}"></script>
  <script src="/static/js/prettify.min.js"></script>
  %end

  <script type="text/javascript">
    zerobin.max_size = {{ settings.MAX_SIZE }};
  </script>

  <p id="alert-template" class="alert-primary">
    <a class="close" data-dismiss="alert" href="#">×</a>
    <strong class="title"></strong>
    <span class="message"></span>
  </p>


</body>

</html>
