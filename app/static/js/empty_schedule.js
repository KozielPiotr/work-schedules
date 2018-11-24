window.onload = function() {
    //adds css to left hours <td> after loading page
    $("td[id^='left-hours']").each(function() {
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
    $("td[id^='prev-left-hours']").each(function() {
        hours = $(this).text();
        if (parseInt(hours) < 0) {
            $(this).css("background", "#ff0000");
        } else if (parseInt(hours) > 0) {
            $(this).css("background", "#ffaa00");
        } else {
            $(this).css("background", "#ffffff");
        };
    });

    //counts in which billing period is current month
    let bpbYear = $("td[id='billing-period-begin']").find("input[name='bpb-y']").val();
    let bpbMonth = $("td[id='billing-period-begin']").find("input[name='bpb-m']").val();
    let bpBegin = new Date(bpbYear, bpbMonth-1);
    let curYear = $("#cur-year").text();
    let curMonth = $("#cur-month").text();
    let curDate = new Date(curYear, curMonth-1);
    let duration = parseInt($("td[id='billing-period-begin']").find("input[name='bpd']").val());
    let period = 0;
    let tempDate = bpBegin;
    while (tempDate <= curDate) {
        tempDate = new Date(tempDate.setMonth(tempDate.getMonth()+duration));
        period += 1
    };
    $("#billing_period").text(period);

    //counts in which billing week is current shift
    $("td[id^='to-json-']").each(function() {
        let bpBegin = new Date(bpbYear, bpbMonth-1);
        let curYearWeek = $(this).find("input[name='year']").val();
        let curMonthWeek = $(this).find("input[name='month']").val();
        let curDayWeek = $(this).find("input[name='day']").val();
        let curDateWeek = new Date(curYear, curMonth-1, curDayWeek);
        let tempDateWeek = bpBegin;
        let periodWeek = 0;


        while (tempDateWeek <= curDateWeek) {
        console.log("Początek pętli wewn.");
            tempDateWeek = new Date(tempDateWeek.setDate(tempDateWeek.getDate()+7));
            console.log(tempDateWeek);
            periodWeek += 1;
            console.log("Koniec pętli wewn.");
        };
        $(this).find("input[name='billing_period-week']").val(periodWeek);
        console.log(curDateWeek + " to " + periodWeek + " tydzień");
    });
};



//checkes if there is 11 hours rest time between shifts
function restTime(currentSelector, worker, year, month, day) {
    currentDay = parseInt($(currentSelector).find("input[name='day']").val());
    currentDayHour = parseInt($(currentSelector).find("input[name='b-hour']").val());
    if ($(currentSelector).find("input[name='event']").val() !== "in_work" && $(currentSelector).find("input[name='event']").val() !== "UNŻ" &&
        $(currentSelector).find("input[name='event']").val() !== "in_work" !== "L4") {
        restHours = 11;
    } else {
        prevMonthDays = [];
        if (currentDay > 1) {
            prevSelector = $(`td[id="to-json-${worker}-${year}-${month}-${day-1}"]`);
            prevDay = parseInt($(prevSelector).find("input[name='day']").val());
            prevDayHour = parseInt($(prevSelector).find("input[name='e-hour']").val());
            restStart = new Date(year, (month-1), prevDay, prevDayHour);
            restStop = new Date(year, (month-1), currentDay, currentDayHour);
        } else {
            $("th[class='prev-daynumber-th']").each(function() {
                prevMonthDays.push(parseInt($(this).text()));
            });
            prevDay = Math.max(...prevMonthDays);
            prevDayHour = $(`td[id="prev-end-${worker}-${year}-${month-1}-${prevDay}"]`).text();
            restStart = new Date(year, (month-2), prevDay, prevDayHour);
            restStop = new Date(year, (month-1), currentDay, currentDayHour);
        };
        if (isNaN(prevDayHour)) {
            restHours = 11;
        } else {
            restHours = (restStop-restStart)/3600000;
        };
        console.log(worker, restStop, restStart, restHours, currentDayHour);
    };
    return restHours
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
        let billingPeriod = $("#billing_period").text();
        let billingWeek = $(this).find("input[name='billing_period-week']").val();

        if (isNaN(beginHour)) {
            beginHour = 0;
        };
        if (isNaN(endHour)) {
            endHour = 0;
        };
        directDay = $(this);

        if (restTime(directDay, worker, year, month, day) < 11) {
            numberOfErrors += 1;
            errors[numberOfErrors] = (`\n${numberOfErrors}. Niezachowane 11 godzin odpoczynku u ${worker} przed dniem ${day}.${month}.${year} `)
        };

        //checks if everything is filled correctly
        if ((event==="UW" || event==="UO" || event==="UB") && (beginHour!==0 || endHour!==8)) {
            numberOfErrors += 1;
            errors[numberOfErrors] = (`\n${numberOfErrors}. Niewłaściwe godziny ${event} u ${worker} w dniu ${day}.${month}.${year}`);
        };
        if (event==="UNŻ" && (beginHour===0 || endHour===0)) {
            numberOfErrors += 1;
            errors[numberOfErrors] = (`\n${numberOfErrors}.Niewłaściwe godziny ${event} u ${worker} w dniu ${day}.${month}.${year}`);
        };


        //fills array for json
        hours.push({"day": day, "month": month, "year": year, "worker": worker, "from": beginHour,
                    "to": endHour, "sum": wrkd, "event": event, "workplace": workplace, "billing_period": billingPeriod,
                    "billing_week": billingWeek});
    });
    if (errors.length > 0) {
        alert(errors);
        return false;
    };
    jsonDict[work] = hours;
    return jsonDict;
};


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


//gives cells and fields color of event for current month
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



