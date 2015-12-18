<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="description" content="Dashboard RT - Logic Box">
    <meta name="author" content="Alexandre Vieira, André Martinez, Eduardo Pereira, Gloriya Gostyaeva, Gonçalo Barroso, Roberto Cunha">

    <title>DITIC Kanban</title>

    <link href="static/res/css/bootstrap.min.css" rel="stylesheet">
    <link href="static/res/css/bootstrap-theme.min.css" rel="stylesheet">
    <link href="static/res/css/dashboard.css" rel="stylesheet">

    <script src="static/res/js/ie-emulation-modes-warning.js"></script>
  </head>

  <body background="static/res/img/background.png" style="background-repeat: repeat;">

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
            <li><a href="#">Profile</a></li>
            <li><a href="#">Preferences</a></li>
            <li><a href="" onClick="onLogoutClick()">Logout</a></li>
            <!--<li role="separator" class="divider"></li>
            <li class="dropdown-header">Nav header</li>
            <li><a href="#">Separated link</a></li>
            <li><a href="#">One more separated link</a></li>-->
          </ul>
        </li>
      </ul>
      <!-- SEARCH -->
      <form class="navbar-form navbar-right">
        <input type="text" class="form-control" placeholder="Search...">
        <button type="submit" class="btn btn-primary">Search</button>
      </form>

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



<br>
<div class="container" background="red">
    <div class="row">
    <div id="title" align="center">
        <div class="col-md-3">DIR</div>
        <div class="col-md-3">DIR</div>
        <div class="col-md-3">DIR-INBOX</div>
        <div class="col-md-3">DIR</div>
    </div>
    </div>
    <div class="row">
    <!-- Row for Titles -->
    <div class="chatlist" style="margin-left:7px; margin-right:7px;">
        <table data-toggle="table" class="dir-inbox-table" data-show-header="false">
            <thead>
                <tr>
                    <th data-valign="middle"></th>
                    <th data-valign="middle"></th>
                    <th data-valign="middle"></th>
                    <th data-valign="middle"></th>
                    <th data-valign="middle"></th>
                    <th data-valign="middle"></th>
                </tr>
            </thead>
            <tbody>
                    % for priority in sorted(dir['tickets'], reverse=True):
                    % for ticket in dir['tickets'][priority]:
                    <tr><td>
                    % if ticket['kanban_actions']['back']:
                    <button onclick="actionButton({{ticket['id']}}, 'back')" type="button">
                            <span class="glyphicon glyphicon-menu-left" aria-hidden="true"></span>
                    </button>
                    </td><td>
                    %end
                    % if ticket['kanban_actions']['interrupted']:
                    <button onclick="actionButton({{ticket['id']}}, 'interrupted')" type="button">
                            <span class="glyphicon glyphicon-ban-circle" aria-hidden="true"></span>
                    </button>
                    </td><td>
                    % end
                    % if ticket['kanban_actions']['increase_priority']:
                    <button onclick="actionButton({{ticket['id']}}, 'increase_priority')" type="button">
                            <span class="glyphicon glyphicon-menu-up" aria-hidden="true"></span>
                    </button>
                    % end
                    </td><td>
                    <button onclick="clickTicket({{ticket['id']}});" type="button">
                        {{ticket['id']}} {{ticket['subject']}}
                    </button>
                    </td><td>
                    % if ticket['kanban_actions']['decrease_priority']:
                    <button onclick="actionButton({{ticket['id']}}, 'decrease_priority')" type="button">
                            <span class="glyphicon glyphicon-menu-down" aria-hidden="true"></span>
                    </button>
                    </td><td>
                    % end
                    % if ticket['kanban_actions']['stalled']:
                    <button onclick="actionButton({{ticket['id']}}, 'stalled')" type="button" style="outline: thin solid black;">
                            <span class="glyphicon glyphicon-time" aria-hidden="true"></span>
                    </button>
                    </td><td>
                    % end
                    % if ticket['kanban_actions']['forward']:
                    <button onclick="actionButton({{ticket['id']}}, 'forward', '{{ticket['status']}}')" type="button">
                            <span class="glyphicon glyphicon-menu-right" aria-hidden="true"></span>
                    </button>
                    </td><td>
                    % end
                    %if 'yes' in ticket['cf.{ditic-urgent}']:
                        <button onclick="actionButton({{ticket['id']}}, 'unset_urgent')" type="button">
                            <span class="glyphicon glyphicon-flash" aria-hidden="true"></span>
                        </button>
                        </td><td>
                    %else:
                        <button onclick="actionButton({{ticket['id']}}, 'set_urgent')" title="Make ticket Urgent">
                            <span class="glyphicon glyphicon-fire" aria-hidden="true"></span>
                        </button>
                        </td><td>
                    %end
                    <button onclick="actionButton({{ticket['id']}}, 'take')">
                        <span class="glyphicon glyphicon-hand-right" aria-hidden="true"></span>
                    </button>
                    </td>
                    % end
                %   end
                            
                </tr>
            </tbody>
        </table>
        </div>
        </div>
