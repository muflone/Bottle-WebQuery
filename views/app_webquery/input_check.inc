% if TITLE:
<label>\\
% end
% selected_value = SELECTED.encode('utf-8') if type(SELECTED) is unicode else str(SELECTED)
<input type="checkbox" name="{{ NAME }}" value="{{ VALUE }}"\\
% if selected_value == VALUE:
 checked="true"\\
% end
>\\
% if TITLE:
{{ TITLE }}</label>\\
% end
