%if "burn_after_reading" in str(paste.expiration):
  %if keep_alive:
   <div class="alert alert-info">
      <strong>Ok!</strong>
      This paste will be deleted the next time it is read.
    </div>
  %else:
   <div class="alert">
   <strong>Warning!</strong>
      This paste has self-destructed. If you close this windows, there is not way
      to recover it.
   </div>
  %end
%end

<div id="copy-success" class="alert alert-success">
  The paste is now in your clipboad
</div>

<div id="short-url-success" class="alert alert-success"></div>

<div class="well paste-form">
<form action="/" method="get" accept-charset="utf-8">
<p class="lnk-option"> 
	  <a id="clip-button">Copy To Clipboard</a>
	  |
	  <a id="short-url" href=""
	     target="_blank">Get short url</a> 
  <span class="paste-option btn-group top">
      <button class="btn btn-clone"><i class="icon-camera"></i>&nbsp;Clone</button>
      <button class="btn">New Paste</button>
  </span>
</p>

<div class="progress progress-striped active">
  <div class="bar"></div>
</div>

<p>
  <pre id="paste-content"  class="prettyprint linenums">
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
<span class="submit-form">
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
	<p>
	<p>
	    <textarea rows="10"  style="width:100%;"
	              class="input-xlarge"
	              id="content" name="content"></textarea>
	</p>
	</form>
</span>


%rebase base
