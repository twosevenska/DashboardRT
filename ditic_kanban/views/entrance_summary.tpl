% result = "['Date', 'Created', 'Resolved', 'Still open'],\n"
% for day in sorted(statistics):
%   if statistics[day]:
%       result += '''["%s", %s, %s, %s],\n''' % (day,
%                                              statistics[day]["created_tickets"],
%                                              statistics[day]['team']['resolved'],
%                                              statistics[day]['team']['open'])
%   else:
%       result += '["%s", 0, 0, 0],\n' % day
%   end
% end

% graph_script = """
    <script type="text/javascript"
          src="https://www.google.com/jsapi?autoload={
            'modules':[{
              'name':'visualization',
              'version':'1',
              'packages':['corechart']
            }]
          }"></script>

    <script type="text/javascript">
      google.setOnLoadCallback(drawChart);

      function drawChart() {
        var data = google.visualization.arrayToDataTable([
%s
        ]);

        var options = {
          title: 'Número de tickets',
          curveType: 'function',
          legend: { position: 'bottom' },
        };

        var chart = new google.visualization.LineChart(document.getElementById('performance'));

        chart.draw(data, options);
      }
    </script>
""" % result

% result = "['Date', 'Mean Time to Resolve', 'Time worked'],\n"
% for day in sorted(statistics):
%   if statistics[day]:
%       result += '''["%s", %s, %s],\n''' % (day,
%                                      statistics[day]['team']['mean_time_to_resolve']/60,
%                                      statistics[day]['team']['time_worked']/60)
%   else:
%       result += '["%s", 0, 0],\n' % day
%   end
% end
% graph_script += """
 <script type="text/javascript"
          src="https://www.google.com/jsapi?autoload={
            'modules':[{
              'name':'visualization',
              'version':'1',
              'packages':['corechart']
            }]
          }"></script>

    <script type="text/javascript">
      google.setOnLoadCallback(drawChart);

      function drawChart() {
        var data = google.visualization.arrayToDataTable([
%s
        ]);

        var options = {
          title: 'Tempo médio de resolução vs Tempo total trabalhado (horas)',
          curveType: 'function',
          legend: { position: 'bottom' },
        };

        var chart = new google.visualization.LineChart(document.getElementById('mean_time_to_resolve'));

        chart.draw(data, options);
      }
    </script>
""" % result

% rebase('skin', meta_refresh=300)

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
                      <audio autoplay="autoplay">
                         <source src="/static/alert1.mp3" />
                      </audio>
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
                    <td align="center">R2RT</td>
                    <td align="center">DONE</td>
                </tr>
                % totals = { status: 0 for status in ['new', 'open', 'stalled', 'rejected', 'resolved']}
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
                    %   for status in ['new', 'open', 'stalled', 'rejected', 'resolved']:
                    <td>{{summary[email][status]}}</td>
                    %       totals[status] += summary[email][status]
                    % end
                </tr>
                % end
                <tr>
                    <td><strong>Totais</strong></td>
                    %   for status in ['new', 'open', 'stalled', 'rejected', 'resolved']:
                    <td><strong>{{totals[status]}}</strong></td>
                    % end
                </tr>
            </table>
        </td>
    </tr>
</table>

<table border="0">
    <td>
        <div id="performance" style="width: 400px; height: 400px"></div>
    </td>
    <td>
        <div id="mean_time_to_resolve" style="width: 400px; height: 400px"></div>
    </td>
</table>


