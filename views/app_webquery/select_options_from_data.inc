% selected_value = SELECTED.encode('utf-8') if type(SELECTED) is unicode else str(SELECTED)
% for record in DATA:
          <option value="{{ record.format_value(FIELD_ID) if DATA_ROWS else record[FIELD_ID] }}"\\
  % if selected_value == (record.format_value(FIELD_ID) if DATA_ROWS else printable_text_for_encoding(record[FIELD_ID], 'utf-8')):
 selected="selected"\\
  % end
>{{ record.format_value(FIELD_VALUE) if DATA_ROWS else record[FIELD_VALUE] }}</option>
% end
