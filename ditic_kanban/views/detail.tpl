% max_len = 30
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
    <link href="static/res/css/sidebar.css" rel="stylesheet">
    <link href="static/res/css/bootstrap-table/bootstrap-table.css" rel="stylesheet">
    
</head>
<body background="static/res/img/background.png" style="background-repeat: repeat;">
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
      <form id="form1" class="navbar-form navbar-right">
        <input id="inBtn" type="text" class="form-control" placeholder="Search..." />
        <button id="sBtn" type="button" class="btn btn-primary"action="clickSearch()">Search</button>
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

    

    <!--
    SIDEBAR
    -->
    <nav class="main-menu">
      <div class="sidebar">
        <div id="title" align="center"><h2>DIR-INBOX</h2></div>
        <div align="center">
            % status = 'dir-inbox'
            (max:
            % if status in email_limit:
                {{email_limit[status]}}
            % end
            )
        </div>
        <div class="chatlist" style="margin-left:7px; margin-right:7px; ">
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
                    % for priority in sorted(dirinbox['tickets'], reverse=True):
                    % for ticket in dirinbox['tickets'][priority]:
                    <tr>
                    
                    <td>
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
                    </td><td>
                    % end
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
                    %if number_tickets_per_status['new'] < email_limit['new']:
                        <button onclick="actionButton({{ticket['id']}}, 'take')" type="button">
                            <span class="glyphicon glyphicon-hand-right" aria-hidden="true"></span></button>
                    %else:
                        <span class="glyphicon glyphicon-minus-sign" aria-hidden="true"></span>
                    % end
                    </td>      
                
                    </tr>
                    %end
                %end
            </tbody>
        </table>
        </div>
      </div>
    </nav>

