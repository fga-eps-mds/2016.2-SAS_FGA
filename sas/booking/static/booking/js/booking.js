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

    this.removeError = function(element) {
        var text = document.getElementsByClassName('help-block');
        var error = document.getElementsByClassName('has-error');

        if(text.length || error.length) {
            $('.help-block').remove(); 
            $('.has-error').removeClass("has-error"); 
        }
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

    this.check_interval_date = function (element1, element2) {
        var startDate = element1.val();
        var endDate = element2.val();

        if (endDate < startDate) {
            this.addError(element2.parent());
            this.addSpan(element2, "End date has to be after start date");

            return false;
        }

        return true;
    }

    this.check_time = function(element1, element2, element3) {
        var startDate = Date.parse(element3.val());
        var beginTime = parseInt(element1.val());
        var endTime = parseInt(element2.val());
        var now = new Date();

        if(beginTime >= endTime) {
            this.addError(element2.parent());
            this.addSpan(element2, "End time has to be after begin time");

            return false;
        }

        if (beginTime < now.getHours() && startDate < now){
            this.addError(element1.parent());
            this.addSpan(element1, "Book time has to be after current time");                
            
            return false;
        }

        return true;
    }

    this.check_weekdays = function(element, array) {
        if (array.length == 0) {
            this.addError(element.parent());
            this.addSpan(element, "Weekday(s) cannot be blank");

            return false;
        }

        return true;
    }

    this.post_form = function(building, start_date, end_date, start_hour, end_hour, week_days, callback) {
        var place = new Place(1, "teste");

        $.when(
            $.post("/buildings/places/unoccupied/", {
                id_building: building,
                start_date: start_date,
                end_date: end_date,
                start_hour: start_hour,
                end_hour: end_hour,
                weekday: week_days
            })
        )


        .then(function(data) {
            place.make_unoccupied_places(data, callback);
        })        
    }
}
