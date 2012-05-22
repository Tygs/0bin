<div class="well"> 

  <h1>FAQ</h1>
  
  %for i, entry in enumerate(settings.MENU):
    %if "mailto:" in entry[1]:
      <p>If a question does not appear here you can  
        <span title="{{ entry[1].replace('mailto:', '').replace('@', '__AT__') }}"
              class="email-link" >
              contact us
        </span>.
      </p>
    %end
  %end 

  <hr width="90%">

  <dl>

    <dt>What's the name of the captain?</dt>
    <dd>The name of the captain is Igloo !</dd>
    </br>
    <dt>What's the name of the captain?</dt>
    <dd>The name of the captain is Igloo !</dd>
    </br>
    <dt>What's the name of the captain?</dt>
    <dd>The name of the captain is Igloo !</dd>
  
  </dl>

</div>



%rebase base settings=settings, pastes_count=pastes_count
