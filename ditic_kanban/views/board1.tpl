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

<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="description" content="Dashboard RT - Logic Box">
    <meta name="author" content="Alexandre Vieira, André Martinez, Eduardo Pereira, Gloriya Gostyaeva, Gonçalo Barroso, Roberto Cunha">

    <title>DITIC Kanban</title>

    <link href="static/res/css/bootstrap-theme.min.css" rel="stylesheet">
    <link href="static/res/css/bootstrap.min.css" rel="stylesheet">
    <script src="static/res/js/ie-emulation-modes-warning.js"></script>
    % graph_script = get('graph_script', '')
    % if graph_script:
    {{!graph_script}}
    % end
  </head>

<img class="img-responsive" src="/static/img/background.png" style="position:fixed;top:0px;left:0px;width: 100%;z-index:-1;" />
    <!-- FIXED NAVBAR
    -->
    <nav class="navbar navbar-inverse navbar-fixed-top">
      <div class="navbar-collapse collapse">
        <ul class="nav navbar-nav navbar-left">
          <a class="navbar-brand" href='/board'>Board</a>
          <a class="navbar-brand" href="/income">Income</a>
          <a class="navbar-brand" id="tickets" href="/detail">My Tickets</a>
        </ul>
        <!-- ADMIN -->
          <ul class="nav navbar-nav navbar-right">
            <li class="dropdown">
              <a href="" class="dropdown-toggle m_right" data-toggle="dropdown" role="button" aria-haspopup="true" aria-expanded="false">{{username}}<span class="caret"></span></a>
              <ul class="dropdown-menu">
                <li><a href="#">Profile</a></li>
                <li><a href="#">Preferences</a></li>
                <li><a href="" onClick="onLogoutClick()">Logout</a></li>
                <!--<li role="separator" class="divider"></li>
                <li class="dropdown-header">Nav header</li>
                <li><a href="#">Separated link</a></li>
                <li><a href="#">One more separated link</a></li>-->
              </ul>
            </li>
          </ul>
          <!-- SEARCH -->
          <form class="navbar-form navbar-right">
            <input type="text" class="form-control" placeholder="Search...">
            <button type="submit">Search</button>
          </form>
          <!-- NEW TICKET -->
          <ul class="nav navbar-nav navbar-right">
            <li class="dropdown">
              <a href="#" class="dropdown-toggle m_right" data-toggle="dropdown" role="button" aria-haspopup="true" aria-expanded="false">New ticket <span class="caret"></span></a>
              <ul class="dropdown-menu">
                <li>
                  <p>
                    <b>Create quick ticket:</b>
                    </br>
                    Subject: <input id="sub" type="text" placeholder="Subject">
                    Text: <input id="text" type="text" placeholder="Text here">
                    <!--<ul><li><a href="#">Advanced Ticket Creation</a></li></ul>-->
                    <button type="submit">create</button>
                  </p>
                </li>
              </ul>
            </li>
          </ul>
      </div>
    </nav>

<br><br><br>


<div class="col-md-8">


<div class="panel panel-default">  
<div class="panel-heading">DITIC Kanban Board </div> 
<div class="panel-body"> 

           <a href="/income">DIR</a> = 
            % # DIR
            % sum = 0
            % # we need this code because DIR can have tickets all along several status
            % for status in summary['dir']:
            %   sum += summary['dir'][status]
            % end
            {{sum}}
            <a href="/income">DIR-INBOX</a> =
         
            % # DIR-INBOX
            % sum = 0
            % # we need this code because DIR can have tickets all along several status
            % for status in summary['dir-inbox']:
            %   sum += summary['dir-inbox'][status]
            % end
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
                       <a href="http://domo-kun.noip.me/rt/Ticket/Display.html?id={{ticket_info['id']}}">
                        {{ticket_info['subject']}}
                    </a>
                    % if username:
                    <a href="/ticket/{{ticket_info['id']}}/action/take">(take)</a>
                    % end
                    % end
                </td>
            </table>
            <br>
            % end
            {{sum}}
        </td>
  </div>  
  <table class="table"> 
    <thead> 
      <tr> 
        <th>user</th> 
        <th>IN</th> 
        <th>ACTIVE</th> 
        <th>STALLED</th> 
        <th>DONE</th>  
      </tr> 
    </thead> 
      % totals = { status: 0 for status in ['new', 'open', 'stalled', 'resolved']}
      % for email in sorted(summary):
      %   if email.startswith('dir'):
      %       continue
      %   end
      %   user = email
      %   if  email != 'unknown':
      %       user = alias[email]
      %   end
    <tbody> 
       <tr>
                    <td><a href="/detail">{{user}}</a></td>
                    %   for status in ['new', 'open', 'stalled', 'resolved']:
                    <td>{{summary[email][status]}}</td>
                    %       totals[status] += summary[email][status]
                    % end
                </tr>
                % end
     <tr>
                    <td><strong>Totais</strong></td>
                    %   for status in ['new', 'open', 'stalled', 'resolved']:
                    <td><strong>{{totals[status]}}</strong></td>
                    % end
                </tr>
   </tbody> 
 </table> 

 </div>
           
</div>
</div>
<div class="col-md-4">
    <div id="performance" style="width: 600px; height: 400px"></div>
    <br>
    <div id="mean_time_to_resolve" style="width: 600px; height: 400px"></div>
</div>


    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js"></script>
    
    <script src="static/res/js/holder.min.js"></script>
    <script src="static/res/js/ie10-viewport-bug-workaround.js"></script>
  </body>
</html>

