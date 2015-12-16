<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <meta name="description" content="Dashboard RT - Logic Box">
    <meta name="author" content="Alexandre Vieira, André Martinez, Eduardo Pereira, Gloriya Gostyaeva, Gonçalo Barroso, Roberto Cunha">

    <title>Logic Box</title>

    <link href="css/bootstrap.min.css" rel="stylesheet">
    <link href="css/cover.css" rel="stylesheet">
    <script src="js/ie-emulation-modes-warning.js"></script>


  </head>

  <body>

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
                  <input id="password" type="password" class="forma-rect" placeholder="Password" aria-describedby="basic-addon1">
                </div>
              </div>
            <button type="button" onclick='onLoginClick()' class="btn btn-default">LOGIN</button>
            </center>

          </div>

        </div>

      </div>

    </div>

    <script src="https://ajax.googleapis.com/ajax/libs/jquery/2.1.4/jquery.min.js"></script>
    <script src="js/bootstrap.min.js"></script>
    <script src="js/ie10-viewport-bug-workaround.js"></script>
    <script>
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
                    console.log("complete.testStatus=" + textStatus);
                },
                success: function (data, textStatus) {
                    console.log("success.testStatus=" + textStatus);
                    window.location.href = "/";
                },
                statusCode: {
                    401: function() {
                        alert("THOU SHALL NOT PASS");
                    }
                }
            });
        }
    </script>
  </body>
</html>
