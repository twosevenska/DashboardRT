% max_len = 30
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

    <link href="/static/res/css/bootstrap.min.css" rel="stylesheet">
    <link href="/static/res/css/bootstrap-theme.min.css" rel="stylesheet">
    <link href="/static/res/css/dashboard.css" rel="stylesheet">
    <link href="/static/res/css/sidebar.css" rel="stylesheet">
	<link href="/static/res/css/bootstrap-table/bootstrap-table.css" rel="stylesheet">

    <script src="/static/res/js/ie-emulation-modes-warning.js"></script>
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
                <li><a href="#">Logout</a></li>
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
            <button type="submit" class="btn btn-primary">Search</button>
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
      <div class="sidebar">
			<div id="title" style="fa fa-home fa-2x color: white" >
				<h2>Dir-Inbox</h2>
			</div>
			<div id="chatlist">
				<table id="dir-inbox-table" class="dir-inbox-table col-md-3" data-show-header="false"></table>
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
                <tr><td>
                    % for priority in sorted(tickets[status], reverse=True):
                    % for ticket in tickets[status][priority]:
                    % if ticket['kanban_actions']['interrupted']:
                    <button onclick="actionButton({{ticket['id']}}, 'interrupted')" type="button">
                            <span class="glyphicon glyphicon-ban-circle" aria-hidden="true"></span>
                    </button>
                    % end
                    % if ticket['kanban_actions']['increase_priority']:
                    <button onclick="actionButton({{ticket['id']}}, 'increase_priority')" type="button">
                            <span class="glyphicon glyphicon-menu-up" aria-hidden="true"></span>
                    </button>
                    % end
                    </td><td>
                    <a title="#{{ticket['id']}}
                        Owner: {{ticket['owner']}}
                        Status: {{ticket['status']}}
                        TimeWorked: {{ticket['timeworked']}}

                        Requestor: {{ticket['requestors']}}
                        Subject: {{ticket['subject']}}" href="/ticket/{{ticket['id']}}?o={{get('username_id', '')}}">
                        {{ticket['id']}}
                        % subject = ticket['subject']
                        % if len(ticket['subject']) > max_len:
                        %   subject = ticket['subject'][:max_len]+'...'
                        % end
                        {{subject}}
                    </a>
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
                    </td>
                    % end
                    % end
                %   end
                % end
                </tr>
                </div>
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
                        <tr><td>
                        % for ticket in tickets[status][priority]:
                        % if ticket['kanban_actions']['back']:
                        <button onclick="actionButton({{ticket['id']}}, 'back')" type="button">
                            <span class="glyphicon glyphicon-menu-left" aria-hidden="true"></span>
                        </button>
                        </td><td>
                        % end
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
                        <a title="#{{ticket['id']}}
                            Owner: {{ticket['owner']}}
                            Status: {{ticket['status']}}
                            TimeWorked: {{ticket['timeworked']}}

                            Requestor: {{ticket['requestors']}}
                            Subject: {{ticket['subject']}}" href="/ticket/{{ticket['id']}}?o={{get('username_id', '')}}">
                            {{ticket['id']}}
                            % subject = ticket['subject']
                            % if len(ticket['subject']) > max_len:
                            %   subject = ticket['subject'][:max_len]+'...'
                            % end
                            {{subject}}
                        </a>
                        </td><td>
                        % if ticket['kanban_actions']['decrease_priority']:
                        <button onclick="actionButton({{ticket['id']}}, 'decrease_priority')" type="button">
                            <span class="glyphicon glyphicon-menu-down" aria-hidden="true"></span>
                        </button>
                        </td><td>
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
                        <tr><td>
                        % for ticket in tickets[status][priority]:
                        % if ticket['kanban_actions']['back']:
                        <button onclick="actionButton({{ticket['id']}}, 'back')" type="button">
                            <span class="glyphicon glyphicon-menu-left" aria-hidden="true"></span>
                        </button>
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
                        <a title="#{{ticket['id']}}
                            Owner: {{ticket['owner']}}
                            Status: {{ticket['status']}}
                            TimeWorked: {{ticket['timeworked']}}

                            Requestor: {{ticket['requestors']}}
                            Subject: {{ticket['subject']}}" href="/ticket/{{ticket['id']}}?o={{get('username_id', '')}}">
                            {{ticket['id']}}
                            % subject = ticket['subject']
                            % if len(ticket['subject']) > max_len:
                            %   subject = ticket['subject'][:max_len]+'...'
                            % end
                            {{subject}}
                        </a>
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
                        % if ticket['kanban_actions']['back']:
                        <button onclick="actionButton({{ticket['id']}}, 'back')">&lt;</button>
                        % end
                        % if ticket['kanban_actions']['interrupted']:
                        <button onclick="actionButton({{ticket['id']}}, 'interrupted');">/</button>
                        % end
                        % if ticket['kanban_actions']['increase_priority']:
                        <button onclick="actionButton({{ticket['id']}}, 'increase_priority')">^</button>
                        % end
                        <tr><td><a title="#{{ticket['id']}}
                            Owner: {{ticket['owner']}}
                            Status: {{ticket['status']}}
                            TimeWorked: {{ticket['timeworked']}}

                            Requestor: {{ticket['requestors']}}
                            Subject: {{ticket['subject']}}" href="/ticket/{{ticket['id']}}?o={{get('username_id', '')}}">
                            {{ticket['id']}}
                            % subject = ticket['subject']
                            % if len(ticket['subject']) > max_len:
                            %   subject = ticket['subject'][:max_len]+'...'
                            % end
                            {{subject}}
                        </a></tr></td>
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


<p id="demo"></p>

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
            strReq = forwardButton(ticketId, ticketStatus);
        }
        if (strReq != null) {
            document.getElementById("demo").innerHTML = "strReq:"+strReq;
        }
        request.open("GET", strReq, true);
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
    function forwardButton(ticketId, ticketStatus){
        if(ticketStatus==='open'){
            str = prompt("Enter conclusion condition:", "");
            while(str.length < 4){str = prompt("Enter conclusion condition:", "It is needed at least 4 characters.");}
            return '/ticket/'+ticketId+'/action/forward-'+str.split(' ').join('_')+'?o={{username_id}}&email={{email}}';
        }else{
            return '/ticket/'+ticketId+'/action/forward?o={{username_id}}&email={{email}}';
        }
    }

    function createButton(){
        var request = new XMLHttpRequest();
        request.onload = function(){window.location.reload()}
        request.open("POST",'/ticket?o={{username_id}}&email={{email}}',true);
        request.send(document.getElementById('sub').value + '\n' + document.getElementById('text').value);
    }
</script>
<!-- ____________________________________________________________________________________ -->
    <script src="/static/res/js/jquery/jquery-1.11.3.min.js"></script>
    <script src="/static/res/js/bootstrap.min.js"></script>
    <script src="/static/res/js/ie10-viewport-bug-workaround.js"></script>
	<script src="/static/res/bootstrap-table/bootstrap-table.js"></script>
 	<!-- Populate Grid -->
 	<script src="/static/res/js/my-tickets-tables.js"></script>
	<script>
	</script>
  </body>
</html>