
% rebase('skin')

<p>
    % username = get('username', '')
    % if username:
    <strong>Authenticated as: {{username}}</strong>
    % end
</p>

<h1>
Ticket #{{ticket_id}}<br>
History item #{{item_id}}: {{description}}
</h1>

<b>Description:</b> {{description}}<br>
<b>Created:</b> {{created}}<br>
<b>Creator:</b> {{creator}}<br>
<br>
<b>Content:</b> {{content}}<br>
<br>
<b>Field:</b> {{field}}<br>
<b>New value:</b> {{newvalue}}<br>
<b>Old value:</b> {{oldvalue}}<br>
<b>Time taken:</b> {{timetaken}}<br>
<b>Type:</b> {{type}}<br>



<p>Time to execute: {{time_spent}}</p>

<script>
</script>


