<form action="/search?o={{get('username_id', '')}}" method="post">
    Search: <input name="search" type="search">
</form>

<p>
<b>Create quick ticket:</b>
</br>
Subject: <input id="sub" type="text" placeholder="My sub1">
Text: <input id="text" type="text" placeholder="My text1">
<button onclick="createButton()">create</button>
</p>

% include('summary')
% max_len = 30

<p>
    <strong>Detail of email:</strong> {{email}} (<a href="/closed/{{email}}?o={{username_id}}">show closed tickets</a>)
</p>

% action_result = get('action_result', '')
% if action_result:
<p>
    <strong>Action:</strong> <i>{{action_result}}</i>
</p>
% end

<table border="1" width="100%">
	<tbody>
    <tr>
        <td align="center">
            <strong>IN</strong><br>
            % status = 'new'
            % if status in number_tickets_per_status:
                <strong>{{number_tickets_per_status[status]}}</strong>
            % end
            % if status in email_limit:
                (max: {{email_limit[status]}})
            % end
        </td>
        <td align="center">
            <strong>ACTIVE</strong><br>
            % status = 'open'
            % if status in number_tickets_per_status:
                <strong>{{number_tickets_per_status[status]}}</strong>
            % end
            % if status in email_limit:
                (max: {{email_limit[status]}})
            % end
        </td>

        <td align="center">
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
                Subject: {{ticket['subject']}}" href="https://suporte.uc.pt/Ticket/Display.html?id={{ticket['id']}}">
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
        <td align="center">
            <strong>Stalled</strong><br>
            % status = 'stalled'
            % if status in number_tickets_per_status:
                <strong>{{number_tickets_per_status[status]}}</strong>
            % end
            % if status in email_limit:
                (max: {{email_limit[status]}})
            % end
        </td>
    </tr>
    <tr>
        % for status in ['stalled']:

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
                Subject: {{ticket['subject']}}" href="http://domo-kun.noip.me/rt/Ticket/Display.html?id={{ticket['id']}}">
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

<p>
    Time to execute: {{time_spent}}
</p>

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


