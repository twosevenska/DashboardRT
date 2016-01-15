<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="description" content="Dashboard RT - Logic Box">
    <meta name="author" content="Alexandre Vieira, André Martinez, Eduardo Pereira, Gloriya Gostyaeva, Gonçalo Barroso, Roberto Cunha">

    <title>User</title>

    <link href="static/res/css/bootstrap.min.css" rel="stylesheet">
    <link href="static/res/css/bootstrap-theme.min.css" rel="stylesheet">
    <link href="static/res/css/dashboard.css" rel="stylesheet">
    <link href="static/res/css/sidebar.css" rel="stylesheet">

    <script src="static/res/js/ie-emulation-modes-warning.js"></script>
  </head>

  <body>
  <img class="img-responsive" src="/static/res/img/background.png" style="position:fixed;top:0px;left:0px;width: 100%;z-index:-1;" />
    <!-- 
    FIXED NAVBAR
    -->
    <nav class="navbar navbar-inverse navbar-fixed-top">
  <div class="navbar-collapse collapse">
    <ul class="nav navbar-nav navbar-left">
      <a class="navbar-brand" href="/board">Board</a>
      <a class="navbar-brand" href="/income">Income</a>
      <a class="navbar-brand" id="tickets" href="/detail">My Tickets</a>
    </ul>
    <!-- ADMIN -->
      <ul class="nav navbar-nav navbar-right">
        <li class="dropdown">
          <a href="" class="dropdown-toggle m_right" data-toggle="dropdown" role="button" aria-haspopup="true" aria-expanded="false">{{username}}<span class="caret"></span></a>
          <ul class="dropdown-menu">
            <li align="center"><a href="" onclick="onProfileClick()">Profile</a></li>
            <li align="center"><a href="#">Preferences</a></li>
            <li align="center"><a href="" onClick="onLogoutClick()">Logout</a></li>
          </ul>
        </li>
      </ul>
      <!-- SEARCH -->
      <ul class="navbar-form navbar-right">
        <input id="search" type="text" class="form-control" placeholder="Search..." />
        <button id="sBtn" type="button" class="btn btn-primary" onclick="clickSearch()">Search</button>
      </ul>

      <!-- NEW TICKET -->
      <ul class="nav navbar-nav navbar-right">
        <li class="dropdown">
            <a href="#" class="dropdown-toggle m_right" data-toggle="dropdown" role="button" aria-haspopup="true" aria-expanded="false">New ticket<span class="caret"></span></a>
            <ul class="dropdown-menu">
        <li><p align="center" style="color:black;">
            <b>Create quick ticket:</b>
            </br>
            Subject: <input id="sub" type="text" placeholder="Subject">
            Text: <input id="text" type="text" placeholder="Text here">
        </p></li>

        <li role="separator" class="divider"></li>
        <li><p align="center" style="color:black;">
            <button type="button" class="btn btn-primary" onclick="onCreateClick()">create</button>
        </p></li>
        </ul>
    </li>
  </ul>

  </div>

</nav>




    <!-- 
    TABLES 
    -->
    <div class="jumbotron">
      <div class="container">
        <!-- Row for Titles -->
        <div class="row col-md-6">
          <h1>User Profile</h1>
          <h2>Edit your profile</h2>
        </div>
      </div><!-- close container -->

      <div class="container">
        <!-- Row for ticket tables -->
          <div class="row col-md-5" style="margin-top:30px">

            <p>id:</p><input type="text" class="form-control" placeholder="">
            <p>Name:</p><input type="text" class="form-control" placeholder="">
            <p>Description:</p><input type="text" class="form-control" placeholder="">
            <p>CorrespondAddress:</p><input type="text" class="form-control" placeholder="">
            <p>InitialPriority:</p><input type="text" class="form-control" placeholder="">
            <p>FinalPriority:</p><input type="text" class="form-control" placeholder="">
            <p>DefaultDueIn:</p><input type="text" class="form-control" placeholder="">
          </div><!-- row -->
          <div class="col-md-2">
            <!-- empty div to separate the columns -->
          </div>
        </div><!-- close container -->
        <div class="container">
          <br> 
          <p><button type="submit">Edit</button></p>
        </div>
      </div><!-- jumbotron -->



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
function onCreateClick(){
        data = {
                    subject: document.getElementById('sub').value,
                    text: document.getElementById('text').value
                };
        $.ajax({
                type: "POST",
                url: "/ticket",
                data: JSON.stringify(data),
                contentType: "application/json",
                success: function (data) {
                    window.location.reload();
                },
                statusCode: {
                    500: function() {
                        window.location.reload();
                        alert('Unable to create the ticket');
                      }
                }
            });
    }
    function clickSearch() {

        $.ajax({
            type: "GET",
            url: "/search/"+document.getElementById('search').value,

            contentType: "application/json",
            complete: function (data, textStatus) {
                console.log("complete.statusCode=" + data.statusCode);
            },
            success: function (data) {
                window.location.href = "/search/"+document.getElementById('search').value;
            }
        });
        }
    function onProfileClick() {
             $.ajax({
                type: "GET",
                url: "/user",
                data: "{}",
                contentType: "application/json",
                complete: function (data, textStatus) {
                    console.log("complete.statusCode=" + data.statusCode);
                },
                success: function (data) {
                    window.open('http://127.0.0.1:8080/user');
            }
        });
        }
</script>
<!-- ____________________________________________________________________________________ -->
    <script src="static/res/js/jquery/jquery-1.11.3.min.js"></script>
    <script src="static/res/js/bootstrap.min.js"></script>
    <script src="static/res/js/holder.min.js"></script>
    <script src="static/res/js/ie10-viewport-bug-workaround.js"></script>
  </body>
</html>
