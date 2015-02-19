
$(document).ready(function(){
    $("#btn-submit-result").click(function(){
        var timezone = $('#input-timezone').val();
        var date_ints = [];
        $.each($('.date-inputs'), function( index, item ) {
            date_ints[index] = item.value;
        });
        date_ints = date_ints.join(',');

        $.ajax({
            type: "GET",
            url: "/tz",
            data: { tz_string: timezone, date_ints: date_ints}
        }).done(function(data) {
            var html_str = '<div>Timezone: ' + data.tz + '</div>';
            html_str += '<div><b> Date --  Timestamp </b></div>';
            $.each( data.dates, function( i, item ) {
                html_str += '<div> ' + i + ' -- ' + item + '</div>';
            })
            $('#panel-result').html(html_str);
        }).fail(function() {
            $('#panel-result').html("Unable to fetch timezone information" );
        });
    });

    $("#btn-add-date").click(function(){
        $(this).before($('#input-date-skeleton').html());
    });
});

