<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <meta name="description" content="Dashboard RT - Logic Box">
    <meta name="author" content="Alexandre Vieira, André Martinez, Eduardo Pereira, Gloriya Gostyaeva, Gonçalo Barroso, Roberto Cunha">

    <title>DITIC Kanban</title>

    <link href="static/res/css/bootstrap.min.css" rel="stylesheet">
    <link href="static/res/css/cover.css" rel="stylesheet">
  </head>

  <body background="static/res/img/background.png" style="background-repeat: repeat;">
    <div class="site-wrapper">
      <div class="site-wrapper-inner">
        <div class="cover-container">
          <div class="inner cover">
            <center>
              <div class="input">
                <div class="input1">
                  <input id="username"  type="text" class="forma-rect" placeholder="User" aria-describedby="basic-addon1">
                </div>
                <br>
                <div class="input2">
                  <input onkeypress="onKeyPress(this, event)" id="password" type="password" class="forma-rect" placeholder="Password" aria-describedby="basic-addon1">
                </div>
              </div>
            <button type="button" onclick='onLoginClick()' class="btn btn-default">LOGIN</button>
            </center>
          </div>
        </div>
      </div>
    </div>

<!-- ____________________________________________________________________________________ -->
    <script src="static/res/js/jquery/jquery-1.11.3.min.js"></script>">
    <script src="static/res/js/bootstrap.min.js"></script>
    <script src="static/res/js/ie10-viewport-bug-workaround.js"></script>
    <script src="static/res/js/ie-emulation-modes-warning.js"></script>
    <script>
        function onKeyPress(thisArg, theEvent) {
          if (theEvent.keyCode == 13) {
            onLoginClick();
          }
        }

        function onLoginClick() {
            data = {
                        username: document.getElementById('username').value,
                        password: document.getElementById('password').value
                   };

            url = "/auth";

            $.ajax({
                type: "POST",
                url: url,
                data: JSON.stringify(data),
                contentType: "application/json",
                complete: function (data, textStatus) {
                    console.log("complete.statusCode=" + data.statusCode);
                },
                success: function (data, textStatus) {
                    window.location.href = "/detail";
                },
                statusCode: {
                    401: function() {
                        alert("THOU SHALL NOT PASS");
                      },
                    500: function() {
                        window.location.reload();
                      }
                }
            });
        }
    </script>
  </body>
</html>
