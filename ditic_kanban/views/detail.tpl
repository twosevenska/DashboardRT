% include('navigator')
% max_len = 30

<!--SIDEBAR-->
<nav class="main-menu">
  <div class="sidebar">
    <div id="title" style="fa fa-home fa-2x color: white" >
      <h2>Dir-Inbox</h2>
    </div>
    <div id="chatlist">
      <table id="dir-inbox-table" class="dir-inbox-table col-md-3" data-show-header="false">
      	
        % for priority in sorted(tickets, reverse=True):
        <tr>
          <td valign="top">
            <strong>{{priority}}</strong>
          </td>
          <td valign="top">
            <table border="0">
              % for ticket in sorted(tickets[priority], reverse=True):
              %if ticket['cf.{is - informatica e sistemas}'] == 'dir-inbox':
              <tr>
                <td>
                  &nbsp;&nbsp;
                  % if ticket['kanban_actions']['back']:
                    <button onclick="actionButton({{ticket['id']}}, 'back')">&lt;</button>
                  % end
                  % if ticket['kanban_actions']['interrupted']:
                    <button onclick="actionButton({{ticket['id']}}, 'interrupted');">/</button>
                  % end
                  % if ticket['kanban_actions']['increase_priority']:
                    <button onclick="actionButton({{ticket['id']}}, 'increase_priority')">^</button>
                  % end
                </td>
                <td>
                  <a href="http://domo-kun.noip.me/rt/Ticket/Display.html?id={{ticket['id']}}">
                    {{ticket['id']}}
                  </a>
                </td>
                <td>
                  {{ticket['status']}}
                </td>
                <td>
                  {{ticket['cf.{servico}']}}
                </td>
                <td>
                  %if len(ticket['requestors']) > 0:
                    {{ticket['requestors']}}
                  %else:
                    no req
                  %end
                </td>
                <td>
                  % subject = ticket['subject']
                  % if len(ticket['subject']) > max_len:
                  %   subject = ticket['subject'][:max_len]+'...'
                  % end
                  {{subject}}               
                </td>
                <td>
                  Created: {{ticket['created']}}<br>
                  Last Update: {{ticket['lastupdated']}}  
                </td>
                <td>
                  % if ticket['kanban_actions']['decrease_priority']:
                    <button onclick="actionButton({{ticket['id']}}, 'decrease_priority')">v</button>
                  % end

                  % if ticket['kanban_actions']['stalled']:
                    <button onclick="actionButton({{ticket['id']}}, 'stalled')">\</button>
                  % end

                  % if ticket['kanban_actions']['forward']:
                    <button onclick="actionButton({{ticket['id']}}, 'forward', '{{ticket['status']}}')">&gt;</button>
                  % end

                  % if email == 'dir-inbox':
                    <button onclick="actionButton({{ticket['id']}}, 'take')">Take</button>
                  %end

                  %if ticket.get('cf.{ditic-urgent}', ''):
                    <button onclick="actionButton({{ticket['id']}}, 'unsetUrgent')" title="Make ticket not urgent">Not Urgent</button>
                  %else:
                    <button onclick="actionButton({{ticket['id']}}, 'setUrgent')" title="Make ticket Urgent">Urgent</button>
                  %end
                </td>
              </tr>
              % end
              %end
            </table>
          </td>
        </tr>
        % end
      </table>
    </div>
  </div>
</nav>
            % status = 'stalled'
            % if status in number_tickets_per_status:
            {{number_tickets_per_status[status]}}
            % end
<!-- TABLES -->
<div class="container">
<!-- Row for Titles -->
<div class="row">
    <h2 class="col-md-3">Stalled</h2>
    <h2 class="col-md-3">In</h2>
    <h2 class="col-md-3">Active</h2>
    <h2 class="col-md-3">Done</h2>
</div>

<!-- Row for ticket tables -->
<div class="row">
  <div class="col-md-3">
	<table data-toggle="table" class="stalled-table">
        <thead>
        </thead>
        <tbody>
        </tbody>
    </table>
  </div>
  <div class="col-md-3">
	<table id="in-table" class="in-table" data-show-header="false"></table>
 </div>
  <div class="col-md-3">
	<table id="active-table" class="active-table" data-show-header="false"></table>
 </div>
 <div class="col-md-3">
	<table id="done-table" class="done-table" data-show-header="false"></table>
 </div>
