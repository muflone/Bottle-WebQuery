% for require in VALUES['REQUIRES']:
  % if require == 'jquery':
    % include('%s/jquery.inc' % MODULE, INCLUDE='scripts')
  % elif require == 'jquery-ui':
    % include('%s/jquery.inc' % MODULE, INCLUDE='ui')
  % elif require == 'tablesorter':
    % tablesorter_options = ('resizable', )
    % include('%s/tablesorter.inc' % MODULE, INCLUDE='stylesheets', OPTIONS=tablesorter_options)
    % include('%s/tablesorter.inc' % MODULE, INCLUDE='scripts', OPTIONS=tablesorter_options)
  % end
% end
