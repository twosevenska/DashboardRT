<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="description" content="Dashboard RT - Logic Box">
    <meta name="author" content="Alexandre Vieira, André Martinez, Eduardo Pereira, Gloriya Gostyaeva, Gonçalo Barroso, Roberto Cunha">
    <link rel="icon" href="../../favicon.ico">

    <title>My Tickets</title>

    <link href="static/css/bootstrap.min.css" rel="stylesheet">
    <link href="static/css/bootstrap-theme.min.css" rel="stylesheet">
    <link href="static/css/dashboard.css" rel="stylesheet">
    <link href="static/css/sidebar.css" rel="stylesheet">

    <script src="static/js/ie-emulation-modes-warning.js"></script>
  </head>

  <body>

    <!--
    FIXED NAVBAR
    -->
    <nav class="navbar navbar-inverse navbar-fixed-top">
      <div class="navbar-collapse collapse">
        <ul class="nav navbar-nav navbar-left">
          <a class="navbar-brand" href="#">MAIN</a>
          <a class="navbar-brand" id="tickets" href="#">MY TICKETS</a>
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
        <button type="submit">create</button>
        </p></li>
            </ul>
        </li>
      </ul>

      </div>
    </nav>


    <!--
    SIDEBAR
    -->
    <nav class="main-menu">
      <div class="sidebar fa fa-home fa-2x">
          <div id="title" style="color: white"><h2>Dir-Inbox</h2></div>
            <div id="chatlist" class="mousescroll">
               <ul style="color: white">
                </ul>
              </div>
        </div>
    </nav>

    <!--
    TABLES
    -->
    <div class="jumbotron">
      <div class="container">
        <!-- Row for Titles -->
        <div class="row">
          <h2 class="col-md-3 stalled-margins">Stalled</h2>
          <h2 class="col-md-3 in-margins">In</h2>
          <h2 class="col-md-3 active-margins">Active</h2>
          <h2 class="col-md-3 done-margins">Done</h2>
        </div>
        <!-- Row for ticket tables -->
        <div class="row">
          <div class="stalled">
            <div id="chatlist" class="col-md-3 mousescroll">
              <ul>
              </ul>
            </div>
          </div>
          <div class="in">
            <div id="chatlist" class="col-md-3 mousescroll">
              <ul>
              </ul>
           </div>
         </div>
         <div class="active">
            <div id="chatlist" class="col-md-3 mousescroll">
              <ul>
              </ul>
            </div>
          </div>
          <div class="division">
            <div class="col-md-1">
              <img src="static/img/division_done.jpg" class="featurette-image img-responsive down" alt="me">
            </div>
          </div>

          <div class="done">
            <div id="chatlist" class="col-md-2 mousescroll">
              <ul>
              </ul>
            </div>
          </div> <!-- done -->
        </div><!-- row -->
      </div><!-- container -->
    </div><!-- jumbotron -->

<!-- ____________________________________________________________________________________ -->
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/2.1.4/jquery.min.js"></script>
    <script src="static/js/bootstrap.min.js"></script>
    <script src="static/js/holder.min.js"></script>
    <script src="static/js/ie10-viewport-bug-workaround.js"></script>
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
  </body>
</html>