</div>
<!-- 
    TABLES 
    
    <div class="jumbotron">

        <div class="centerTables">
        <div class="row">
          <h2 class="col-md-3">DIR</h2>
          <h2 class="col-md-3">DIR-INBOX</h2>
        </div>
          <div class="row">
            <div class="col-md-3">
              <table data-toggle="table" class="dir-table" data-show-header="false">
                <thead>
                  <tr>
                    <th data-valign="middle"></th>
                    <th data-valign="middle"></th>
                    <th data-valign="middle"></th>
                    <th data-valign="middle"></th>
                  </tr>
                </thead>
              <tbody>
                % for priority in sorted(dir['tickets'], reverse=True):
                    % for ticket in dir['tickets'][priority]:
                    <tr><td>
                    % if ticket['kanban_actions']['back']:
                    <button onclick="actionButton({{ticket['id']}}, 'back')" type="button">
                            <span class="glyphicon glyphicon-menu-left" aria-hidden="true"></span>
                    </button>
                    </td><td>
                    %end
                    % if ticket['kanban_actions']['interrupted']:
                    <button onclick="actionButton({{ticket['id']}}, 'interrupted')" type="button">
                            <span class="glyphicon glyphicon-ban-circle" aria-hidden="true"></span>
                    </button>
                    </td><td>
                    % end
                    % if ticket['kanban_actions']['increase_priority']:
                    <button onclick="actionButton({{ticket['id']}}, 'increase_priority')" type="button">
                            <span class="glyphicon glyphicon-menu-up" aria-hidden="true"></span>
                    </button>
                    % end
                    </td><td>
                    <button onclick="clickTicket({{ticket['id']}});" type="button">
                        {{ticket['id']}} {{ticket['subject']}}
                    </button>
                    </td><td>
                    % if ticket['kanban_actions']['decrease_priority']:
                    <button onclick="actionButton({{ticket['id']}}, 'decrease_priority')" type="button">
                            <span class="glyphicon glyphicon-menu-down" aria-hidden="true"></span>
                    </button>
                    </td><td>
                    % end
                    % if ticket['kanban_actions']['stalled']:
                    <button onclick="actionButton({{ticket['id']}}, 'stalled')" type="button">
                            <span class="glyphicon glyphicon-time" aria-hidden="true"></span>
                    </button>
                    </td><td>
                    % end
                    %if 'yes' in ticket['cf.{ditic-urgent}']:
                        <button onclick="actionButton({{ticket['id']}}, 'unset_urgent')" type="button">
                            <span class="glyphicon glyphicon-flash" aria-hidden="true"></span>
                        </button>
                        </td>
                    %else:
                        <button onclick="actionButton({{ticket['id']}}, 'set_urgent')" title="Make ticket Urgent">
                            <span class="glyphicon glyphicon-fire" aria-hidden="true"></span>
                        </button>
                        </td><td>
                    %end
                    % if ticket['kanban_actions']['forward']:
                    <button onclick="actionButton({{ticket['id']}}, 'forward', '{{ticket['status']}}')" type="button">
                            <span class="glyphicon glyphicon-menu-right" aria-hidden="true"></span>
                    </button>
                    </td>
                    %end
                    %end
                %end
                        
            </tbody>
        </table>
        
    </div>
            </div>
            <div class="glyphs-dirs">
              <img src="static/res/img/right.png" class="featurette-image img-responsive down" alt="right">
              <img src="static/res/img/left.png" class="featurette-image img-responsive down" alt="left">
            </div>

            <div class="col-md-3">
              <div id="chatlist" class="col-md-2 mousescroll">
                <table data-toggle="table" class="dir-table" data-show-header="false">
                <thead>
                  <tr>
                    <th data-valign="middle"></th>
                    <th data-valign="middle"></th>
                    <th data-valign="middle"></th>
                    <th data-valign="middle"></th>
                  </tr>
                </thead>
              <tbody>
                % for priority in sorted(dirinbox['tickets'], reverse=True):
                    % for ticket in dirinbox['tickets'][priority]:
                    <tr><td>
                    % if ticket['kanban_actions']['back']:
                    <button onclick="actionButton({{ticket['id']}}, 'back')" type="button">
                            <span class="glyphicon glyphicon-menu-left" aria-hidden="true"></span>
                    </button>
                    </td><td>
                    %end
                    % if ticket['kanban_actions']['interrupted']:
                    <button onclick="actionButton({{ticket['id']}}, 'interrupted')" type="button">
                            <span class="glyphicon glyphicon-ban-circle" aria-hidden="true"></span>
                    </button>
                    </td><td>
                    % end
                    % if ticket['kanban_actions']['increase_priority']:
                    <button onclick="actionButton({{ticket['id']}}, 'increase_priority')" type="button">
                            <span class="glyphicon glyphicon-menu-up" aria-hidden="true"></span>
                    </button>
                    % end
                    </td><td>
                    <button onclick="clickTicket({{ticket['id']}});" type="button">
                        {{ticket['id']}} {{ticket['subject']}}
                    </button>
                    </td><td>
                    % if ticket['kanban_actions']['decrease_priority']:
                    <button onclick="actionButton({{ticket['id']}}, 'decrease_priority')" type="button">
                            <span class="glyphicon glyphicon-menu-down" aria-hidden="true"></span>
                    </button>
                    </td><td>
                    % end
                    % if ticket['kanban_actions']['stalled']:
                    <button onclick="actionButton({{ticket['id']}}, 'stalled')" type="button">
                            <span class="glyphicon glyphicon-time" aria-hidden="true"></span>
                    </button>
                    </td><td>
                    % end
                    % if ticket['kanban_actions']['forward']:
                    <button onclick="actionButton({{ticket['id']}}, 'forward', '{{ticket['status']}}')" type="button">
                            <span class="glyphicon glyphicon-menu-right" aria-hidden="true"></span>
                    </button>
                    </td><td>
                    % end
                    %if 'yes' in ticket['cf.{ditic-urgent}']:
                        <button onclick="actionButton({{ticket['id']}}, 'unset_urgent')" type="button">
                            <span class="glyphicon glyphicon-flash" aria-hidden="true"></span>
                        </button>
                        </td>
                    %else:
                        <button onclick="actionButton({{ticket['id']}}, 'set_urgent')" title="Make ticket Urgent">
                            <span class="glyphicon glyphicon-fire" aria-hidden="true"></span>
                        </button>
                        </td>
                    %end
                    %end
                %end
                        
            </tbody>
        </table>
              </div>
          </div>
          
          
        </div>
    </div>