<!-- TABLES -->
  <div class="container">
	<!-- Row for Titles -->
    <div class="row">
        <h2 class="col-md-3">Stalled</h2>
        <h2 class="col-md-3">In</h2>
        <h2 class="col-md-3">Active</h2>
        <h2 class="col-md-3">Done</h2>
    </div>

    <div class="row">
        <h4 class="col-md-3">
            % status = 'stalled'
            % if status in number_tickets_per_status and status >= 1:
                {{number_tickets_per_status[status]}}
            % else:
                0
            % end
        </h4>
        <h4 class="col-md-3">
            % status = 'new'
            % if status in number_tickets_per_status >= 1:
               {{number_tickets_per_status[status]}}
            % else:
                0
            % end
            % if status in email_limit:
                (max: {{email_limit[status]}})
            % end
        </h4>
        <h4 class="col-md-3">
            % status = 'open'
            % if status in number_tickets_per_status >= 1:
                {{number_tickets_per_status[status]}}
            % else:
                0
            % end
            % if status in email_limit:
                (max: {{email_limit[status]}})
            % end
        </h4>
        <h4 class="col-md-3">
            % status = 'resolved'
            % if status in number_tickets_per_status >= 1:
                {{number_tickets_per_status[status]}}
            % else:
                0
            % end
            % if status in email_limit:
                (max: {{email_limit[status]}})
            % end
        </h4>
    </div>

    <!-- Row for ticket tables -->
	<div class="row">
	  <div class="col-md-3">
		<table data-toggle="table" class="stalled-table" data-show-header="false">
            <thead>
                <tr>
                    <th data-valign="middle"></th>
                    <th data-valign="middle"></th>
                    <th data-valign="middle"></th>
                    <th data-valign="middle"></th>
                </tr>
            </thead>
            <tbody>
                % for status in ['stalled']:
                %   if status not in tickets.keys():
                %       continue
                %   end
                    % for priority in sorted(tickets[status], reverse=True):
                    % for ticket in tickets[status][priority]:
                    <tr><td>
                    % if ticket['kanban_actions']['increase_priority']:
                    <button onclick="actionButton({{ticket['id']}}, 'increase_priority')" type="button">
                            <span class="glyphicon glyphicon-menu-up" aria-hidden="true"></span>
                    </button>
                    </td><td>
                    % end
                    <button onclick="clickTicket({{ticket['id']}});">
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
                    % if ticket['kanban_actions']['back']:
                        <button onclick="actionButton({{ticket['id']}}, 'back')" type="button">
                                <span class="glyphicon glyphicon-flash" aria-hidden="true"></span>
                        </button>
                        
                    % else:
                        <span class="glyphicon glyphicon-minus-sign" aria-hidden="true"></span>
                        
                    % end
                    </tr>
                %end
                %end
            % end
            </tbody>
        </table>
	  </div>
	  <div class="col-md-3">
		<table data-toggle="table" class="in-table" data-show-header="false">
            <thead>
                <tr>
                    <th data-valign="middle"></th>
                    <th data-valign="middle"></th>
                    <th data-valign="middle"></th>
                    <th data-valign="middle"></th>
                    <th data-valign="middle"></th>
                </tr>
            </thead>
            <tbody>
                % for status in ['new']:
                %   if status not in tickets.keys():
                %       continue
                %   end
                    % for priority in sorted(tickets[status], reverse=True):
                    % for ticket in tickets[status][priority]:
                    <tr><td>
                    %sts = 'dir-inbox'
                    % if sts in email_limit:
                    % if email_limit.get(sts) > number_tickets_per_status.get(sts):
                    <button onclick="actionButton({{ticket['id']}}, 'back')" type="button">
                            <span class="glyphicon glyphicon-menu-left" aria-hidden="true"></span>
                    </button>
                    </td><td>
                    % else:
                        <span class="glyphicon glyphicon-minus-sign" aria-hidden="true"></span>
                    </td><td>
                    % end
                    %end
                    % if ticket['kanban_actions']['increase_priority']:
                    <button onclick="actionButton({{ticket['id']}}, 'increase_priority')" type="button">
                            <span class="glyphicon glyphicon-menu-up" aria-hidden="true"></span>
                    </button>
                    </td><td>
                    % end
                    <button onclick="clickTicket({{ticket['id']}});">
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
                    % else:
                        <span class="glyphicon glyphicon-minus-sign" aria-hidden="true"></span>
                        
                    % end
                    </td>

                    </tr>
                
                %   end
            % end
            </tbody>
        </table>
	 </div>
	  <div class="col-md-3">
		<table data-toggle="table" class="active-table" data-show-header="false">
            <thead>
                <tr>
                    <th data-valign="middle"></th>
                    <th data-valign="middle"></th>
                    <th data-valign="middle"></th>
                    <th data-valign="middle"></th>
                    <th data-valign="middle"></th>
                </tr>
            </thead>
            <tbody>
                % for status in ['open']:

                    %   if status not in tickets.keys():
                    %       continue
                    %   end

                    % for priority in sorted(tickets[status], reverse=True):
                        % for ticket in tickets[status][priority]:
                        <tr><td>
                        % if ticket['kanban_actions']['back']:
                        <button onclick="actionButton({{ticket['id']}}, 'back')" type="button">
                            <span class="glyphicon glyphicon-menu-left" aria-hidden="true"></span>
                        </button>
                        </td><td>
                        % else: 
                            <span class="glyphicon glyphicon-minus-sign" aria-hidden="true"></span>
                        </td><td>
                        % end
                        % if ticket['kanban_actions']['increase_priority']:
                        <button onclick="actionButton({{ticket['id']}}, 'increase_priority')" type="button">
                            <span class="glyphicon glyphicon-menu-up" aria-hidden="true"></span></button>

                        % end
                        % if ticket['kanban_actions']['interrupted']:
                        <button onclick="actionButton({{ticket['id']}}, 'interrupted')" type="button">
                            <span class="glyphicon glyphicon-ban-circle" aria-hidden="true"></span>
                        </button>
                        </td><td>
                        % end
                        <button onclick="clickTicket({{ticket['id']}});" type="button">
                            {{ticket['id']}} {{ticket['subject']}}
                        </button>
                        </td><td>
                        % if ticket['kanban_actions']['decrease_priority']:
                        <button onclick="actionButton({{ticket['id']}}, 'decrease_priority')" type="button">
                            <span class="glyphicon glyphicon-menu-down" aria-hidden="true"></span></button>
                        % end
                        % if ticket['kanban_actions']['stalled']:
                        <button onclick="actionButton({{ticket['id']}}, 'stalled')" type="button">
                            <span class="glyphicon glyphicon-time" aria-hidden="true"></span></button>
                        </td><td>
                        % end
                        % if ticket['kanban_actions']['forward']:
                        <button onclick="actionButton({{ticket['id']}}, 'forward', '{{ticket['status']}}')" type="button">
                            <span class="glyphicon glyphicon-menu-right" aria-hidden="true"></span></button>
                        % end
                        % end
                        </td></tr>
                    % end
                % end
            </tbody>
        </table>
	 </div>
	 <div class="col-md-3">
		<table data-toggle="table" class="in-table" data-show-header="false">
            <thead>
                <tr>
                    <th></th>
                </tr>
            </thead>
            <tbody>
                % for status in ['resolved']:

                    %   if status not in tickets.keys():
                    %       continue
                    %   end

                    % for priority in sorted(tickets[status], reverse=True):
                        % for ticket in tickets[status][priority]:
                        <tr><td>
                        % if ticket['kanban_actions']['back']:
                        <button onclick="actionButton({{ticket['id']}}, 'back')">&lt;</button>
                        % end
                        % if ticket['kanban_actions']['interrupted']:
                        <button onclick="actionButton({{ticket['id']}}, 'interrupted');">/</button>
                        % end
                        % if ticket['kanban_actions']['increase_priority']:
                        <button onclick="actionButton({{ticket['id']}}, 'increase_priority')">^</button>
                        % end
                        <button onclick="clickTicket({{ticket['id']}});">
                        {{ticket['id']}} {{ticket['subject']}}
                        </button></tr></td>
                        % if ticket['kanban_actions']['decrease_priority']:
                        <button onclick="actionButton({{ticket['id']}}, 'decrease_priority')">v</button>
                        % end
                        % if ticket['kanban_actions']['stalled']:
                        <button onclick="actionButton({{ticket['id']}}, 'stalled')">\</button>
                        % end
                        % if ticket['kanban_actions']['forward']:
                        <button onclick="actionButton({{ticket['id']}}, 'forward', '{{ticket['status']}}')">&gt;</button>
                        % end
                        % end
                    % end
                % end
            </tbody>
        </table>
	 </div>
	</div>
    </div>
  </div>

<script>
    function actionButton(ticketId, action, ticketStatus){
        if(ticketStatus=='open'){
            str = prompt("Enter conclusion condition:", "");
            while(str.length < 4){str = prompt("Enter conclusion condition:", "It is needed at least 4 characters.");}
        }
        $.ajax({
            type: "PUT",
            url: "/ticket/"+ticketId+"/action/"+action,
            data: JSON.stringify({'ticketmail':ticketStatus}),
            contentType: "application/json",
            success: function (data) {
                window.location.reload();
            },
            statusCode: {
                500: function() {
                    window.location.reload();
                    alert('Unable to resolve action');
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
    function clickSearch(ticketId) {
            var form = document.getElementById("form1");
            dat = form.submit();
             $.ajax({
            type: "POST",
            url: "/search",
            data: JSON.stringify(dat),
            contentType: "application/json",
            complete: function (data, textStatus) {
                console.log("complete.statusCode=" + data.statusCode);
            },
            success: function (data) {
                window.location.href = "/search";
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