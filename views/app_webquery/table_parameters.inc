% if PARAMETERS:
    <form method="get">
      <input type="hidden" name="uuid" value="{{ ARGS['UUID'] }}">
      <table id="parameters">
        <caption>Query parameters</caption>
        <tbody>
  % for PARAM_NAME in PARAMETERS.keys():
          <tr>
            <th>{{PARAM_NAME }}</th>
    % if type(PARAMETERS[PARAM_NAME]) is list:
            <td><select name="{{ PARAM_NAME }}">
      % if type(PARAMETERS[PARAM_NAME][0]) is list:
        % include('%s/select_options_from_data.inc' % MODULE, DATA_ROWS=False, FIELD_ID=0, FIELD_VALUE=1, SELECTED=ARGS[PARAM_NAME], DATA=PARAMETERS[PARAM_NAME])
      % else:
        % include('%s/select_options_from_data.inc' % MODULE, DATA_ROWS=False, FIELD_ID=0, FIELD_VALUE=1, SELECTED=ARGS[PARAM_NAME], DATA=[(value, value) for value in PARAMETERS[PARAM_NAME]])
      % end
            </select></td>
    % elif type(PARAMETERS[PARAM_NAME]) is str:
            <td><input type="text" name="{{ PARAM_NAME }}" value="{{ ARGS[PARAM_NAME] }}"></td>
    % elif type(PARAMETERS[PARAM_NAME]) is datetime.date:
            <td><input type="text" name="{{ PARAM_NAME }}" value="{{ ARGS[PARAM_NAME] }}" id="{{ PARAM_NAME.replace(' ', '_') }}"></td>
            <script>
              $( "#{{ PARAM_NAME.replace(' ', '_') }}" ).datepicker({
                dateFormat: "yy-mm-dd",
              });
            </script>
    % end
          </tr>
  % end
        </tbody>
        <tfoot>
          <tr>
            <td colspan="2">
              <input type="submit" name="confirm" value="Confirm">
              <input type="submit" name="format" value="CSV">
            </td>
          </tr>
        </tfoot>
      </table>
    </form>
% end
