%rebase layout title='Affectation de cycles'
<h1>Affectation de cycles</h1>

<table>
    <thead>
    <tr>
        <th width="150">Date de début</th>
        <th width="150">Date de fin</th>
        <th>Cycle</th>
        <th></th>
    </tr>
    </thead>
    <tbody>
    %for affectationcycle in affectation_cycles:
    <tr>
        <td>
            <a href="{{app.get_url('update_affectation_cycle', id=affectationcycle.affectation_id)}}"> {{affectationcycle.debut}}</a>
        </td>
        <td>
            <a href="{{app.get_url('update_affectation_cycle', id=affectationcycle.affectation_id)}}"> {{affectationcycle.fin}}</a>
        </td>
        <td>
            <a href="{{app.get_url('update_cycle', id=affectationcycle.cycle.cycle_id)}}"> {{affectationcycle.cycle.libelle}}</a>
        </td>
        <td>
            <a href="{{app.get_url('delete_affectation_cycle', id=affectationcycle.affectation_id)}}" class="alert button">Delete</a>
        </td>
    </tr>
    %end
    </tbody>

</table>


<a href="{{app.get_url('new_affectation_cycle')}}" class="button">Ajouter...</a>

