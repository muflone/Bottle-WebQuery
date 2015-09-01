% for require in VALUES['REQUIRES']:
  % if require == 'jquery':
    % include('%s/jquery.inc' % MODULE, INCLUDE='scripts')
  % elif require == 'jquery-ui':
    % include('%s/jquery.inc' % MODULE, INCLUDE='ui')
  % end
% end
