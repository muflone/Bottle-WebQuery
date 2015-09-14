% if INCLUDE == 'stylesheets':
    <link type="text/css" rel="stylesheet" href="static/css/tablesorter.css">
% elif INCLUDE == 'scripts':
    <script type="text/javascript" src="static/tablesorter-2.23.3/jquery.tablesorter.min.js"></script>
    <script type="text/javascript" src="static/tablesorter-2.23.3/jquery.tablesorter.widgets.min.js"></script>
    <script>
    $(function(){
      $('.data')
        .tablesorter({
          sortReset: true,
          widgets: [
  % if 'resizable' in OPTIONS:
            'resizable',
  % end
          ],
          widgetOptions: {
            storage_useSessionStorage: true,  /* Save to session */
  % if 'resizable' in OPTIONS:
            resizable_addLastColumn: false,   /* Resize freely */
            resizable: false,                 /* Don't restore columns width */
  % end
          },
        })
      ;
    });
    </script>
% elif INCLUDE == 'body':
  % pass
% end
