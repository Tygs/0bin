



 

<form class="well" method="post" action="/paste/create">
  <div class="d-flex justify-content-between">
    
    <div>
      <label class="col-form-label">Upload text/img:</label>
      <div class="file-upload">
        <input type="button" class="btn btn-primary"  value="Upload File">
        <input type="file" class="hide-upload" id="file-upload" >
      </div>
    </div> 

    <div class="form-group select-date paste-option">
      <label class="col-form-label">Expiration:</label>
      <div class="input-group"> 
        <select id="expiration" name="expiration" class="custom-select">
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

  <div>
    <div class="progress-bar progress-bar-striped progress">
      <div class="bar"></div>
    </div>
    <textarea rows="10"  style="width:100%;"  
              class="form-control"
              id="content" name="content"></textarea>
  </div>

</form>


% rebase("base", settings=settings, pastes_count=pastes_count)
 