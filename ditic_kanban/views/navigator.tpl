% rebase('skin')

<nav class="navbar navbar-inverse navbar-fixed-top">
  <div class="navbar-collapse collapse">
    <ul class="nav navbar-nav navbar-left">
      <a class="navbar-brand" href="/">Board</a>
      <a class="navbar-brand" id="tickets" href="/index">My Tickets</a>
    </ul>
    <!-- ADMIN -->
      <ul class="nav navbar-nav navbar-right">
        <li class="dropdown">
          <a href="#" class="dropdown-toggle m_right" data-toggle="dropdown" role="button" aria-haspopup="true" aria-expanded="false">Admin<span class="caret"></span></a>
          <ul class="dropdown-menu">
            <li><a href="#">Profile</a></li>
            <li><a href="#">Preferences</a></li>
            <li><a href="#" onClick="onLogoutClick()">Logout</a></li>
            <li role="separator" class="divider"></li>
            <li class="dropdown-header">Nav header</li>
            <li><a href="#">Separated link</a></li>
            <li><a href="#">One more separated link</a></li>
          </ul>
        </li>
      </ul>
      <!-- SEARCH -->
      <form class="navbar-form navbar-right">
        <input type="text" class="form-control" placeholder="Search...">
        <button type="submit">Search</button>
      </form>
      <!-- NEW TICKET -->
      <ul class="nav navbar-nav navbar-right">
<li class="dropdown">
  <a href="#" class="dropdown-toggle m_right" data-toggle="dropdown" role="button" aria-haspopup="true" aria-expanded="false">New ticket <span class="caret"></span></a>
  <ul class="dropdown-menu">
    <li><p>
    <b>Create quick ticket:</b>
    </br>
      Subject: <input id="sub" type="text" placeholder="Subject">
      Text: <input id="text" type="text" placeholder="Text here">
    <ul><li><a href="#">Advanced Ticket Creation</a></li></ul>
    <button type="submit" onclick="create()">create</button>
    </p></li>
        </ul>
    </li>
  </ul>

  </div>
  <script>
    function onLogoutClick() {
            $.ajax({
                type: "DELETE",
                url: "/auth",
                data: "{}",
                contentType: "application/json",
                complete: function (data, textStatus) {
                    console.log("complete.statusCode=" + data.statusCode);
                },
                success: function (data) {
                    window.location.href = "/login";
                }
            });
        }
  </script>
</nav>