% rebase('skin')

<p>
    % username = get('username', '')
    % if username:
    <strong>Authenticated as: {{username}}</strong>
    % end
</p>

<table border="1">
    <tr>
        <td align="center"><a href="/detail/dir?o={{username_id}}">DIR</a></td>
        <td align="center"><a href="/detail/dir-inbox?o={{username_id}}">DIR-INBOX</a></td>
        <td align="center">DITIC Kanban Board</td>
    </tr>
    <tr>
        % # DIR
        % sum = 0
        % # we need this code because DIR can have tickets all along several status
        % for status in summary['dir']:
        %   sum += summary['dir'][status]
        % end
        <td align="center" valign="top">{{sum}}</td>

        % # DIR-INBOX
        % sum = 0
        % # we need this code because DIR can have tickets all along several status
        % for status in summary['dir-inbox']:
        %   sum += summary['dir-inbox'][status]
        % end
        <td align="center" valign="top">
            % urgent = get('urgent', '')
            % if urgent:
            <table border="1">
                <td align="center">
                    URGENT<br>
                    <br>
                    % for ticket_info in urgent:
                        <a href="https://suporte.uc.pt/Ticket/Display.html?id={{ticket_info['id']}}">
                            {{ticket_info['subject']}}
                        </a>
                        % if username:
                        <a href="/ticket/{{ticket_info['id']}}/action/take?o={{username_id}}&email={{email}}">(take)</a>
                        % end
                    % end
                </td>
            </table>
            <br>
            % end
            {{sum}}
        </td>
        <td>
            <table border="1">
                <tr>
                    <td align="center">user</td>
                    <td align="center">IN</td>
                    <td align="center">ACTIVE</td>
                    <td align="center">STALLED</td>
                    <td align="center">DONE</td>
                </tr>
                % for email in sorted(summary):
                %   if email.startswith('dir'):
                %       continue
                %   end
                %   user = email
                %   if  email != 'unknown':
                %       user = alias[email]
                %   end
                <tr>
                    <td><a href="/detail/{{email}}?o={{username_id}}">{{user}}</a></td>
                    %   for status in ['new', 'open', 'stalled', 'resolved']:
                    <td>{{summary[email][status]}}</td>
                    % end
                </tr>
                % end
            </table>
        </td>
    </tr>
</table>