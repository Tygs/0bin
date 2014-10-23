<p class="file-upload">
	<input type="button" class="btn btn-upload"  value="Upload File">
	<input type="file" class="hide-upload" id="file-upload" >
</p>

<form class="well" method="post" action="/paste/create">
  <p class="paste-option">
  <label for="expiration" >Expiration:</label>
    <select id="expiration" name="expiration">
      <option value="burn_after_reading">Burn after reading</option>
      <option value="10_mins">10 minutes</option>
      <option value="30_mins">30 minutes</option>
      <option value="1_hour">1 hour</option>
      <option value="3_hours">3 hours</option>
      <option value="6_hours">6 hours</option>
      <option value="12_hours">12 hours</option>
      <option selected value="1_day">1 day</option>
      <option value="2_days">2 days</option>
      <option value="5_days">5 days</option>
      <option value="10_days">10 days</option>
      <option value="15_days">15 days</option>
      <option value="20_days">20 days</option>
      <option value="1_month">1 month</option>
      <option value="2_months">2 months</option>,
      <option value="6_months">6 months</option>
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


%rebase base settings=settings, pastes_count=pastes_count