-->

<!-- ____________________________________________________________________________________ -->
    <script src="/static/res/js/jquery/jquery-1.11.3.min.js"></script>
    <script src="/static/res/js/bootstrap.min.js"></script>
    <script src="/static/res/js/holder.min.js"></script>
    <script src="/static/res/js/ie10-viewport-bug-workaround.js"></script>
    
  <script src="/static/res/js/my-tickets-tables.js"></script>
    <script>
    function actionButton(ticketId, action, ticketStatus){
        var request = new XMLHttpRequest();
        request.onload = function(){window.location.reload()}

        if(action==='back'){
            strReq = backButton(ticketId);
        }else if(action==='interrupted'){
            strReq = interruptedButton(ticketId);
        }else if(action==='increase_priority'){
            strReq = increasePriorityButton(ticketId);
        }else if(action==='decrease_priority'){
            strReq = decreasePriorityButton(ticketId);
        }else if(action==='stalled'){
            strReq = stalledButton(ticketId);
        }else if(action==='forward'){
            if(ticketStatus==='open'){
                forwardButton(ticketId);
                return;
            }else{
                strReq = '/ticket/'+ticketId+'/action/forward';
            }
        }else if(action==='set_urgent'){
            strReq = setUrgentButton(ticketId, ticketStatus);
        }else if(action==='unset_urgent'){
            strReq = unsetUrgentButton(ticketId, ticketStatus);
        }else if(action === 'take'){
            strReq = takeButton(ticketId)
        }

        request.open("PUT", strReq, true);
        request.send();
    }

    function backButton(ticketId){
        return '/ticket/'+ticketId+'/action/back?o={{username_id}}&email={{email}}';
    }
    function interruptedButton(ticketId){
        return '/ticket/'+ticketId+'/action/interrupted?o={{username_id}}&email={{email}}';
    }
    function increasePriorityButton(ticketId){
        return '/ticket/'+ticketId+'/action/increase_priority?o={{username_id}}&email={{email}}';
    }
    function decreasePriorityButton(ticketId){
        return '/ticket/'+ticketId+'/action/decrease_priority?o={{username_id}}&email={{email}}';
    }
    function stalledButton(ticketId){
        return '/ticket/'+ticketId+'/action/stalled?o={{username_id}}&email={{email}}';
    }
    function takeButton(ticketId){
        return '/ticket/'+ticketId+'/action/take';
    }
    function unsetUrgentButton(ticketId){
        return '/ticket/'+ticketId+'/action/unset_urgent';
    }
    function setUrgentButton(ticketId){
        return '/ticket/'+ticketId+'/action/set_urgent';
    }
    function forwardButton(ticketId){

        str = prompt("Enter conclusion condition:", "");
        while(str.length < 4){str = prompt("Enter conclusion condition:", "It is needed at least 4 characters.");}
        
        $.ajax({
                type: "PUT",
                url: "/ticket/"+ticketId+"/action/forward-"+str,
                data: "{}",
                contentType: "application/json",
                success: function (data) {
                    window.location.reload();
                },
                statusCode: {
                    500: function() {
                        window.location.reload();
                        alert('Unable to mark ticket as done');
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
    function clickTicket(ticketId) {
            $.ajax({
                type: "GET",
                url: "/ticket/"+ticketId,
                complete: function (data, textStatus) {
                    console.log("complete.statusCode=" + data.statusCode);
                },
                success: function (data) {
                    window.location.href = "/ticket/"+ticketId;
                }
            });
        }
    </script>
  </body>
</html>
