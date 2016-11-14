%rebase layout title='Plannings'

<!--
<nav aria-label="You are here:" role="navigation">
  <ul class="breadcrumbs">
    <li><a href="#">Home</a></li>
    <li><a href="#">Features</a></li>
    <li class="disabled">Gene Splicing</li>
    <li>
      <span class="show-for-sr">Current: </span> Cloning
    </li>
  </ul>
</nav>
-->


<h1>Planning Jour</h1>

<table>
    <thead>
    <tr>
        <th>Libellé</th>
        <th width="150">Heure</th>
        <th width="150">Température</th>
        <th></th>
    </tr>
    </thead>
    <tbody>
    %for planning in plannings:
    <tr>
        <td>
            <a href="{{app.get_url('update_planning', id=planning.planning_id)}}">{{planning.libelle}}</a>
        </td>
        <td>
            %for plage in planning.plages:
            <div>{{plage.heure}}</div>
            %end
        </td>
        <td>
            %for plage in planning.plages:
            <div>{{plage.temperature}}</div>
            %end
        </td>
        <td>
            <a href="{{app.get_url('delete_planning', planning_id=planning.planning_id)}}"
               class="alert button">Delete</a>
        </td>
    </tr>
    %end
    %end
    </tbody>

</table>


<a href="{{app.get_url('new_planning')}}" class="button">Ajouter...</a>

