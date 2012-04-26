<form class="well" method="post" action="/paste/create">

<p class="paste-option">
<label >Expiration:</label>
  <select id="expiration" name="expiration">
    <option value="burn_after_reading">Burn after reading</option>
    <option value="10_minutes">10 minutes</option>
    <option value="1_hour">1 hour</option>
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


<p class="paste-option">
<label >Expiration:</label>
  <select id="expiration" name="expiration">
    <option value="burn_after_reading">Burn after reading</option>
    <option value="10_minutes">10 minutes</option>
    <option value="1_hour">1 hour</option>
    <option selected value="1_day">1 day</option>
    <option value="1_month">1 month</option>
    <option value="never">Never</option>
  </select>
<button type="submit" class="btn btn-primary">Submit</button>
<p>

</ul>

</form>

%rebase base