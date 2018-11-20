//checkes if there is 11 hours of rest between shifts
function restTime(currentSelector, worker, year, month, day) {
    currentDay = parseInt($(currentSelector).find("input[name='day']").val());
    currentDayHour = parseInt($(currentSelector).find("input[name='b-hour']").val());
    prevMonthDays = [];
    if (currentDay > 1) {
        prevDay = $(`td[id="to-json-${worker}-${year}-${month}-${day-1}"]`);
    } else {
        console.log("Zeszły miesiąc");
        $("td[id^='to-json-prev-${worker}-']").each(function() {
            prevMonthLastDay.push(parseInt($(this).find("input[name='day']").val()));
        });
        prevMonthLastDay = Math.max(...prevMonthDays);
        prevSelector = $(`td[id="to-json-prev-${worker}-${year}-${month}-${prevMonthLastDay}"]`);
    };
    prevDay = parseInt($(prevSelector).find("input[name='day']").val());
    prevDayHour = parseInt($(prevSelector).find("input[name='e-hour']").val());

    restStart = new Date(year, (month-1), prevDay, prevDayHour);
    restStop = new Date(year, (month-1), currentDay, currentDayHour);
    restHours = (restStop-restStart)/3600000;

    if (isNaN(prevDayHour)) {
        prevDayHour = 8;
    };
};


//gets data of all days in month and prepers dict for json
function getHours() {
    let hours = [];
    let jsonDict = {};
    let work = "";
    $("td[id^='begin']").each(function() {
        $(this).change();
    });
    let numberOfErrors = 0
    let errors = [];
    $("td[id^='to-json-']").each(function() {
        selHelper = $(this).find("input[name='helper']").val();
        let day = $(this).find("input[name='day']").val();
        let month = $(this).find("input[name='month']").val();
        let year = $(this).find("input[name='year']").val();
        let worker = $(this).find("input[name='worker']").val();
        let beginHour = parseInt($(this).find("input[name='b-hour']").val());
        let endHour = parseInt($(this).find("input[name='e-hour']").val());
        let wrkd = $(this).find("input[name='counted']").val();
        let event = $(this).find("input[name='event']").val();
        let workplace = $(this).find("input[name='shop']").val();

        if (isNaN(beginHour)) {
            beginHour = 0;
        };
        if (isNaN(endHour)) {
            endHour = 0;
        };
        directDay = $(this);
        restTime(directDay, worker, year, month, day);

        //checks if everything is filled correctly
        if ((event==="UW" || event==="UO" || event==="UB") && (beginHour!==0 || endHour!==8)) {
            numberOfErrors += 1
            errors[numberOfErrors] = (`\n${numberOfErrors}. Niewłaściwe godziny ${event} u ${worker} w dniu ${day}.${month}.${year}`);
        };
        if (event==="UNŻ" && (beginHour===0 || endHour===0)) {
            numberOfErrors += 1
            errors[numberOfErrors] = (`\n${numberOfErrors}.Niewłaściwe godziny ${event} u ${worker} w dniu ${day}.${month}.${year}`)
        };


        //fills array for json
        hours.push({"day": day, "month": month, "year": year, "worker": worker, "from": beginHour,
                    "to": endHour, "sum": wrkd, "event": event, "workplace": workplace});
    });
    if (errors.length > 0) {
        alert(errors);
        return false;
    };
    jsonDict[work] = hours;
    return jsonDict;
}


$(document).ready(function() {
        $("form").submit(function(e){
            let form = $(this);
            $.ajax({
                url   : form.attr("action"),
                type  : form.attr("method"),
                contentType: 'application/json;charset=UTF-8',
                data  : JSON.stringify(getHours()),
                success: function(response){
                    alert(response);
                    //window.location.replace(response);
                },
            });
            return false;
        });
});


//fills <td> that sends data to form json
function tdToJson(selHelper, from, to, counted, event) {
    let td = $(`td[id="to-json-${selHelper}"]`);
    td.find("input[name='b-hour']").val(from);
    td.find("input[name='e-hour']").val(to);
    td.find("input[name='counted']").val(counted);
    td.find("input[name='event']").val(event);
};


//counts sum of hours worked by worker in day
$(document).ready(function() {
    $("td[id^='begin-'], td[id^='end-']").change(function() {
        let selHelper = $(this).find("input[name='helper']").val();
        let from = parseInt($(`#begin-${selHelper}`).find("input[name='begin-hour']").val());
        let to = parseInt($(`#end-${selHelper}`).find("input[name='end-hour']").val());
        let counted = $(`#counted-${selHelper}`).find("output[name='counted']");
        let event = $(`#event-${selHelper}`).find(":selected").val();
        if (isNaN(from)) {
              from = 0;
        };
        if (isNaN(to)) {
            to = 0;
        };
        if (isNaN(counted.val())) {
            counted.val(0);
        };
        counted.val(to - from).change();
        counted = counted.val();
        tdToJson(selHelper, from, to, counted, event);
    });
});


