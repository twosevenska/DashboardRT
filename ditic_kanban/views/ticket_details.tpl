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

    <link href="../static/res/css/bootstrap.min.css" rel="stylesheet">
    <link href="../static/res/css/bootstrap-theme.min.css" rel="stylesheet">
    <link href="../static/res/css/tdetail.css" rel="stylesheet">

    </head>
<body background="../static/res/img/background.png" style="background-repeat: repeat;">

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
  <h1><small>Details of the ticket #{{ticket_id}}:</small> {{subject}}  </h1>
  <button class="btn btn-primary" onclick="onCommentClick({{ticket_id}})" type="button" title="Comment this ticket">
    Comment
  </button>
  <div class="row">
    <div class="col-md-8">
    	<div class="col-md-4">
  			<h2>The Basics:</h2>
  			<h4>id:<small> {{ticket_id}}</small></h4>
  			<h4>Status:<small> {{status}}</small></h4>
  			<h4>Priority:<small> {{priority}}</small></h4>
  			<h4>Queue:<small> {{queue}}</small></h4>

  			<h2>People:</h2>

  			<h4>Owner:<small> {{owner}}</small></h4>
  			<h4>Requestors:<small> {{requestors}}</small></h4>
  			<h4>Cc:<small> {{cc}}</small></h4>
  			<h4>AdminCc:<small> {{admincc}}</small></h4>
      </div>
      <div class="col-md-4">
  			<h2>Dates:</h2>
  			<h4>Created:<small>  {{created}}</small></h4>
  			<h4>Starts:<small> {{starts}}</small></h4>
  			<h4>Started:<small>  {{started}}</small></h4>
  			<h4>Last Contact:<small>  {{told}}</small></h4>
  			<h4>Due:<small> {{due}}</small></h4>
  				% closed = get('closed', '')
  				% if closed:
  			<h4>Closed:<small> {{closed}}</small></h4>
  				% end

  				% updated = get('updated', '')
  				% if updated:
  			<h4>Updated:<small> {{updated}}</small></h4>
  			% end

  			<h2>Custom Fields:</h2>

  				% interrupted = get('cf.{ditic-interrupted}', '')
  			<h4>DITIC-interrupted:<small> {{interrupted}}</small></h4>

  				% urgent = get('cf.{ditic-urgent}', '')
  			<h4>DITIC-urgent:<small> {{urgent}}</small></h4>

  				% sistemas = get('cf.{is - informatica e sistemas}', '')
  			<h4>IS - Informatica e Sistemas:<small> {{sistemas}}</small></h4>

  				% servico = get('cf.{servico}', '')
  			<h4>Servico:<small> {{servico}}</small></h4>
      </div>
    </div>
    <div class="col-md-4">

      <h2>History:</h2>
      % for item in history :
        <a href="/ticket/{{ticket_id}}/history/{{item[0]}}">{{item[1]}}</a><br><br>
      % end
    </div>
  </div>
</div>
<script src="/static/res/js/jquery/jquery-1.11.3.min.js"></script>
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
function onCommentClick(ticketId) {

            msg = prompt("Enter comment:", "");
            $.ajax({
                type: "POST",
                url: "/ticket/"+ticketId+"/comment/"+msg,
                data: "{}",
                contentType: "application/json",
                success: function (data) {
                    window.location.reload();
                },
                statusCode: {
                    500: function() {
                        window.location.reload();
                        alert('Internal error. Unable to comment.');
                      }
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
    <script src="/static/res/js/jquery/jquery-1.11.3.min.js"></script>
    <script src="/static/res/js/bootstrap.min.js"></script>
	<script src="/static/res/bootstrap-table/bootstrap-table.js"></script>
    <script src="/static/res/js/ie10-viewport-bug-workaround.js"></script>
 	<!-- Populate Grid -->
 	<script src="/static/res/js/my-tickets-tables.js"></script>

</body>
</html>