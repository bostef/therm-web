%rebase layout title='toto', parent_url=app.get_url('cycles')

<h1>Cycle</h1>

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
        %render_field(form.libelle, '(4-20 characters)</p>')
        %for planning in form.plannings:
        %render_field(planning.planning_id)
        %end
    </dl>

    <!-- Buttons (actions) -->
    <button type="submit" class="success button">Enregistrer</button>
</form>
