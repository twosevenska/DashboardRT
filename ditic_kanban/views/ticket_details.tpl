
% rebase('skin')

<p>
    % username = get('username', '')
    % if username:
    <strong>Authenticated as: {{username}}</strong>
    % end
</p>

<h1>#{{ticket_id}}: {{subject}}</h1>

<h2>The Basics</h2>
<b>id:</b> {{ticket_id}}<br>
<b>Status:</b> {{status}}<br>
<b>Priority:</b> {{priority}}<br>
<b>Queue:</b> {{queue}}<br>

<h2>People</h2>
<b>Owner:</b> {{owner}}<br>
<b>Requestors:</b> {{requestors}}<br>
<b>Cc:</b> {{cc}}<br>
<b>AdminCc:</b> {{admincc}}<br>

<h2>Dates</h2>
<b>Created:</b> {{created}}<br>
<b>Starts:</b> {{starts}}<br>
<b>Started:</b> {{started}}<br>
<b>Last Contact:</b> {{told}}<br>
<b>Due:</b> {{due}}<br>
% closed = get('closed', '')
% if closed:
<b>Closed:</b> {{closed}}<br>
% end
% updated = get('updated', '')
% if updated:
<b>Updated:</b> {{updated}}<br>
% end

<p>Time to execute: {{time_spent}}</p>

<script>
</script>


