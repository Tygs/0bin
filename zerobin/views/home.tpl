<p class="file-upload" v-if="support.fileUpload">
  <input type="button" class="btn btn-upload" value="Upload File" :value="isUploading ? 'Uploading...': 'Upload file'"
    :disabled="isUploading">
  <input type="file" class="hide-upload" id="file-upload" @change="handleUpload($event.target.files)">
</p>

<form class="well" method="post" action="/paste/create">
  <p class="paste-option">
    <label for="expiration">Expiration:</label>
    <select id="expiration" name="expiration" v-model="newPaste.expiration">
      <option value="burn_after_reading">Burn after reading</option>
      <option selected value="1_day">1 day</option>
      <option value="1_month">1 month</option>
      <option value="never">Never</option>
    </select>
    <button type="submit" class="btn btn-primary" @click="encryptAndSendPaste($event)">Submit</button>
  </p>
  <p>
    <div class="progress progress-striped active" v-show="isLoading">
      <div class="bar"></div>
    </div>
    <textarea rows="10" style="width:100%" class="input-xlarge" id="content" name="content" autofocus
      v-on:keydown.ctrl.enter="encryptAndSendPaste($event)"></textarea>
  </p>

  <p class="paste-option down" v-if="displayBottomToolBar">
    <label for="expiration">Expiration:</label>
    <select id="expiration" name="expiration" v-model="newPaste.expiration">
      <option value="burn_after_reading">Burn after reading</option>
      <option selected value="1_day">1 day</option>
      <option value="1_month">1 month</option>
      <option value="never">Never</option>
    </select>
    <button type="submit" class="btn btn-primary" @click="encryptAndSendPaste($event)">Submit</button>
  </p>
</form>


% rebase("base", settings=settings, pastes_count=pastes_count)
