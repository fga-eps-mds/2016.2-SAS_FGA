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

    this.make_places = function(id, callback){
        all = new Array()
        callback(all);
        url = "/buildings/places/" +id + "/";
        $.when($.getJSON(url)).then(function(data){
            for(var i = 0; i < data.length; i++){
                p = new Place(data[i].pk, data[i].name);
                all.push(p);
            }
            callback(all);
        });
    }

    this.make_unoccupied_places = function(data, callback) {
        all = new Array()
        for(var i = 0; i < data.length; i++){
            p = new Place(data[i].pk, data[i].name);
            all.push(p);
        }
        callback(all);
    }

    this.by_building = function(id){
        all = new Array()
        url = "/buildings/places/" +id + "/";
        $.when($.getJSON(url)).then(function(data){
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
    return p.all();

}

Place.by_building = function(id){
    p = new Place();
    return p.by_building(id);

}
Place.make_places = function(id, callback){
    p = new Place();
    return p.make_places(id, callback);
}

Place.make_unoccupied_places = function(data, callback) {
    p = new Place();
    return p.make_unoccupied_places(data, callback);
}
