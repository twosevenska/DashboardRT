<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta charset="UTF-8">

    <meta name="description" content="Dashboard RT - Logic Box">
    <meta name="author" content="Alexandre Vieira, André Martinez, Eduardo Pereira, Gloriya Gostyaeva, Gonçalo Barroso, Roberto Cunha">

    <title>DITIC Kanban</title>

    <link href="../../../static/res/css/bootstrap.min.css" rel="stylesheet">
    <link href="../../../static/res/css/bootstrap-theme.min.css" rel="stylesheet">
    <link href="../../../static/res/css/tdetail.css" rel="stylesheet">

</head>
<body background="../../../static/res/img/background.png" style="background-repeat: repeat;">
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

<p> &nbsp </p>
<p> &nbsp </p>
<div class="container ticket_detail">
    
        <h2>
            <small>Ticket #{{ticket_id}}</small>
            <br>
            History item #{{item_id}}: <small>{{description}}</small>
        </h2>
        <hr>
        <div class="row vdivide">
            <div class="col-md-4">
                <h4>Description:<br><small> {{description}}</small></h4>
            </div>
            <div class="col-md-4">
                <h4>Created:<br><small> {{created}}</small></h4>
            </div>
            <div class="col-md-4">
                <h4>Creator:<br><small>{{creator}}</small></h4>
            </div>
        </div>
    <hr>
    <h3>Content:</h3>
    <color="black"> {{content}}</color>

    <hr>
    
    <div class="row vdivide">
        <div class="col-md-2">
            <h4>Field: <br><small>{{field}}</small></h4>
        </div>
        <div class="col-md-2">
            <h4>New value:<br><small> {{newvalue}}</small></h4>
        </div>
        <div class="col-md-2">
            <h4>Old value:<br><small> {{oldvalue}}</small></h4>
        </div>
        <div class="col-md-2">
            <h4>Time taken:<br><small> {{timetaken}}</small></h4>
        </div>
        <div class="col-md-2">
            <h4>Type:<br><small> {{type}}</small></h4>
        </div>

    </div><br>
        <p>Time to execute: {{time_spent}}</p>

</div>
<script>
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
<!-- ____________________________________________________________________________________ -->
<script src="/static/res/js/jquery/jquery-1.11.3.min.js"></script>
<script src="/static/res/js/bootstrap.min.js"></script>
<script src="/static/res/bootstrap-table/bootstrap-table.js"></script>
<script src="/static/res/js/ie10-viewport-bug-workaround.js"></script>
<!-- Populate Grid -->
<script src="/static/res/js/my-tickets-tables.js"></script>

</body>
</html>
