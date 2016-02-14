<!DOCTYPE html>
<html>
  <head>
    <title>User login</title>
    <link type="text/css" rel="stylesheet" href="static/css/styles.css">
    <link type="text/css" rel="stylesheet" href="static/css/login.css">
  </head>

  <body>
    <div class="container">
      <section id="content">
% if ACTION == 'logout':
        <h3>Disconnection successfull.</h3>
% end
        <form action="login" method="POST">
          <h1>Login</h1>
          <div>
            <input placeholder="User" required="" id="username" name="username" type="text" autofocus>
          </div>
          <div>
            <input placeholder="Password" required="" id="password" name="password" type="password">
          </div>
% if INVALID:
          <h4>Wrong username or password.</h4>
% end
          <div>
            <input type="hidden" name="forward" value="{{ FORWARD }}">
            <input value="Login" type="submit">
          </div>
        </form>
      </section>
    </div>
  </body>
</html>
