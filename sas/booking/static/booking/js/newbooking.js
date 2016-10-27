var buildings = Building.all();

function breadcrumbsadd(index){
    $("#breadcrumbs ul li:eq(" + index + ")").addClass("active")

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
            if(i % 3 == 0){
                var text = "<tr>" + p.td_place() + "</tr";
                $('#booking-places tr:last').after(text);
            }else{
                $('#booking-places td:last').after(p.td_place());
            }
        }
}
$(document).ready(function(){
    $("#page1").show();
    $("#page2").hide();
    $("#page3").hide();
    $("#page4").hide();
    $("#page5").hide();
    
    
    
    $("#next-date").click(function(){
        $("#page1").hide();
        $("#page2").show();
        $("#page3").hide();
        $("#page4").hide();
        $("#page5").hide();
        breadcrumbsadd(0);
    });
    $("#next-building").click(function(){
        $("#page1").hide();
        $("#page2").hide();
        $("#page3").show();
        $("#page4").hide();
        $("#page5").hide();
        breadcrumbsadd(1);
        console.log(buildings.length);
        for(var i = 0; i < buildings.length; i++){
            var b = buildings[i];
            if(i % 3 == 0){
                var text = "<tr>" + b.td_place() + "</tr";
                $('#booking-buildings tr:last').after(text);
            }else{
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
        breadcrumbsadd(2);
        //TODO: breadcrumps refresh
        
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
        $("#page5").show();
        breadcrumbsadd(3);
    });
});

