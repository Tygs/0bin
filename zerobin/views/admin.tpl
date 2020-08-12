%if is_authenticated:

<form action="" method="delete">

    <div>
        <form>
            <div class="form-group">
                <label>Paste to delete</label>
                <input type="text" class="form-control" placeholder="Paste URL or ID">
            </div>
            <button type="submit" class="btn btn-black">Delete</button>
        </form>
    </div>


    %else:
    <form action="/login" method="post">

        <div class="login-form">
            <form>

                <label>Password</label>
                <input type="password" class="form-control" placeholder="Password">
                <button type="submit" class="btn btn-black">Login</button>
            </form>
        </div>

    </form>
    %end


    % rebase('base', settings=settings, pastes_count=pastes_count)
