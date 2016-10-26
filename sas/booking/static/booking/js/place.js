function Place(pk, name){
    this.pk = pk;
    this.name = name;

    this.tran = function(data){
        all = new Array()
        for(var i = 0; i < data.length; i++){
            p = new Place(data[i].pk, data[i].name);
            all.push(all);
            console.log(p.pk);
            console.log(p.name);
        }
        return all;
    }

    this.all = function(){
        $.getJSON("/places",  this.tran)
    }
}

Place.all = function(){
    p = new Place();
    p.all()

}


