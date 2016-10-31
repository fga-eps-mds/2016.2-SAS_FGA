function Building(){
 
    this.check_name = function(value){
        if(value.length == 0){
           return false; 
        }else{
            return true;
        }
    }   
    this.check_name_element = function(element){
        var name = element.find("form-control").val();
        if(!this.check_name(name)){
            element.addClass("has-error");
            element.find("form-control").after("<span class='help-block'> Enter a valid date. </span>");
        }
    }
}
