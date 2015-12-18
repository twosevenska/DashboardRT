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
<body>
<img class="img-responsive" src="/static/res/img/background.png" style="position:fixed;top:0px;left:0px;width: 100%;z-index:-1;" />
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
            <button type="submit" class="btn btn-primary">Search</button>
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
                    <button type="submit" class="btn btn-primary" onclick="onCreateClick()">Create</button>
                  </p>
                </li>
              </ul>
            </li>
          </ul>
      </div>
    </nav>

<br><br><br>br><br>


<div class="col-md-8">


<div class="panel panel-default">  
<div class="panel-heading">DITIC Kanban Board </div> 
<div class="panel-body">
    <div class="col-md-4">
      <p><a href="/income">DIR</a></h4> = 
        % # DIR
        % sum = 0
        % # we need this code because DIR can have tickets all along several status
        % for status in summary['dir']:
        %   sum += summary['dir'][status]
        % end
        {{sum}}</p>
       <p><a href="/income">DIR-INBOX</a> = 
        % # DIR-INBOX
        % sum = 0
        % # we need this code because DIR can have tickets all along several status
        % for status in summary['dir-inbox']:
        %   sum += summary['dir-inbox'][status]
        % end
        {{sum}}</p>
    </div>
    <div class="col-md-8">
          % urgent = get('urgent', '')
          % if urgent:
              <audio autoplay="autoplay">
                <source src="/static/alert1.mp3" />
              </audio>
              <div class="panel panel-danger">
                <div class="panel-heading">
                <h3 class="panel-title" align="center">URGENT</h3>
                </div>
                <div class="panel-body" align="center">
                  
                  % for ticket_info in urgent:
                  <div class="row">
                    <div class="btn-group" role="group">
                    <button type="button" onclick="clickTicket({{ticket_info['id']}})" class="btn btn-default">
                      {{ticket_info['subject']}}
                    </button>
                    % if username:
                     <button type="button" onclick="actionButton({{ticket_info['id']}}, 'take')" class="btn btn-default">
                      <span class="glyphicon glyphicon-hand-right" aria-hidden="true"></span>
                     </button>
                    % end
                    </div>
                    % end
                    </div>
                </div>
              </div>
          </div>
      </div>
  <br>  
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
<script>
    function actionButton(ticketId, action, ticketStatus){
        
        $.ajax({
            type: "PUT",
            url: "/ticket/"+ticketId+"/action/"+action,
            data: JSON.stringify({'ticketmail':ticketStatus}),
            contentType: "application/json",
            success: function (data) {
                window.location.reload();
            },
            statusCode: {
                500: function() {
                    window.location.reload();
                    alert('Unable to resolve action');
                  }
            }
        });
    }

    function onCreateClick(){
        data = {
                    subject: document.getElementById('sub').value,
                    text: document.getElementById('text').value
                };
        $.ajax({
                type: "POST",
                url: "/ticket",
                data: JSON.stringify(data),
                contentType: "application/json",
                success: function (data) {
                    window.location.reload();
                },
                statusCode: {
                    500: function() {
                        window.location.reload();
                        alert('Unable to create the ticket');
                      }
                }
            });
    }

    function onLogoutClick() {
            $.ajax({
                type: "DELETE",
                url: "/auth",
                data: "{}",
                contentType: "application/json",
                complete: function (data, textStatus) {
                    console.log("complete.statusCode=" + data.statusCode);
                },
                success: function (data) {
                    window.location.href = "/login";
                }
            });
        }
    function clickTicket(ticketId) {
            $.ajax({
                type: "GET",
                url: "/ticket/"+ticketId,
                complete: function (data, textStatus) {
                    console.log("complete.statusCode=" + data.statusCode);
                },
                success: function (data) {
                    window.location.href = "/ticket/"+ticketId;
                }
            });
        }
</script>
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js"></script>
    
    <script src="/static/res/js/bootstrap.min.js"></script>
    <script src="static/res/js/holder.min.js"></script>
    <script src="static/res/js/ie10-viewport-bug-workaround.js"></script>
  </body>
</html>

