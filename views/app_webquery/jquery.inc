% if INCLUDE == 'stylesheets':
  % pass
% elif INCLUDE == 'scripts':
    <script type="text/javascript" src="static/jquery/jquery-1.11.3.min.js"></script>
% elif INCLUDE == 'ui':
    <link type="text/css" rel="stylesheet" href="static/jquery/jquery-ui-1.11.4.min.css">
    <link type="text/css" rel="stylesheet" href="static/jquery/jquery-ui.theme-1.11.4.min.css">
    <script type="text/javascript" src="static/jquery/jquery-ui-1.11.4.min.js"></script>
% elif INCLUDE == 'body':
  % pass
% end
