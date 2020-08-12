%if "burn_after_reading" in str(paste.expiration):
%if keep_alive:
<p class="alert alert-info">
  <a class="close" data-dismiss="alert" href="#" @click.prevent="$event.target.parentNode.remove()">×</a>
  <strong class="title">Ok!</strong>
  <span class="message">
    This paste will be deleted the next time it is read.
  </span>
</p>
%else:
<p class="alert">
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
 
      <div class="btn-group" role="group" >
        <button v-if="support.clipboard" @click.prevent="copyToClipboard()" type="button" id="clip-button" class="btn btn-secondary">Copy To Clipboard</button>
        <button type="button" id="email-link" class="btn btn-secondary"  @click="handleSendByEmail($event)>Email this</button>
      </div>

      <div> 
        <span class="paste-option btn-group">
            <button class="btn btn-clone btn-secondary" @click.prevent="handleClone()">Clone</button>
           
        <button class="btn  btn-secondar" v-if="downloadLink.url">
          <a :href="downloadLink.url" :download="downloadLink.name"> Download</a>
        </button>

           <button class="btn btn-secondary">New Paste</button>
        </span>
      </div> 
      
    </div> 
 
    <div class="progress-container">
      <div class="progress progress-bar progress-bar-striped active"  v-show="isLoading">
        <div class="bar"></div>
      </div>
    </div>

    %expiration = paste.humanized_expiration
    %if expiration:
      <span id="expiration-tag">Expire {{ expiration }}</span>
    %end

    <pre id="paste-content" class="prettyprint">
      <code>
        {{ paste.content }}
      </code>
    </pre>

    <div class="d-flex justify-content-between down">
      <div v-if="currentPaste.ownerKey">  
        <button class="btn btn-clone btn-secondary" @click="handleDeletePaste()">Delete Paste</button> 
      </div> 
      <div> 
        <span class="paste-option btn-group">
            <button class="btn btn-clone btn-secondary" @click.prevent="handleClone()">Clone</button>
           
        <button class="btn  btn-secondar" v-if="downloadLink.url">
          <a :href="downloadLink.url" :download="downloadLink.name"> Download</a>
        </button>

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
        <label class="col-form-label">&nbsp;</label>
        <div class="file-upload"> 
          <button type="button" class="btn btn-danger" @click.prevent="handleCancelClone()">Cancel clone</button> 
        </div>
      </div> 

      <div class="form-group select-date-clone paste-option">
        <label class="col-form-label" >Expiration:</label>
        <div class="input-group"> 
          <select id="expiration" name="expiration" class="custom-select" v-model="newPaste.expiration">
            <option value="burn_after_reading">Burn after reading</option>
            <option selected value="1_day">1 day</option>
            <option value="1_month">1 month</option>
            <option value="never">Never</option>
          </select>
          <div class="input-group-append"> 
            <button type="submit" class="btn btn-primary">Submit</button>
          </div>
        </div>
      </div>
      
    </div> 

    <div class="progress-container progress-clone" >
      <div class="progress progress-bar progress-bar-striped active"  v-show="isLoading">
        <div class="bar"></div>
      </div>
    </div>

    <div> 
        <textarea rows="10"  style="width:100%;"
                  class=" form-control" @keydown.prevent.ctrl.enter="encryptAndSendPaste()"
                  id="content" name="content"></textarea>
    </div>

    <div class="d-flex justify-content-between" v-if="displayBottomToolBar">>
    
      <div>
        <label class="col-form-label">&nbsp;</label>
        <div class="file-upload"> 
          <button type="button" class="btn btn-danger" @click.prevent="handleCancelClone()">Cancel clone</button> 
        </div>
      </div> 

      <div class="form-group select-date-clone paste-option">
        <label class="col-form-label" >Expiration:</label>
        <div class="input-group"> 
          <select id="expiration" name="expiration" class="custom-select" v-model="newPaste.expiration">
            <option value="burn_after_reading">Burn after reading</option>
            <option selected value="1_day">1 day</option>
            <option value="1_month">1 month</option>
            <option value="never">Never</option>
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
