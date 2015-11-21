<form action="/search?o={{get('username_id', '')}}" method="post">
    Search: <input name="search" type="search">
</form>

% include('summary')
% max_len = 80

<p>
    <strong>{{email.upper()}}</strong><br>
    <strong># Tickets:</strong> <i>{{number_tickets_per_status[email]}}</i>
</p>

% action_result = get('action_result', '')
% if action_result:
<p>
    <strong>Action:</strong> <i>{{action_result}}</i>
</p>
% end

<table border="1" width="100%">
    % for priority in sorted(tickets, reverse=True):
    <tr>
        <td valign="top">
            <strong>{{priority}}</strong>
        </td>
        <td valign="top">
            <table border="0">
           % for ticket in sorted(tickets[priority], reverse=True):
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
                        %   if ticket.get('cf.{ditic-urgent}', ''):
							<button onclick="actionButton({{ticket['id']}}, 'unsetUrgent')" title="Make ticket not urgent">Not Urgent</button>
                        %   else:
							<button onclick="actionButton({{ticket['id']}}, 'setUrgent')" title="Make ticket Urgent">Urgent</button>
                        %   end
                        % end
                    </td>
                </tr>
            % end
            </table>
        </td>
    </tr>
    % end
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
        }else if(action==='take'){
            strReq = takeButton(ticketId, ticketStatus);
        }else if(action==='setUrgent'){
            strReq = setUrgentButton(ticketId, ticketStatus);
        }else if(action==='unsetUrgent'){
            strReq = unsetUrgentButton(ticketId, ticketStatus);
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
	function takeButton(ticketId){
        return '/ticket/'+ticketId+'/action/take?o={{username_id}}&email={{email}}';
    }
	function unsetUrgentButton(ticketId){
        return '/ticket/'+ticketId+'/action/unset_urgent?o={{username_id}}&email={{email}}';
    }
	function setUrgentButton(ticketId){
        return '/ticket/'+ticketId+'/action/set_urgent?o={{username_id}}&email={{email}}';
    }
</script>