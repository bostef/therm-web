%# disp_table.tpl

<form action="/new" method="POST">

<p>The items are as follows:</p>
<table border="1">
  <tr>
    %for r in rows:
      <th>{{r}}</th>
    %end
  </tr>
    %for i in range(cases):
     <tr>
      %for r in rows:
         %if r==edit:
             <td contenteditable="true">{{rows[r][i]}}</td>
         %elif r == check:
        <td>
          % if rows[r][i] == 1:
            <input type="checkbox" name="myTextEditBox" value="1" checked="checked" />
          % else:
            <input type="checkbox" name="myTextEditBox" value="0" />
          % end
        </td>
         %else:
            <td>{{rows[r][i]}}</td>
         %end
      %end
     </tr>
    %end
</table>

 <input type="checkbox" name="checkbox" value="1" checked="checked" />
    <input type="checkbox" name="checkbox" value="1" checked="checked" />
    <input type="submit" name="add" value="Save">
</form>