% if INCLUDE == 'stylesheets':
  % pass
% elif INCLUDE == 'scripts':
    <script type="text/javascript" src="static/jquery/jquery-1.11.3.min.js"></script>
% elif INCLUDE == 'ui':
    <script type="text/javascript" src="static/jquery/jquery-ui-1.11.4.min.js"></script>
% elif INCLUDE == 'body':
  % pass
% end
