function Booking(){
    this.check_empty = function(value){
        if(value.length == 0){
           return false; 
        }else{
            return true;
        }
    }
    this.check_name = function(value){
        if(value.length == 0){
           return false; 
        }else{
            return true;
        }
    }   
    this.addError = function(element){
        if(!element.hasClass("has-error")){
            element.addClass("has-error");
        }
    }
    this.addSpan = function(element, text){
        if(element.has(".help-block") == false){
            element.after("<span class='help-block'>" + text + "</span");
        }
    }
    this.check_name_element = function(element){
        
        var name = element.val();
        if(!this.check_name(name)){
            this.addError(element.parent());
            this.addSpan(element, "Booking name cannot be blanck");
            return false;
        }
        return true;

    }
    this.check_date = function(element){
        var date = element.val();
        if(!this.check_empty(name)){
            this.addError(element.parent());
            this.addSpan(element, "Date  cannot be blanck");
            return false;
        }
        return true;
    }
}
