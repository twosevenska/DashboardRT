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
                        <a href="/ticket/{{ticket['id']}}/action/back?o={{username_id}}&email={{email}}">&lt;</a>
                        % end
                        % if ticket['kanban_actions']['interrupted']:
                        <a href="/ticket/{{ticket['id']}}/action/interrupted?o={{username_id}}&email={{email}}">/</a>
                        % end
                        % if ticket['kanban_actions']['increase_priority']:
                        <a href="/ticket/{{ticket['id']}}/action/increase_priority?o={{username_id}}&email={{email}}">^</a>
                        % end
                    </td>
                    <td>
                        <a href="https://suporte.uc.pt/Ticket/Display.html?id={{ticket['id']}}">
                            {{ticket['id']}}
                        </a>
                    </td>
                    <td>
                        <a href="https://suporte.uc.pt/Ticket/Display.html?id={{ticket['id']}}">
                            {{ticket['status']}}
                        </a>
                    </td>
                    <td>
                        <a href="https://suporte.uc.pt/Ticket/Display.html?id={{ticket['id']}}">
                            {{ticket['cf.{servico}']}}
                        </a>
                    </td>
                    <td>
                        <a href="https://suporte.uc.pt/Ticket/Display.html?id={{ticket['id']}}">
                            {{ticket['requestors']}}
                        </a>
                    </td>
                    <td>
                        <a href="https://suporte.uc.pt/Ticket/Display.html?id={{ticket['id']}}">
                            % subject = ticket['subject']
                            % if len(ticket['subject']) > max_len:
                            %   subject = ticket['subject'][:max_len]+'...'
                            % end
                            {{subject}}
                        </a>
                    </td>
                    <td>
                        <a href="https://suporte.uc.pt/Ticket/Display.html?id={{ticket['id']}}">
                            Created: {{ticket['created']}}<br>
                            Last Update: {{ticket['lastupdated']}}
                        </a>
                    </td>
                    <td>
                        % if ticket['kanban_actions']['decrease_priority']:
                        <a href="/ticket/{{ticket['id']}}/action/decrease_priority?o={{username_id}}&email={{email}}">v</a>
                        % end
                        % if ticket['kanban_actions']['stalled']:
                        <a href="/ticket/{{ticket['id']}}/action/stalled?o={{username_id}}&email={{email}}">\</a>
                        % end
                        % if ticket['kanban_actions']['forward']:
                        <a href="/ticket/{{ticket['id']}}/action/forward?o={{username_id}}&email={{email}}">&gt;</a>
                        % end
                        % if email == 'dir-inbox':
                        <a href="/ticket/{{ticket['id']}}/action/take?o={{username_id}}&email={{email}}">(take)</a>
                        %   if ticket.get('cf.{ditic-urgent}', ''):
                        <a href="/ticket/{{ticket['id']}}/action/unset_urgent?o={{username_id}}&email={{email}}" title="Make ticket not urgent">(Not Urg.)</a>
                        %   else:
                        <a href="/ticket/{{ticket['id']}}/action/set_urgent?o={{username_id}}&email={{email}}" title="Make ticket URGENT">(Urg.)</a>
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
