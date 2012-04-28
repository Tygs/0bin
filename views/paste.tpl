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

<div class="well">
<form action="/" method="get" accept-charset="utf-8">
<p>
  <a href="{{ paste.path }}">Raw</a>
  <span class="paste-option btn-group top">
      <button class="btn">New Paste</button>
      <button class="btn"><i class="icon-camera"></i>&nbsp;Clone</button>
  </span>
</p>

<p>
  <pre id="paste-content" class="prettyprint">
    <code>
      {{ paste.content }}
    </code>
  </pre>
</p>

<p class="paste-option btn-group bottom">
    <button class="btn">New Paste</button>
    <button class="btn"><i class="icon-camera"></i>&nbsp;Clone</button>
<p>

</form>
</div>
%rebase base
