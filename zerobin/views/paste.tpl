%if "burn_after_reading" in str(paste.expiration):
  %if keep_alive:
    <p class="alert alert-info">
      <a class="close" data-dismiss="alert" href="#">×</a>
      <strong class="title">Ok!</strong>
      <span class="message">
        This paste will be deleted the next time it is read.
      </span>
    </p>
  %else:
    <p class="alert">
      <a class="close" data-dismiss="alert" href="#">×</a>
      <strong class="title">Warning!</strong>
      <span class="message">
        This paste has self-destructed. If you close this window,
        there is no way to recover it.
      </span>
    </p>
  %end
%end

<div class="well paste-form">
<form action="/" method="get" accept-charset="utf-8">
<p class="lnk-option">
  <a id="clip-button" href="#">Copy To Clipboard</a> |
  <a id="short-url" href="#">Get short url</a> |
  <a id="email-link" href="#">Email this</a>

  <span class="paste-option btn-group top">
      <button class="btn btn-clone"><i class="icon-camera"></i>&nbsp;Clone</button>
      <button class="btn">New Paste</button>
  </span>
</p>

<div class="progress progress-striped active">
  <div class="bar"></div>
</div>

%expiration = paste.humanized_expiration
%if expiration:
  <p id="expiration-tag">Expire {{ expiration }}</p>
%end

<p>
  <pre id="paste-content" class="prettyprint">
    <code>
      {{ paste.content }}
    </code>
  </pre>
</p>

<p class="paste-option btn-group bottom">
    <button class="btn btn-clone"><i class="icon-camera"></i>&nbsp;Clone</button>
    <button class="btn">New Paste</button>
</p>

</form>
</div>

<!-- For cloning -->
<div class="submit-form clone">
  <form class="well" method="post" action="/paste/create">
    <p class="paste-option">
    <label for="expiration" >Expiration:</label>
      <select id="expiration" name="expiration">
        <option value="burn_after_reading">Burn after reading</option>
        <option selected value="1_day">1 day</option>
        <option value="1_month">1 month</option>
        <option value="never">Never</option>
      </select>
      <button type="submit" class="btn btn-primary">Submit</button>
      <button class="btn btn-danger">Cancel clone</button>
    </p>

    <div>
        <div class="progress progress-striped active">
          <div class="bar"></div>
        </div>
        <textarea rows="10"  style="width:100%;"
                  class="input-xlarge"
                  id="content" name="content"></textarea>
    </div>
  </form>
</div>


%rebase base settings=settings, pastes_count=pastes_count