//gives cells and fields color of event
$(document).ready(function() {
    $("td[id^='event-']").change(function() {
        let selHelper = $(this).find("input[name='helper']").val();
        let event = $(this).find(":selected");
        let from = $(`#begin-${selHelper}`).find("input[name='begin-hour']");
        let to = $(`#end-${selHelper}`).find("input[name='end-hour']");
        let counted = $(`#counted-${selHelper}`).find("output[name='counted']");

        if (event.val()==="off" || event.val()==="in_work") {
            $(this).css("background", "#fff");
            $(`#begin-${selHelper}`).css("background", "#fff");
            $(`#end-${selHelper}`).css("background", "#fff");
            $(`#counted-${selHelper}`).css("background", "#fff");
            from.css("background", "#fff");
            to.css("background", "#fff");
            counted.css("background", "#fff");
            event.css("background", "#fff");
        } else if (event.val()=="UW") {
            $(this).css("background", "#FC33FF");
            $(`#begin-${selHelper} *`).css("background", "#FC33FF");
            $(`#end-${selHelper}`).css("background", "#FC33FF");
            $(`#counted-${selHelper}`).css("background", "#FC33FF");
            from.css("background", "#FC33FF");
            to.css("background", "#FC33FF");
            counted.css("background", "#FC33FF");
            event.css("background", "#FC33FF");
            from.val("");
            to.val(8).change();
        } else if (event.val()==="UNŻ" || event.val()==="UO" || event.val()==="UOJ" ||
                    event.val()==="UR" || event.val()==="UB") {
            if (isNaN(parseInt(from.val()))){
                let worker = $(`td[id="to-json-${selHelper}"]`).find("input[name='worker']").val();
                let day = $(`td[id="to-json-${selHelper}"]`).find("input[name='day']").val();
                missingHours = prompt(`Wpisz prawidłową godzinę rozpoczęcia pracy dla pracownika ${worker} w dniu ${day}.`);
                from.val(missingHours).change();
            };
            if (isNaN(parseInt(to.val()))){
                let worker = $(`td[id="to-json-${selHelper}"]`).find("input[name='worker']").val();
                let day = $(`td[id="to-json-${selHelper}"]`).find("input[name='day']").val();
                missingHours = prompt(`Wpisz prawidłową godzinę zakończenia pracy dla pracownika ${worker} w dniu ${day}.`);
                to.val(missingHours).change();
            };
            $(this).css("background", "#FC33FF");
            $(`#begin-${selHelper}`).css("background", "#FC33FF");
            $(`#end-${selHelper}`).css("background", "#FC33FF");
            $(`#counted-${selHelper}`).css("background", "#FC33FF");
            from.css("background", "#FC33FF");
            to.css("background", "#FC33FF");
            counted.css("background", "#FC33FF");
            event.css("background", "#FC33FF");
        } else if (event.val()==="L4") {
            $(this).css("background", "#80D332");
            $(`#begin-${selHelper}`).css("background", "#80D332");
            $(`#end-${selHelper}`).css("background", "#80D332");
            $(`#counted-${selHelper}`).css("background", "#80D332");
            from.css("background", "#80D332");
            to.css("background", "#80D332");
            counted.css("background", "#80D332");
            event.css("background", "#80D332");
        };
    });
});


//counts sum of hours worked by worker in whole month and hours left to work or overtime
$(document).ready(function() {
    $("td[id^='begin-'], td[id^='end-']").change(function() {
        let selHelper = $(this).find("input[name='helper']").val();
        worker = $(`td[id="to-json-${selHelper}"]`).find("input[name='worker']").val();
        monthHours = $("#working-hours").val();
        sum = 0;
        $(`td[id^="to-json-${worker}"]`).each(function() {
            hours = parseInt($(this).find("input[name='counted']").val());
            if (isNaN(hours)) {
                hours = 0;
            };
            sum += hours;
        });
        $(`#hours-of-${worker}`).val(sum); //sum of worker's hours
        $(`#hours-left-for-${worker}`).val(monthHours - sum); //ours left or overtime

        //adds css if there are hours left of overtime
        if (parseInt($(`#hours-left-for-${worker}`).val()) < 0) {
            $(`#hours-left-for-${worker}`).css("background", "#ff0000");
            $(`#left-hours-${worker}`).css("background", "#ff0000");
        } else if (parseInt($(`#hours-left-for-${worker}`).val()) > 0) {
            $(`#hours-left-for-${worker}`).css("background", "#ffaa00");
            $(`#left-hours-${worker}`).css("background", "#ffaa00");
        } else {
            $(`#hours-left-for-${worker}`).css("background", "#ffffff");
            $(`#left-hours-${worker}`).css("background", "#ffffff");
        };
    });
});





//adds css to left hours <td> after loading page
window.onload = function() {
    $("td[id^='left-hours").each(function() {
        hours = $(this).find("output");
        if (parseInt(hours.val()) < 0) {
            $(this).css("background", "#ff0000");
            hours.css("background", "#ff0000");
        } else if (parseInt(hours.val()) > 0) {
            $(this).css("background", "#ffaa00");
            hours.css("background", "#ffaa00");
        } else {
            $(this).css("background", "#ffffff");
            hours.css("background", "#ffffff");
        };
    });
    $("td[id^='prev-left-hours").each(function() {
        hours = $(this).text();
        if (parseInt(hours) < 0) {
            $(this).css("background", "#ff0000");
        } else if (parseInt(hours) > 0) {
            $(this).css("background", "#ffaa00");
        } else {
            $(this).css("background", "#ffffff");

        };
    });
};