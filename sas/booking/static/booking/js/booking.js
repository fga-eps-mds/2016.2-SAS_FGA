function Booking() {

    this.check_empty = function(value) {
        if(value.length == 0) {
           return false;
        }

        else {
            return true;
        }
    }

    this.check_name = function(value) {
        if(value.length == 0) {
           return false;
        }

        else {
            return true;
        }
    }

    this.addError = function(element) {
        if(!element.hasClass("has-error")) {
            element.addClass("has-error");
        }
    }

    this.addSpan = function(element, text) {
        if(document.getElementsByClassName("help-block").length > 0) {
            $('.help-block').remove();
        }

        element.after("<span class='help-block'>" + text + "</span>");
    }

    this.check_name_element = function(element) {
        var name = element.val();

        if(!this.check_name(name)) {
            this.addError(element.parent());
            this.addSpan(element, "Booking name cannot be blank");

            return false;
        }

        return true;
    }

    this.check_date = function(element) {
        var date = element.val();

        if(!this.check_empty(date)) {
            this.addError(element.parent());
            this.addSpan(element, "Date cannot be blank");

            return false;
        }

        var today = new Date();
        var dd = today.getDate();
        var mm = today.getMonth() + 1;

        var yyyy = today.getFullYear();
        if(dd<10) { dd='0'+dd }
        if(mm<10) { mm='0'+mm }

        var today = mm+'/'+dd+'/'+yyyy;

        if(date < today) {
            this.addError(element.parent());
            this.addSpan(element, "Date has to be bigger or equal to today's date");

            return false;
        }

        return true;
    }
}
