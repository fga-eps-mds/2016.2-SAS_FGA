var buildings = Building.all();


function getCookie(name) {
    var cookieValue = null;

    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }

    return cookieValue;
}

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

var csrftoken = getCookie('csrftoken');
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

function breadcrumbsadd(index){
    $("#breadcrumbs ul li:eq(" + index + ")").addClass("active")

}

function back(index){
    $("#breadcrumbs ul li:eq(" + index + ")").removeClass("active")
    $("#page" + (index + 1)).hide();
    $("#page" + index).show();
}

$("#booking-buildings tbody").on("click", "td", function(){
    $(".building-selected").removeClass("building-selected");
    $(this).addClass("building-selected");
});

$("#booking-places tbody").on("click", "td", function(){
    $(".place-selected").removeClass("place-selected");
    $(this).addClass("place-selected");
});

function test(places){
    console.log("Executou");
    for(var i = 0; i < places.length; i++){
        var p = places[i];

        if(i % 3 == 0) {
            var text = "<tr>" + p.td_place() + "</tr";
            $('#booking-places tr:last').after(text);
        }

        else {
            $('#booking-places td:last').after(p.td_place());
        }
    }
}

$("#slider_begin_time").slider({
    min: 8,
    max: 22,
    step: 2,
    create: function( event, ui ) {
        $("#input_slider_begin_time").val("8:00");
    }
});
$("#slider_end_time").slider({
    min: 8,
    max: 22,
    step: 2,
    create: function( event, ui ) {
        $("#input_slider_end_time").val("8:00");
    }
});

$(document).ready(function(){
    $("#page1").show();
    $("#page2").hide();
    $("#page3").hide();
    $("#page4").hide();
    $("#page5").hide();
    $("#period-dates").hide();
    $("#id_week_days").hide();

    $(".btn-back").on("click", function() {
        var val = $(this).val();
        val = val - 1;

        back(val);
    });

    $('.datepicker1').datepicker({
			inline: true,
			useCurrent: true,
			format: '{% trans "mm/dd/yyyy" %}',
			language: '{% trans "en" %}',
			autoclose: true,
	});

    $("#input_slider_begin_time").attr("disabled", true);
    $( "#slider_begin_time" ).on( "slidechange", function( event, ui ) {
        var text = $( "#slider_begin_time" ).slider("value");
        text = text + ":00";
        $("#input_slider_begin_time").val(text);
    });

    $("#input_slider_end_time").attr("disabled", true);
    $( "#slider_end_time" ).on( "slidechange", function( event, ui ) {
        var text = $( "#slider_end_time" ).slider("value");
        text = text + ":00";
        $("#input_slider_end_time").val(text);
    });

    $('input[name=times]', '#page2').click(function(){
        if($('input[name=times]:checked', '#page2').val() == "interval"){
           $("#period-dates").show();
           $("#one-day").hide();
           $("#id_week_days").show();
        }

        else{
           $("#period-dates").hide();
           $("#one-day").show();
           $("#id_week_days").hide();
        }
    });

    breadcrumbsadd(0);
    var booking = new Booking();
    $('#booking-name-error').css('display', 'none');
    $("#next-date").click(function(){
        if(!booking.check_name_element($("#name_of_booking"))){
            return 0;
        }
        $("#page1").hide();
        $("#page2").show();
        $("#page3").hide();
        $("#page4").hide();
        $("#page5").hide();

        breadcrumbsadd(1);
    });

    $('#booking-period-error').css('display', 'none');
    $("#next-building").click(function(){
        if($('input[name=times]:checked', '#page2').val() == "interval"){
            if(!booking.check_date($("#id_start_date")) || !booking.check_date($("#id_end_date"))){
            } 
        }else{
            if(!booking.check_date($("#id_one_day_date"))){
            }
        }
        console.log($('#id_one_day_date').val());
        console.log($.datepicker.formatDate('mm/dd/yy', new Date()));
        console.log(parseInt($("#slider_end_time").slider("value")));
        console.log(parseInt($("#slider_begin_time").slider("value")));

        $("#page1").hide();
        $("#page2").hide();
        $("#page3").show();
        $("#page4").hide();
        $("#page5").hide();
        $("#booking-buildings").find(".place-span").remove();

        $('#booking-period-error').css('display', 'none');
        breadcrumbsadd(2);

        for(var i = 0; i < buildings.length; i++){
            var b = buildings[i];

            if(i % 3 == 0){
                var text = "<tr>" + b.td_place() + "</tr";
                $('#booking-buildings tr:last').after(text);
            }

            else{
                $('#booking-buildings td:last').after(b.td_place());
            }
        }
     });

    $("#next-place").click(function(){
        //TODO: get the id of building
        $("#page1").hide();
        $("#page2").hide();
        $("#page3").hide();
        $("#page4").show();
        $("#page5").hide();

        breadcrumbsadd(3);
        //TODO: breadcrumps refresh
        $("#booking-places").find(".place-span").remove();
        //places = Place.all();
        var id = $(".building-selected > input").attr("value");
        console.log("Ate aqui places length:" );
        Place.make_places(id, test);
    });

    $("#next-finish").click(function(){
        $("#page1").hide();
        $("#page2").hide();
        $("#page3").hide();
        $("#page4").hide();
        $("#page5").hide();
        breadcrumbsadd(4);

        var building = $(".building-selected > input").attr("value");
        var place = $(".place-selected > input").attr("value");
        var booking_name = $("#booking_name").val();
        var start_date = $("#id_start_date").val();
        var end_date = $("#id_end_date").val();
        var start_hour = $( "#slider_begin_time" ).slider("value") + ":00:00";
        var end_hour = $( "#slider_end_time" ).slider("value") + ":00:00";
        var ar_week_days = Array();

        $("input[name=week_days]:checked").each(function(index){
            ar_week_days.push($(this).val());
        });

        $.post("/booking/newbooking/", {
            building     : building,
            place        : place,
            booking_name : booking_name,
            start_date   : start_date,
            end_date     : end_date,
            start_hour   : start_hour,
            end_hour     : end_hour,
            week_days    : ar_week_days

            }).done(function(result){
                $("#page5").append(result);
        });
    });
});
