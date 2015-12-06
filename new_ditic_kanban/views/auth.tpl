% rebase('skin')

% if message != '':
Result: <strong>{{message}}</strong>
% end

<form action="/auth" method="post">
    <table>
        <tr>
            <td>
                Username:
            </td>
            <td>
                <input name="username" type="text" value="{{get('username', '')}}"/>
            </td>
        </tr>
        <tr>
            <td>
                Password:
            </td>
            <td>
                <input name="password" type="password" value="{{get('password', '')}}" />
            </td>
        </tr>
        <tr>
            <td>
                <input value="Login" type="submit" />
            </td>
        </tr>
    </table>
</form>