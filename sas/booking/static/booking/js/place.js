function Place(pk, name){
    this.pk = pk;
    this.name = name;
    

    this.td_place = function(){
        var begin = "<td class='place-span'>";
        var input = "<input type='hidden' value='" + this.pk + "' />";
         
        var end = "</td>"
        return begin + input + this.name + end;
    }

    this.all = function(){
        all = new Array()
        $.getJSON("/places", function(data){
            for(var i = 0; i < data.length; i++){
                p = new Place(data[i].pk, data[i].name);
                all.push(p);
            }
        });
        return all;
    }
}

Place.all = function(){
    p = new Place();
    return p.all()

}


