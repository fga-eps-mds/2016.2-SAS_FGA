var places = Place.all();

function breadcrumbsadd(index){
    $("#breadcrumbs ul li:eq(" + index + ")").addClass("active")

}

$(document).ready(function(){
    $("#page1").hide();
    $("#page3").hide();
    
    $("#next-place").click(function(){
        //TODO: get the id of building
         
        $("#page2").hide();
        $("#page3").show();
        breadcrumbsadd(2);
        //TODO: breadcrumps refresh
        
        //places = Place.all();
        console.log("Ate aqui places length:", places.length);
        for(var i = 0; i < places.length; i++){
            p = places[i];
            if(i % 3 == 0){
                text = "<tr>" + p.td_place() + "</tr";
                $('#booking-places tr:last').after(text);
            }else{
                $('#booking-places td:last').after(p.td_place());
            }
        }

    });
});

