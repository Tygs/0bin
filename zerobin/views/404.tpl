<script type="text/javascript">
  zerobin.paste_not_found = true;
</script>

<p class="alert alert-error">
  <a class="close" data-dismiss="alert" href="#">×</a>
  <strong class="title">404 Error!</strong>
  <span class="message">
    Either this paste has expired or this page never existed.
  </span>
</p>

<p class="file-upload">
	<input type="button" class="btn btn-upload"  value="Upload File">
	<input type="file" class="hide-upload" id="file-upload" >
</p>

<form class="well" method="post" action="/paste/create">
<p class="paste-option">
<label for="expiration" >Expiration:</label>
  <select id="expiration" name="expiration">
    <option value="burn_after_reading">Burn after reading</option>
    <option selected value="1_day">1 day</option>
    <option value="1_month">1 month</option>
    <option value="1_year">1 year</option>
    <option value="never">Never</option>
  </select>
<button type="submit" class="btn btn-primary">Submit</button>
</p>
<p>
    <div class="progress progress-striped active">
      <div class="bar"></div>
    </div>
    <textarea rows="10"  style="width:100%;"
              class="input-xlarge"
              id="content" name="content"></textarea>
</p>
</form>


% rebase('base', settings=settings, pastes_count=pastes_count)
