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

    <div class="d-flex justify-content-between">

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
          <button type="button" class="btn btn-danger" @click.prevent="handleCancelClone()">Cancel clone</button>
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
      <input type="text" class="paste-excerpt" name="paste-excerpt"
        placeholder="Optional paste title. This part is NOT encrypted: anything you type here will be visible by anyone"
        v-model="newPaste.title" maxlength="60">
    </div>

    <div class="d-flex justify-content-between" v-if="displayBottomToolBar">>

      <div>
        <label class="col-form-label">&nbsp;</label>
        <div class="file-upload">
          <button type="button" class="btn btn-danger" @click.prevent="handleCancelClone()">Cancel clone</button>
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
