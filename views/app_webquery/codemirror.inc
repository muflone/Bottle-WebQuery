% if INCLUDE == 'stylesheets':
    <link type="text/css" rel="stylesheet" href="static/css/codemirror.css">
    <link type="text/css" rel="stylesheet" href="static/codemirror-5.6/lib/codemirror.css" />
    <link type="text/css" rel="stylesheet" href="static/codemirror-5.6/addon/dialog/dialog.css" />
    <link type="text/css" rel="stylesheet" href="static/codemirror-5.6/addon/hint/show-hint.css" />
    <link type="text/css" rel="stylesheet" href="static/css/codemirror-theme-custom.css">
    <link type="text/css" rel="stylesheet" href="static/css/codemirror-fullscreen-full-width.css">
% elif INCLUDE == 'scripts':
    <script src="static/codemirror-5.6/lib/codemirror.js"></script>
    <script src="static/codemirror-5.6/addon/hint/show-hint.js"></script>
    <script src="static/codemirror-5.6/addon/hint/sql-hint.js"></script>
    <script src="static/js/codemirror-sql-custom.js"></script>
    <script src="static/codemirror-5.6/addon/display/placeholder.js"></script>
    <script src="static/codemirror-5.6/addon/selection/active-line.js"></script>
    <script src="static/codemirror-5.6/addon/edit/closebrackets.js"></script>
    <script src="static/codemirror-5.6/addon/edit/matchbrackets.js"></script>
    <script src="static/codemirror-5.6/addon/display/fullscreen.js"></script>
    <script src="static/codemirror-5.6/addon/dialog/dialog.js"></script>
    <script src="static/codemirror-5.6/addon/search/search.js"></script>
    <script src="static/codemirror-5.6/addon/search/searchcursor.js"></script>
% elif INCLUDE == 'body':
    <script>
    window.onload = function() {
      window.editor = CodeMirror.fromTextArea(document.getElementById('codemirror'), {
        mode: 'text/x-sql-custom',
        extraKeys: {
          "Ctrl-Space": "autocomplete",
          "F11": function(cm) {
            cm.setOption("fullScreen", !cm.getOption("fullScreen"));
          },
          "Esc": function(cm) {
            if (cm.getOption("fullScreen")) cm.setOption("fullScreen", false);
          },
          "Ctrl-F": "find",
          "Ctrl-G": "findNext",
          "Shift-Ctrl-G": "findPrevious",
          "Ctrl-R": "replace",
          "Shift-Ctrl-R": "replaceAll",
        },
        theme: "custom",
        lineWrapping: false,
        lineNumbers: true,
        styleActiveLine: true,
        autoCloseBrackets: true,
        matchBrackets : true,
      });
    };
    </script>
% end
