<form action="." method="post">
    <div class="login-form">
        <form>
            <label>Password</label>
            %if status == "error":
            <div class="alert alert-danger" role="alert alert-danger">
                {{message}}
            </div>
            %end
            <input type="password" class="form-control" placeholder="Password" name="password">
            <button type="submit" class="btn btn-black">Login</button>
        </form>
    </div>

</form>


% rebase('base', settings=settings, pastes_count=pastes_count)
