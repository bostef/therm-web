%rebase layout title=None

<h1 xmlns="http://www.w3.org/1999/html">Planning Jour</h1>

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


%def render_field_col(field, desc=None, **kwargs):
<div class="small-3 columns">
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
%end


<form method="POST">
    <dl>
        %render_field(form.libelle)
        <div class="row">
            <div class="small-3 columns">&nbsp;</div>
            <div class="small-3 columns">
                <center>Heure</center>
            </div>
            <div class="small-3 columns">
                <center>Température</center>
            </div>
            <div class="small-3 columns"></div>
        </div>

        %for plage in form.plages:
        <div class="row">
            <div class="small-3 columns">&nbsp;</div>
            %render_field_col(plage.heure)
            %render_field_col(plage.temperature)
            <div class="small-3 columns"></div>
        </div>
        %end
    </dl>

    <div class="row">
        <div class="small-3 columns">&nbsp;</div>
        <div class="small-3 columns">&nbsp;
            <center>
                <!-- Buttons (actions) -->
                <button type="submit" class="success button">Enregistrer</button>
            </center>
        </div>
        <div class="small-3 columns">&nbsp;
            <center>
                <a href={{app.get_url('plannings')}} class="button">Annuler</a></center>
        </div>
        <div class="small-3 columns">&nbsp;</div>

</form>


