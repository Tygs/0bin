<form class="form-group" action="." method="post">
	<div class="login-form">
		<form>
			<label>Password:</label>
			%if status == "error":
			<div class="alert alert-danger" role="alert alert-danger">
					{{message}}
			</div>
      %end
      <div class="input-group">
        <input type="password" id="password-field" placeholder="Enter your admin password here" name="password">
        <div class="input-group-append">
          <button type="submit" class="btn btn-secondary">Login</button>
        </div>
      </div>
		</form>
	</div>
</form>

% rebase('base', settings=settings, pastes_count=pastes_count)
