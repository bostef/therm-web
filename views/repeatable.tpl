
%rebase layout title='Plannings'



<script src="/static/js/jquery.repeatable.js"></script>

<form method="post">
    <div class="repeatable-container"></div>
    <input type="button" value="Add Person" class="add" />
    <input type="submit" value="Submit" />
</form>

<script type="text/template" id="people">
<div class="field-group">
    <label for="firstname_{?}">First name</label>
    <input type="text" name="firstname_{?}" value="" id="firstname_{?}" />

    <label for="lastname_{?}">First name</label>
    <input type="text" name="lastname_{?}" value="" id="lastname_{?}" />

    <input type="button" class="delete" value="X" />
</div>
</script>

<script>





$(function() {
    $(".repeatable-container").repeatable({
        template: "#people",
        startWith:5
    });
});
</script>