</div>

<table data-toggle="table" class="stalled-table">
    <thead>
        <tr>
            <td align="center">
                <strong>Stalled</strong><br>

            </td>

            <td>
                <strong>IN</strong><br>
                % status = 'new'
                % if status in number_tickets_per_status:
                    <strong>{{number_tickets_per_status[status]}}</strong>
                % end
                % if status in email_limit:
                    (max: {{email_limit[status]}})
                % end
            </td>

            <td>
                <strong>ACTIVE</strong><br>
                % status = 'open'
                % if status in number_tickets_per_status:
                    <strong>{{number_tickets_per_status[status]}}</strong>
                % end
                % if status in email_limit:
                    (max: {{email_limit[status]}})
                % end
            </td>

            <td>
                <strong>DONE</strong><br>
                % status = 'resolved'
                % if status in number_tickets_per_status:
                    <strong>{{number_tickets_per_status[status]}}</strong>
                % end
                % if status in email_limit:
                    (max: {{email_limit[status]}})
                % end
            </td>
        </tr>
    </thead>
    <tbody>
         <tr>
            % for status in ['stalled']:

            %   if status not in tickets.keys():
            %       continue
            %   end
            <td>
                %   for priority in sorted(tickets[status], reverse=True):
                {{priority}}<br>
                % for ticket in tickets[status][priority]:
                &nbsp;&nbsp;
                % if ticket['kanban_actions']['back']:
                <button onclick="actionButton({{ticket['id']}}, 'back')">&lt;</button>
                % end
                % if ticket['kanban_actions']['interrupted']:
                <button onclick="actionButton({{ticket['id']}}, 'interrupted');">/</button>
                % end
                % if ticket['kanban_actions']['increase_priority']:
                <button onclick="actionButton({{ticket['id']}}, 'increase_priority')">^</button>
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
                % if ticket['kanban_actions']['decrease_priority']:
                <button onclick="actionButton({{ticket['id']}}, 'decrease_priority')">v</button>
                % end
                % if ticket['kanban_actions']['stalled']:
                <button onclick="actionButton({{ticket['id']}}, 'stalled')">\</button>
                % end
                % if ticket['kanban_actions']['forward']:
                <button onclick="actionButton({{ticket['id']}}, 'forward', '{{ticket['status']}}')">&gt;</button>
                % end
                <br>
                % end
            %   end
            </td>
            % end
            </div>
        </tr>
        <tr>
            % for status in ['new', 'open', 'resolved']:
            %   if status not in tickets.keys():
            <td></td>
            %       continue
            %   end
            <div align="center" style="background-color: red;">
            <td valign="top">
            %   for priority in sorted(tickets[status], reverse=True):
                {{priority}}<br>
                % for ticket in tickets[status][priority]:
                &nbsp;&nbsp;
                % if ticket['kanban_actions']['back']:
                <button onclick="actionButton({{ticket['id']}}, 'back')">&lt;</button>
                % end
                % if ticket['kanban_actions']['interrupted']:
                <button onclick="actionButton({{ticket['id']}}, 'interrupted');">/</button>
                % end
                % if ticket['kanban_actions']['increase_priority']:
                <button onclick="actionButton({{ticket['id']}}, 'increase_priority')">^</button>
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
                % if ticket['kanban_actions']['decrease_priority']:
                <button onclick="actionButton({{ticket['id']}}, 'decrease_priority')">v</button>
                % end
                % if ticket['kanban_actions']['stalled']:
                <button onclick="actionButton({{ticket['id']}}, 'stalled')">\</button>
                % end
                % if ticket['kanban_actions']['forward']:
                <button onclick="actionButton({{ticket['id']}}, 'forward', '{{ticket['status']}}')">&gt;</button>
                % end
                <br>
                % end
            %   end
            </td>
            % end
            </div>
        </tr>

    </tbody>
</table>
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