%rebase layout title='Cycles'
<h1>Cycles</h1>

<table>
    <thead>
    <tr>
        <th>Libellé</th>
        <th width="150">Cycles</th>
        <th></th>
    </tr>
    </thead>
    <tbody>
    %for cycle in cycles:
    <tr>
        <td>
            <a href="{{app.get_url('update_cycle', id=cycle.cycle_id)}}"> {{cycle.libelle}}</a>
        </td>
        <td>
            %for contenu in cycle.plannings:
            <div>
                <a href="{{app.get_url('update_planning', id=contenu.planning.planning_id)}}">
                    {{contenu.planning.libelle}}</a>
            </div>
            %end
        </td>
        <td>
            <a href="{{app.get_url('delete_cycle', cycle_id=cycle.cycle_id)}}" class="alert button">Delete</a>
        </td>
    </tr>
    %end
    </tbody>

</table>


<a href="{{app.get_url('new_cycle')}}" class="button">Ajouter...</a>

