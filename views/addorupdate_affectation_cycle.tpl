%rebase layout title='Affectation de cycle'

<h1>Affectation de cycle</h1>

%def render_field(field, desc=None, **kwargs):
<div class="row">
    <div class="small-3 columns">
        <dt>{{!field.label}}</dt>
    </div>
    <div class="small-9 columns">
        <dd>{{!field(**kwargs)}}
            %if desc:
            {{!desc}}
            %end
            %if field.errors:
            <div class="alert callout">
                <ul class=errors>
                    %for error in field.errors:
                    <li>{{ error }}</li>
                    %end
                </ul>
            </div>
            %end
        </dd>
    </div>
</div>
%end


<form method="POST">
    <dl>
        %render_field(form.debut)
        %render_field(form.fin)
        %render_field(form.cycle_id)
    </dl>

    <div class="row">
        <div class="small-3 columns"></div>
        <div class="small-6 columns">&nbsp;
        <center>
            <button type="submit" class="success button">Enregistrer</button>
        </center>
        </div>
       <div class="small-3 columns">&nbsp;
            <center><a href={{app.get_url('affectation_cycles')}} class="button">Annuler</a></center>
        </div>

    </div>
</form>
