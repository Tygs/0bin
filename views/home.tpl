<form class="well" method="post" action="/paste/create">

<ul>
  <li>
    <span class="btn-group">
      <button class="btn">New Paste</button>
      <button class="btn"><i class="icon-camera"></i>&nbsp;Clone</button>
    </span>
  </li>

  <li>
      <span class="paste-option">
      <label for='expire_in'>Expiration:</label>
        <select id="expire_in" name="expire_in">
          <option value="burn_after_reading">Burn after reading</option>
          <option value="10_minutes">10 minutes</option>
          <option value="1_hour">1 hour</option>
          <option selected value="1_day">1 day</option>
          <option value="1_month">1 month</option>
          <option value="never">Never</option>
        </select>
      <button type="submit" class="btn btn-primary">Submit</button>
      <span>
  </li>
</ul>

<p>
    <textarea rows="10"  style="width:100%;"
              class="input-xlarge"
              id="content" name="content"></textarea>
</p>


<ul>
  <li>
    <span class="btn-group">
      <button class="btn">New Paste</button>
      <button class="btn"><i class="icon-camera"></i>&nbsp;Clone</button>
    </span>
  </li>

  <li>
      <span class="paste-option">
      <label >Expiration:</label>
        <select id="expire_in" name="expire_in">
          <option value="burn_after_reading">Burn after reading</option>
          <option value="10_minutes">10 minutes</option>
          <option value="1_hour">1 hour</option>
          <option selected value="1_day">1 day</option>
          <option value="1_month">1 month</option>
          <option value="never">Never</option>
        </select>
      <button type="submit" class="btn btn-primary">Submit</button>
      <span>
  </li>
</ul>

</form>

%rebase base