%include('navigator')

    <!--
    SIDEBAR
    -->
    <nav class="main-menu">
      <div class="sidebar fa fa-home fa-2x">
          <div id="title" style="color: white"><h2>Dir-Inbox</h2></div>
            <div id="chatlist" class="mousescroll">
               <ul style="color: white">
                </ul>
              </div>
        </div>
    </nav>
    <!--
    TABLES
    -->
    <div class="jumbotron">
      <div class="container">
        <!-- Row for Titles -->
        <div class="row">
          <h2 class="col-md-3 stalled-margins">Stalled</h2>
          <h2 class="col-md-3 in-margins">In</h2>
          <h2 class="col-md-3 active-margins">Active</h2>
          <h2 class="col-md-3 done-margins">Done</h2>
        </div>
        <!-- Row for ticket tables -->
        <div class="row">
          <div class="stalled">
            <div id="chatlist" class="col-md-3 mousescroll">
              <ul>
                <li>  
                  <a href="#" class="list-group-item active">
                    <h4 class="list-group-item-heading">123</h4>
                    <p class="list-group-item-text">iiiiiiiiii</p>
                  </a>
                </li>
              </ul>
            </div>
          </div>
          <div class="in">
            <div id="chatlist" class="col-md-3 mousescroll">
              <ul>
              </ul>
           </div>
         </div>
         <div class="active">
            <div id="chatlist" class="col-md-3 mousescroll">
              <ul>
              </ul>
            </div>
          </div>
          <div class="division">
            <div class="col-md-1">
              <img src="static/img/division_done.jpg" class="featurette-image img-responsive down" alt="me">
            </div>
          </div>

          <div class="done">
            <div id="chatlist" class="col-md-2 mousescroll">
              <ul>
              </ul>
            </div>
          </div> <!-- done -->
        </div><!-- row -->
      </div><!-- container -->
    </div><!-- jumbotron -->

<!-- ____________________________________________________________________________________ -->
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/2.1.4/jquery.min.js"></script>
    <script src="static/js/bootstrap.min.js"></script>
    <script src="static/js/holder.min.js"></script>
    <script src="static/js/ie10-viewport-bug-workaround.js"></script>
    <script src="static/js/ie-emulation-modes-warning.js"></script>
    <script>
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
    </script>

