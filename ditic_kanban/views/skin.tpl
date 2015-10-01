<!DOCTYPE html>
<html lang="en">
<head>
    % meta_refresh = get('meta_refresh', 0)
    {{!'<meta http-equiv="refresh" content="%s">' % meta_refresh if meta_refresh else ''}}
    <meta charset="UTF-8">
    <title>{{title}}</title>
    % graph_script = get('graph_script', '')
    % if graph_script:
    {{!graph_script}}
    % end
</head>
<body>
% username_id = get('username_id', '')
<a href="/?o={{username_id}}">home</a>
{{!base}}
</body>
</html>