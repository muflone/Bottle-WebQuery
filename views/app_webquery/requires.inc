% for require in VALUES['REQUIRES']:
  % if require == 'jquery':
    % include('%s/jquery.inc' % MODULE, INCLUDE='scripts')
  % elif require == 'jquery-ui':
    % include('%s/jquery.inc' % MODULE, INCLUDE='ui')
  % elif require == 'tablesorter':
    % include('%s/tablesorter.inc' % MODULE, INCLUDE='stylesheets')
    % include('%s/tablesorter.inc' % MODULE, INCLUDE='scripts')
  % end
% end
