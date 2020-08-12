<form action="./delete/" method="post">
    %if status == "error":
    <div class="alert alert-danger" role="alert alert-danger">
        {{message}}
    </div>
    %end
    <div>
        <div class="form-group">
            <label>Paste to delete</label>
            <input name="paste" type="text" class="form-control" placeholder="Paste URL or ID">
        </div>
        <button type="submit" class="btn btn-black">Delete</button>

    </div>

</form>

<form action="./logout/" method="post">
    <div>
        <button type="submit" class="btn btn-black">Logout</button>
    </div>
</form>


% rebase('base', settings=settings, pastes_count=pastes_count)
