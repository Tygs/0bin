%if "burn_after_reading" in str(paste.expiration):
%if keep_alive:
<p class="alert alert-dismissible alert-primary">
  <a class="close" data-dismiss="alert" href="#" @click.prevent="$event.target.parentNode.remove()">×</a>
  <strong class="title">Ok!</strong>
  <span class="message">
    This paste will be deleted the next time it is read.
  </span>
</p>
%else:
<p class="alert alert-warning alert-dismissible">
  <a class="close" data-dismiss="alert" href="#" @click.prevent="$event.target.parentNode.remove()">×</a>
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

    <div :class="{'d-flex': true, 'justify-content-between': true , 'reader-mode-tools': readerMode}" >

      <div class="btn-group" role="group">
        <button v-if="support.clipboard && currentPaste.type === 'text'" @click.prevent="copyToClipboard()"
          type="button" id="clip-button" class="btn btn-secondary">Copy to clipboard</button>
        <button type="button" id="email-link" class="btn btn-secondary" @click="handleSendByEmail($event)">Email
          this</button>
      </div>

      <div>
        <span class="paste-option btn-group">
          <button class="btn btn-clone btn-secondary" @click.prevent="handleClone()">Clone</button>
          <a class="btn btn-secondary download-link" :href="currentPaste.downloadLink.url"
            :download="currentPaste.downloadLink.name">Download</a>
          <button class="btn btn-secondary">New Paste</button>
        </span>
      </div>

    </div>

    <div class="progress-container">
      <div class="progress  active" v-show="isLoading">
        <div class="progress-bar progress-bar-striped" role="progressbar"></div>
      </div>
    </div>

    %expiration = paste.humanized_expiration
    %if expiration:
    <span id="expiration-tag">Expire {{ expiration }}</span>
    %end

    <pre id="paste-content" class="prettyprint" v-if="!readerMode">
        <code>
          {{ paste.content }}
        </code>
    </pre>

    <div>
      <div id="readable-paste-content" v-if="readerMode">
        {% currentPaste.content %}
      </div>
    </div>

    <div class="paste-options-res">
      <div class="btn-group">
        <span class="input-group-text">Tip it with<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24"><path d="M12 2c5.514 0 10 4.486 10 10s-4.486 10-10 10-10-4.486-10-10 4.486-10 10-10zm0-2c-6.627 0-12 5.373-12 12s5.373 12 12 12 12-5.373 12-12-5.373-12-12-12zm0 18v-1.511h-.5v1.511h-1v-1.511h-2.484l.25-1.489h.539c.442 0 .695-.425.695-.854v-4.444c0-.416-.242-.702-.683-.702h-.817v-1.5h2.5v-1.5h1v1.5h.5v-1.5h1v1.526c2.158.073 3.012.891 3.257 1.812.29 1.09-.429 2.005-1.046 2.228.75.192 1.789.746 1.789 2.026 0 1.742-1.344 2.908-4 2.908v1.5h-1zm-.5-5.503v2.503c1.984 0 3.344-.188 3.344-1.258 0-1.148-1.469-1.245-3.344-1.245zm0-.997c1.105 0 2.789-.078 2.789-1.25 0-1-1.039-1.25-2.789-1.25v2.5z" fill="#eee"/></svg></span>
        <a class="btn btn-primary btc-tip-address"
            href="bitcoin:{{ paste.btc_tip_address or  settings.DEFAULT_BTC_TIP_ADDRESS }}">
            {{ paste.btc_tip_address or settings.DEFAULT_BTC_TIP_ADDRESS}}
        </a>
        <button class="btn btn-secondary">copy</button>
      </div>
    </div>


    <div class="d-flex justify-content-between down">
      <div v-if="currentPaste.ownerKey">
        <button class="btn btn-clone btn-secondary" @click="handleDeletePaste()">Delete Paste</button>
      </div>
      <div>
        <span class="paste-option btn-group">
          <button class="btn btn-clone btn-secondary" @click.prevent="handleClone()">Clone</button>

          <a class="btn btn-secondary download-link" :href="currentPaste.downloadLink.url"
            :download="currentPaste.downloadLink.name"> Download</a>

          <button class="btn btn-secondary">New Paste</button>
        </span>
      </div>
    </div>

  </form>
</div>

<!-- For cloning -->
<div class="submit-form clone">
  <form class="well" method="post" action="/paste/create" @submit.prevent="encryptAndSendPaste()">

    <div class="d-flex justify-content-between">

      <div>
        <div class="file-upload">
          <button type="button" class="btn btn-info" @click.prevent="handleCancelClone()">Cancel clone</button>
        </div>
      </div>

      <div class="form-group select-date-clone paste-option">
        <div class="input-group">
          <select id="expiration" name="expiration" class="custom-select" v-model="newPaste.expiration">
            <option value="burn_after_reading">Burn after reading</option>
            <option selected value="1_day">Expire in 1 day</option>
            <option value="1_month">Expire in 1 month</option>
            <option value="never">Never expire</option>
          </select>
          <div class="input-group-append">
            <button type="submit" class="btn btn-primary">Submit</button>
          </div>
        </div>
      </div>

    </div>

    <div class="progress-container progress-clone">
      <div class="progress active" v-show="isLoading">
        <div class="progress-bar progress-bar-striped" role="progressbar"></div>
      </div>
    </div>

    <div>
      <textarea rows="10" style="width:100%;" class=" form-control" @keydown.ctrl.enter="encryptAndSendPaste()"
        id="content" name="content"></textarea>

      <div class="paste-options">
        <h6>Paste Options (these options are optionals)</h6>

        <div class="input-group mb-3">
          <div class="input-group-prepend">
            <span class="input-group-text">Title</span>
          </div>
          <input type="text" class="form-control paste-excerpt" name="paste-excerpt"
            placeholder="Optional paste title. This part is NOT encrypted: anything you type here will be visible by anyone"
            v-model="newPaste.title" maxlength="60">
        </div>

        <div class="input-group mb-3">
          <div class="input-group-prepend">
            <span class="input-group-text" id="basic-addon1">BTC tip</span>
          </div>
          <input type="text" class="form-control paste-btc-tip-address" name="paste-btc-tip-address"
            placeholder="Put a BTC address to ask for a tip. Leave it empty to let us use our."
            v-model="newPaste.btcTipAddress" maxlength="50">
        </div>

      </div>

    </div>

    <div class="d-flex justify-content-between" v-if="displayBottomToolBar">>

      <div>
        <label class="col-form-label">&nbsp;</label>
        <div class="file-upload">
          <button type="button" class="btn btn-info" @click.prevent="handleCancelClone()">Cancel clone</button>
        </div>
      </div>

      <div class="form-group select-date-clone paste-option">
        <div class="input-group">
          <select id="expiration" name="expiration" class="custom-select" v-model="newPaste.expiration">
            <option value="burn_after_reading">Burn after reading</option>
            <option selected value="1_day">Expire in 1 day</option>
            <option value="1_month">Expire in 1 month</option>
            <option value="never">Never expire</option>
          </select>
          <div class="input-group-append">
            <button type="submit" class="btn btn-primary">Submit</button>
          </div>
        </div>
      </div>

    </div>
  </form>
</div>


% rebase("base", settings=settings, pastes_count=pastes_count)
