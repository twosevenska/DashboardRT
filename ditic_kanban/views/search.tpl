<form action="/search?o={{get('username_id', '')}}" method="post">
    Search: <input name="search" type="search">
</form>

% include('summary')
% max_len = 80

<p>
    <strong>Searching for (last 90 days): </strong><i>{{email}}</i><br>
    <strong># Tickets:</strong> <i>{{number_tickets}}</i>
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
