<div class="alert alert-error max-size-reached">
  <a class="close" data-dismiss="alert" href="#">×</a>
  <strong>Warning!</strong><br>
  Your file is <strong class="file-size"></strong>KB You have reached the maximum size limit of {{ max_size_kb }}KB.
</div>

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
    <option value="never">Never</option>
  </select>
<button type="submit" class="btn btn-primary">Submit</button>
<p>
<p>
    <textarea rows="10"  style="width:100%;"
              class="input-xlarge"
              id="content" name="content"></textarea>
</p>
<div class="progress progress-striped active">
  <div class="bar"></div>
</div>
</form>


%rebase base max_size=max_size
