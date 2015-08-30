% if INCLUDE == 'stylesheets':
    <link type="text/css" rel="stylesheet" href="static/fancytree-2.11.0/skin-lion/ui.fancytree.min.css">
% elif INCLUDE == 'scripts':
    <script type="text/javascript" src="static/fancytree-2.11.0/jquery.fancytree-all.min.js"></script>
% elif INCLUDE == 'scripts-table':
    <script type="text/javascript" src="static/fancytree-2.11.0/jquery.fancytree.table.js"></script>
% elif INCLUDE == 'body':
  % pass
% end
