function Building(pk, name){
    this.pk = pk;
    this.name = name;


    this.td_place = function(){
        var begin = "<td class='place-span'><i class='glyphicon glyphicon-home'></i>&nbsp;";
        var input = "<input type='hidden' value='" + this.pk + "' />";

        var end = "</td>"
        return begin + input + this.name + end;
    }

    this.all = function(){
        var all = new Array()
        $.getJSON("/buildings", function(data){
            for(var i = 0; i < data.length; i++){
                var p = new Building(data[i].pk, data[i].name);
                all.push(p);
            }
        });
        return all;
    }

}

Building.all = function(){
    var b = new Building();
    return b.all();

}
