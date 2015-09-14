% if INCLUDE == 'stylesheets':
    <link type="text/css" rel="stylesheet" href="static/css/tablesorter.css">
% elif INCLUDE == 'scripts':
    <script type="text/javascript" src="static/tablesorter-2.23.3/js/jquery.tablesorter.min.js"></script>
    <script type="text/javascript" src="static/tablesorter-2.23.3/js/jquery.tablesorter.widgets.min.js"></script>
    <script>
    $(function(){
      $('.data').tablesorter({
        sortReset: true,
        widgets: [ 'resizable' ],
        widgetOptions: {
          storage_useSessionStorage: true,  /* Save to session */
          resizable_addLastColumn: false,   /* Resize freely */
          resizable: false,                 /* Don't restore columns width */
        },
      });
    });
    </script>
% elif INCLUDE == 'body':
  % pass
% end
