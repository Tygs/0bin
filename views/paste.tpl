%if "burn_after_reading" in str(paste.expiration):
  <div class="alert">
  <strong>Warning!</strong>
  %if keep_alive:
      This paste will be deleted the next time it is read.
  %else:
      This paste has self-destructed. If you close this windows, there is not way
      to recover it.
  %end
  </div>
%end

<div class="well">

	<p class="paste-option btn-group">
	  <button class="btn">New Paste</button>
	  <button class="btn"><i class="icon-camera"></i>&nbsp;Clone</button>
	</p>

	<form action="/paste/clone" method="get" accept-charset="utf-8">
	</form>

	<p>

	  <pre id="paste-content" class="prettyprint">
	    <code>
	      {{ paste.content }}
	    </code>
	  </pre>

	</p>

	<p class="paste-option btn-group">
	  <button class="btn">New Paste</button>
	  <button class="btn"><i class="icon-camera"></i>&nbsp;Clone</button>
	<p>

	</form>

</div>

%rebase base