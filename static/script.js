$(document).ready(function () {

    $('#pkrc').change(function () {

        var selected = $('#pkrc').find(":selected").text();
        var sukpafemale = $('#female' + selected).text();

        $('#a_female').val(sukpafemale);
    });
});