<form class="well" method="post" action="/paste/create" @submit.prevent="encryptAndSendPaste()">
  <div class="d-flex justify-content-between">

    <div>
      <div class="file-upload" v-if="support.fileUpload">
        <label type="button" class="btn btn-primary upload-file"
          :disabled="isUploading">{% isUploading ? 'Uploading...': 'Upload file' %}
          <input type="file" class="hide-upload" id="file-upload" @change="handleUpload($event.target.files)">
        </label>
      </div>
    </div>

    <div class="form-group select-date paste-option">
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

  <div class="pre-wrapper">

    <div class="progress" v-show="isLoading">
      <div class="progress-bar progress-bar-striped" role="progressbar"></div>
    </div>

    <textarea rows="10" style="width:100%;" class="form-control" id="content" name="content" autofocus
      @keydown.ctrl.enter="encryptAndSendPaste()"></textarea>

    <div class="paste-options">
      <h6>Optional fields (those are <em>not</em> encrypted):</h6>

      <div class="input-group mb-3">
        <div class="input-group-prepend">
          <span class="input-group-text">Title</span>
        </div>
        <input type="text" class="form-control paste-excerpt" name="paste-excerpt"
          placeholder="Anything you type here will be visible by anyone, including search engines."
          v-model="newPaste.title" maxlength="60">
      </div>

      <div class="input-group mb-3">
        <div class="input-group-prepend">
          <span class="input-group-text tip" id="basic-addon1">Tip <svg xmlns="http://www.w3.org/2000/svg" width="18"
                height="18" viewBox="0 0 24 24">
                <path
                  d="M12 2c5.514 0 10 4.486 10 10s-4.486 10-10 10-10-4.486-10-10 4.486-10 10-10zm0-2c-6.627 0-12 5.373-12 12s5.373 12 12 12 12-5.373 12-12-5.373-12-12-12zm0 18v-1.511h-.5v1.511h-1v-1.511h-2.484l.25-1.489h.539c.442 0 .695-.425.695-.854v-4.444c0-.416-.242-.702-.683-.702h-.817v-1.5h2.5v-1.5h1v1.5h.5v-1.5h1v1.526c2.158.073 3.012.891 3.257 1.812.29 1.09-.429 2.005-1.046 2.228.75.192 1.789.746 1.789 2.026 0 1.742-1.344 2.908-4 2.908v1.5h-1zm-.5-5.503v2.503c1.984 0 3.344-.188 3.344-1.258 0-1.148-1.469-1.245-3.344-1.245zm0-.997c1.105 0 2.789-.078 2.789-1.25 0-1-1.039-1.25-2.789-1.25v2.5z"
                  fill="#eee" /></svg></span>
        </div>
        <input type="text" class="form-control paste-btc-tip-address" name="paste-btc-tip-address"
          placeholder="Put a BTC address to ask for a tip. Leave it empty to let us use our."
          v-model="newPaste.btcTipAddress" maxlength="50">
      </div>

    </div>

  </div>

  <div class="form-group select-date paste-option down" v-if="displayBottomToolBar">
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

</form>


% rebase("base", settings=settings, pastes_count=pastes_count)
