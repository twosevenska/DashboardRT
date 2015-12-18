<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <meta name="description" content="Dashboard RT - Logic Box">
    <meta name="author" content="Alexandre Vieira, André Martinez, Eduardo Pereira, Gloriya Gostyaeva, Gonçalo Barroso, Roberto Cunha">

    <title>CIUC Kanban</title>


    <link href="static/res/css/bootstrap-theme.min.css" rel="stylesheet">
    <link href="static/res/css/bootstrap.min.css" rel="stylesheet">
    <link href="static/res/css/dashboard.css" rel="stylesheet">
    <link href="static/res/css/sidebar.css" rel="stylesheet">
    <link href="static/res/css/bootstrap-table/bootstrap-table.css" rel="stylesheet">
    
    % graph_script = get('graph_script', '')
    % if graph_script:
    {{!graph_script}}
    % end
</head>
<body>
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
                        <a href="http://domo-kun.noip.me/rt/Ticket/Display.html?id={{ticket['id']}}">
                            {{ticket['id']}}
                        </a>
                    </td>
                    <td>
                        <a href="http://domo-kun.noip.me/rt/Ticket/Display.html?id={{ticket['id']}}">
                            {{ticket['status']}}
                        </a>
                    </td>
                    <td>
                        <a href="http://domo-kun.noip.me/rt/Ticket/Display.html?id={{ticket['id']}}">
                            {{ticket['cf.{servico}']}}
                        </a>
                    </td>
                    <td>
                        <a href="http://domo-kun.noip.me/rt/Ticket/Display.html?id={{ticket['id']}}">
                            {{ticket['requestors']}}
                        </a>
                    </td>
                    <td>
                        <a href="http://domo-kun.noip.me/rt/Ticket/Display.html?id={{ticket['id']}}">
                            % subject = ticket['subject']
                            % if len(ticket['subject']) > max_len:
                            %   subject = ticket['subject'][:max_len]+'...'
                            % end
                            {{subject}}
                        </a>
                    </td>
                    <td>
                        <a href="http://domo-kun.noip.me/rt/Ticket/Display.html?id={{ticket['id']}}">
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
</body>