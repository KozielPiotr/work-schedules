//fills <td> that sends data to form json
function tdToJson(selHelper, from, to, counted, event) {
    let td = $(`td[id="to-json-${selHelper}"]`);
    td.find("input[name='b-hour']").val(from);
    td.find("input[name='e-hour']").val(to);
    td.find("input[name='counted']").val(counted);
    td.find("input[name='event']").val(event);
};

function prevEventsCss(selector, selHelper, event, from, to, counted){
    if (event.text() === "X" || event.text() === "........") {
        if($(selector).closest("tr").find("th[class='prev-dayname-th']").text() === "Sobota" ||
                $(selector).closest("tr").find("th[class='prev-dayname-th']").text() === "Niedziela") {
            from.css("background", "#aba5a5c7");
            to.css("background", "#aba5a5c7");
            counted.css("background", "#aba5a5c7");
            event.css("background", "#aba5a5c7");
            console.log("1");
        } else {
            from.css("background", "#fff");
            to.css("background", "#fff");
            counted.css("background", "#fff");
            event.css("background", "#fff");
            console.log("2");
        };
    } else if (event.text() === "UNŻ" || event.text() === "UO" || event.text() === "UOJ" ||
                event.text() === "UR" || event.text() === "UB" || event.text() === "UW") {
        from.css("background", "#FC33FF");
        to.css("background", "#FC33FF");
        counted.css("background", "#FC33FF");
        event.css("background", "#FC33FF");
        console.log("3");
    } else if (event.text()==="L4") {
        from.css("background", "#80D332");
        to.css("background", "#80D332");
        counted.css("background", "#80D332");
        event.css("background", "#80D332");
        console.log("4");
    };
    console.log("funkcja");
};

function eventsCss(selector, selHelper, event, from, to, counted){
    //let event = $(selector).find(":selected");
    //let from = $(`#begin-${selHelper}`).find("input[name='begin-hour']");
    //let to = $(`#end-${selHelper}`).find("input[name='end-hour']");
    //let counted = $(`#counted-${selHelper}`).find("output[name='counted']");

    if (event.val() === "off" || event.val() === "in_work") {
        if($(selector).closest("tr").find("th[class='dayname-th']").text() === "Sobota" ||
                $(selector).closest("tr").find("th[class='dayname-th']").text() === "Niedziela") {
            $(selector).css("background", "#aba5a5c7");
            $(`#begin-${selHelper}`).css("background", "#aba5a5c7");
            $(`#end-${selHelper}`).css("background", "#aba5a5c7");
            $(`#counted-${selHelper}`).css("background", "#aba5a5c7");
            from.css("background", "#aba5a5c7");
            to.css("background", "#aba5a5c7");
            counted.css("background", "#aba5a5c7");
            event.css("background", "#aba5a5c7");
        } else {
            $(selector).css("background", "#fff");
            $(`#begin-${selHelper}`).css("background", "#fff");
            $(`#end-${selHelper}`).css("background", "#fff");
            $(`#counted-${selHelper}`).css("background", "#fff");
            from.css("background", "#fff");
            to.css("background", "#fff");
            counted.css("background", "#fff");
            event.css("background", "#fff");
        };
    } else if (event.val() === "UNŻ" || event.val() === "UO" || event.val() === "UOJ" ||
                event.val() === "UR" || event.val() === "UB" || event.val() === "UW") {
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
        $(selector).css("background", "#FC33FF");
        $(`#begin-${selHelper}`).css("background", "#FC33FF");
        $(`#end-${selHelper}`).css("background", "#FC33FF");
        $(`#counted-${selHelper}`).css("background", "#FC33FF");
        from.css("background", "#FC33FF");
        to.css("background", "#FC33FF");
        counted.css("background", "#FC33FF");
        event.css("background", "#FC33FF");
    } else if (event.val()==="L4") {
        $(selector).css("background", "#80D332");
        $(`#begin-${selHelper}`).css("background", "#80D332");
        $(`#end-${selHelper}`).css("background", "#80D332");
        $(`#counted-${selHelper}`).css("background", "#80D332");
        from.css("background", "#80D332");
        to.css("background", "#80D332");
        counted.css("background", "#80D332");
        event.css("background", "#80D332");
    };
};


//checks if there is 35-hour break once in every billing week
function weeklyRest() {
    //fills hidden td with proper event values
    $("td[id^='event-']").each(function() {
        $(this).change();
    });

    //list of workers
    let workers = [];
    $("th[class='worker-name']").each(function() {
        workers.push($(this).text());
    });

    //list of billing weeks
    let billingWeeksNumbers = [];
    $("input[name='billing-period-week']").each(function(){
        if (!(billingWeeksNumbers.includes($(this).val()))) {
            billingWeeksNumbers.push($(this).val())
        };
    });

    //list of all dates in month
    let datesInMonth = [];
    let curYear = $("#cur-year").text();
    let curMonth = $("#cur-month").text()-1;
    let monthBegin = new Date(curYear, curMonth);
    let tempDate = new Date(monthBegin);
    while (monthBegin.getMonth() === tempDate.getMonth()) {
        datesInMonth.push(new Date(tempDate));
        tempDate = new Date(tempDate.setDate(tempDate.getDate()+1));
    };

    //defines the beginning of current billing period
    const monthOfBillingPeriod = parseInt($("#month-of-billing-period").text());
    const billingPeriodDuration =  $("td[id='billing-period-begin']").find("input[name='bpd']").val();
    monthBegin = new Date(curYear, curMonth);
    const currentBillingPeriodBegin = new Date(monthBegin.setMonth(monthBegin.getMonth()-(monthOfBillingPeriod-1)));

    //assigns dates to weeks
    let currentBillingPeriodBeginYear = currentBillingPeriodBegin.getFullYear();
    let currentBillingPeriodBeginMonth = currentBillingPeriodBegin.getMonth();
    weeksDict = {};
    for (let week in billingWeeksNumbers) {
        datesList = [];
        for (date in datesInMonth) {
            const beginDate1 = new Date(currentBillingPeriodBeginYear, currentBillingPeriodBeginMonth);
            const beginDate2 = new Date(currentBillingPeriodBeginYear, currentBillingPeriodBeginMonth);
            if (datesInMonth[date] <= new Date(beginDate1.setDate(beginDate1.getDate()*billingWeeksNumbers[week]*7)) &&
                datesInMonth[date] > new Date(beginDate2.setDate(beginDate2.getDate()*(billingWeeksNumbers[week]-1)*7))) {
                datesList.push(datesInMonth[date]);
            weeksDict[billingWeeksNumbers[week]] = datesList;
            };
        };
    };

    lastWeekInMonth = parseInt(billingWeeksNumbers[billingWeeksNumbers.length-1]);

    //checking 35-hours break
    let weeklyHoursErrors = []
    for (let worker in workers) {
        for (let week in weeksDict) {
            //finds last day of billing week
            weekLength = weeksDict[week].length - 1;
            let lastDay = new Date(weeksDict[week][weekLength]);
            let firstDay= new Date(new Date(lastDay).setDate(lastDay.getDate()-6));
            let hours = 0;
            weeklyBreak = false;
            if (week ==  lastWeekInMonth && weeksDict[week].length < 7) {
                weeklyBreak = true;
            } else {
                //finds td in template that contains data for current day and worker
                name = workers[worker].replace(" ", "_");
                let year = lastDay.getFullYear();
                let month = lastDay.getMonth();
                let currentDay = new Date(lastDay);
                let td = `td[id^="to-json-${name}-${currentDay.getFullYear()}-${currentDay.getMonth()+1}-${currentDay.getDate()}"]`;
                let start = new Date(new Date(lastDay.setDate(lastDay.getDate()+1)));
                let stop;
                while ($(td).find("input[name='billing-period-week']").val()==week) {
                    if ($(td).find("input[name='event']").val() === "off") {
                        if (currentDay.getTime() === firstDay.getTime()) {
                            stop = new Date(firstDay);
                            hours = -((stop-start)/3600000);
                            td = `td[id^="${currentDay.getFullYear()}-${currentDay.getMonth()+1}-${currentDay.getDate()-1}"]`;
                        } else {
                            currentDay = new Date(currentDay.setDate(currentDay.getDate()-1));
                            if (currentDay.getMonth() === month-1) {
                                td = `td[id^="prev-to-json-${name}-${currentDay.getFullYear()}-${currentDay.getMonth()+1}-${currentDay.getDate()}"]`;
                            } else {
                                td = `td[id^="to-json-${name}-${currentDay.getFullYear()}-${currentDay.getMonth()+1}-${currentDay.getDate()}"]`;
                            };
                        };
                    } else {
                        stop = new Date(new Date(currentDay).setHours($(td).find("input[name='e-hour']").val()));
                        hours = -((stop-start)/3600000);
                        start = new Date(new Date(currentDay).setHours($(td).find("input[name='b-hour']").val()));
                        currentDay = new Date(currentDay.setDate(currentDay.getDate()-1));
                        if (currentDay.getMonth() === month-1) {
                            td = `td[id^="prev-to-json-${name}-${currentDay.getFullYear()}-${currentDay.getMonth()+1}-${currentDay.getDate()}"]`;
                        } else {
                            td = `td[id^="to-json-${name}-${currentDay.getFullYear()}-${currentDay.getMonth()+1}-${currentDay.getDate()}"]`;
                        };
                    };
                    if (hours >= 35) {
                        weeklyBreak = true;
                    };
                };
            };
            if (weeklyBreak === false) {
                weeklyHoursErrors.push(`\n${workers[worker]}: Niezachowana 35 godzinna przerwa w tygodniu ${firstDay.getDate()}.${firstDay.getMonth()+1}.${firstDay.getFullYear()} - ${lastDay.getDate()}.${lastDay.getMonth()+1}.${firstDay.getFullYear()}`);
            };
        };
    };
    if (weeklyHoursErrors.length > 0) {
        alert(weeklyHoursErrors);
        return false;
    } else {
        return true;
    };

};


//checks if there is 11 hours rest time between shifts
function restTime(currentSelector, worker, year, month, day) {
    currentDay = parseInt($(currentSelector).find("input[name='day']").val());
    currentDayHour = parseInt($(currentSelector).find("input[name='b-hour']").val());
    if ($(currentSelector).find("input[name='event']").val() === "off") {
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
    };
    return restHours
};


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

    //adds css to weekend rows (saturdays and sundays)
    $("th[class$='dayname-th']").each(function() {
        if ($(this).text() === "Sobota" || $(this).text() === "Niedziela") {
            $(this).closest("tr").find("*").css("background", "#aba5a5c7");
        };
    });

    //counts in which billing period is current month and what is current month's number in billing period
    let bpbYear = $("td[id='billing-period-begin']").find("input[name='bpb-y']").val();
    let bpbMonth = $("td[id='billing-period-begin']").find("input[name='bpb-m']").val();
    let bpBegin = new Date(bpbYear, bpbMonth-1);
    let curYear = $("#cur-year").text();
    let curMonth = $("#cur-month").text();
    let curDate = new Date(curYear, curMonth-1);
    let duration = parseInt($("td[id='billing-period-begin']").find("input[name='bpd']").val());
    let period = 0;
    let tempDate = bpBegin;

    //billing period
    monthNu = 0;
    bpBegin = new Date(bpbYear, bpbMonth-1);
    tempDate = bpBegin;
    while (tempDate <= curDate) {
        tempDate = new Date(tempDate.setMonth(tempDate.getMonth()+1));
        monthNu ++;
        if (monthNu % duration === 1) {
            period ++;
        };
    };
    $("td[id='billing-period']").find("input[name='billing-period']").val(period);

    //month in billing period
    monthNumberInBp = monthNu % duration;
    if (monthNumberInBp === 0) {
        monthNumberInBp = duration;
    };
    $("#month-of-billing-period").text(monthNumberInBp);

    //counts in which billing week is current shift
        //makes list of all days in month
    let date = new Date(curYear, curMonth-1);
    let days = [];
    while (date.getMonth() === curMonth-1) {
        days.push(new Date(date));
        date.setDate(date.getDate() + 1);
    };
        //assigns billing week number to each date in month
    let weekDates = {};
    function assignWeeksToDates(element, index, array) {
        let curDate = new Date(curYear, curMonth-1);
        let monthsToBegin = monthNumberInBp - 1;
        let bpBegin = new Date(curDate.setMonth(curDate.getMonth()-monthsToBegin));
        let curDateWeek = element;
        let tempDateWeek = bpBegin;
        let periodWeek = 0;
        while (tempDateWeek <= curDateWeek) {
            tempDateWeek = new Date(tempDateWeek.setDate(tempDateWeek.getDate()+7));
            periodWeek ++;
        };
        weekDates[element] = periodWeek;

    }
    days.forEach(assignWeeksToDates);

    let zeroWeek;
    $("td[id^='to-json-']").each(function() {
        curDate = new Date(curYear, curMonth-1);
        let monthsToBegin = monthNumberInBp - 1;
        let bpBegin = new Date(curDate.setMonth(curDate.getMonth()-monthsToBegin));
        let curYearWeek = $(this).find("input[name='year']").val();
        let curMonthWeek = $(this).find("input[name='month']").val();
        let curDayWeek = $(this).find("input[name='day']").val();
        let curDateWeek = new Date(curYearWeek, curMonthWeek-1, curDayWeek);
        let tempDateWeek = new Date (curDateWeek.getFullYear(), curDateWeek.getMonth(), curDateWeek.getDate());
        if ((monthNumberInBp === duration && bpBegin.getDay() === curDateWeek.getDay() &&
            curDateWeek.getMonth() !== new Date (tempDateWeek.setDate(curDateWeek.getDate()+6)).getMonth()) ||
            curDateWeek >= zeroWeek) {
                zeroWeek = new Date(curDateWeek);
                $(this).find("input[name='billing-period-week']").val(0);
        } else {
            $(this).find("input[name='billing-period-week']").val(weekDates[curDateWeek]);
        };
    });

    //adds css to prev month table
    $("td[id^='prev-event-']").each(function() {
        let selector = $(this);
        let selHelper = $(selector).closest("td").attr('id').replace("prev-event-", "");
        let event = $(selector);
        let from = $(`#prev-begin-${selHelper}`);
        let to = $(`#prev-end-${selHelper}`);
        let counted = $(`#prev-counted-${selHelper}`);
        counted.css("background", "red");
        prevEventsCss(selector, selHelper, event, from, to, counted);
        console.log("OK");
    });

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
        let wrkd = parseInt($(this).find("input[name='counted']").val());
        let event = $(this).find("input[name='event']").val();
        let workplace = $(this).find("input[name='shop']").val();
        let billingPeriod = $("td[id='billing-period']").find("input[name='billing-period']").val();
        let billingWeek = $(this).find("input[name='billing-period-week']").val();

        if (isNaN(beginHour)) {
            beginHour = 0;
        };
        if (isNaN(endHour)) {
            endHour = 0;
        };
        directDay = $(this);

        //checks if everything is filled correctly
        if (wrkd > 12) {
            tooMany = window.confirm(`Czy ${worker} powinien pracować ponad 12 godzin w dniu ${day}.${month}.${year}?\nJeżeli tak, naciśnij "OK".`);
            if (!tooMany) {
            numberOfErrors += 1;
            errors[numberOfErrors] = (`\n${numberOfErrors}. Ponad 12 godzin pracy u ${worker} w dniu ${day}.${month}.${year}`);
            };
        };

        if (restTime(directDay, worker, year, month, day) < 11) {
            numberOfErrors += 1;
            errors[numberOfErrors] = (`\n${numberOfErrors}. Niezachowane 11 godzin odpoczynku u ${worker} przed dniem ${day}.${month}.${year}`);
        };

        if (beginHour === 0 && endHour !== 0) {
            numberOfErrors += 1;
            errors[numberOfErrors] = (`\n${numberOfErrors}. Brak godziny rozpoczęcia pracy ${worker} w dniu ${day}.${month}.${year}`);
        };

        if (beginHour !== 0 && endHour === 0) {
            numberOfErrors += 1;
            errors[numberOfErrors] = (`\n${numberOfErrors}. Brak godziny zakończenia pracy ${worker} w dniu ${day}.${month}.${year}`);
        };

        if (beginHour > endHour) {
            numberOfErrors += 1;
            errors[numberOfErrors] = (`\n${numberOfErrors}. Późniejsza godzina rozpoczęcia niż zakończenia pracy u ${worker} w dniu ${day}.${month}.${year}`);
        };

        if (beginHour === endHour && beginHour !== 0 && endHour !== 0) {
            numberOfErrors += 1;
            errors[numberOfErrors] = (`\n${numberOfErrors}. Praca nie może zaczynać się i kończyć o tej samej godzinie u ${worker} w dniu ${day}.${month}.${year}`);
        };

        if ((event==="UW" || event==="UB") && (wrkd !== 8)) {
            numberOfErrors += 1;
            errors[numberOfErrors] = (`\n${numberOfErrors}. Przy ${event} ${worker} w dniu ${day}.${month}.${year} zmiana musi trwać 8 godzin`);
        };
        if ((event==="UNŻ" && (beginHour===0 || endHour===0)) || (event==="UO" && (beginHour===0 || endHour===0))) {
            numberOfErrors += 1;
            errors[numberOfErrors] = (`\n${numberOfErrors}. Niewłaściwe godziny ${event} u ${worker} w dniu ${day}.${month}.${year}`);
        };


        //fills array for json
        hours.push({"day": day, "month": month, "year": year, "worker": worker, "from": beginHour,
                    "to": endHour, "sum": wrkd, "event": event, "workplace": workplace, "billing_period": billingPeriod,
                    "billing_week": billingWeek});
    });

    if (weeklyRest() === false) {
        numberOfErrors += 1;
        errors[numberOfErrors] = (`\n${numberOfErrors}. Niezachowanie 35 godzinnego odpoczynku tygodniowego`);
    }

    if (errors.length > 0) {
        alert(errors);
        return false;
    };
    jsonDict[work] = hours;
    return jsonDict;
};


//checks if schedule is filled correctly
$(document).ready(function() {
    $("#check-schedule-btn").click(function() {
        getHours()
    });
});


//submits schedule
$(document).ready(function() {
    $("form").submit(function(e){
    console.log("DUPA");
        let form = $(this);
        $.ajax({
            url   : form.attr("action"),
            type  : form.attr("method"),
            contentType: 'application/json;charset=UTF-8',
            data  : JSON.stringify(getHours()),
            success: function(response){
                if (response === "1") {
                    alert("Popraw błędy w stworzonym grafiku.");
                } else if (response === "2") {
                    alert("Coś poszło nie tak.\nPrawdopodobnie grafik już istnieje.");
                } else {
                    window.location.replace("/index");
                }
            },
        });
        return false;
    });
});


//counts sum of hours worked by worker in day
$(document).ready(function() {
    $("td[id^='begin-'], td[id^='end-'], td[id^='event-']").change(function() {
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


//keeps correct value of event field
$(document).ready(function() {
    $("td[id^='begin-'], td[id^='end-']").change(function() {
        let selHelper = $(this).find("input[name='helper']").val();
        let from = parseInt($(`#begin-${selHelper}`).find("input[name='begin-hour']").val());
        let to = parseInt($(`#end-${selHelper}`).find("input[name='end-hour']").val());
        let event = $(`#event-${selHelper}`).find("select[name='event']");

        //sets event to "off" when begin and end hour fields are empty OR
        //sets event to "in_work" if begin and end hour are not empty and event is "off"
        if ((isNaN(from) && isNaN(to)) && (event.val() === "in_work")) {
            event.val("off").change();
        } else if (!(isNaN(from) && isNaN(to)) && (event.val() === "off")) {
            event.val("in_work").change();
        };
    });

    //deletes begin and end hour if event is set to "off"
    $("td[id^='event-']").change(function() {
        let selHelper = $(this).find("input[name='helper']").val();
        let from = $(`#begin-${selHelper}`).find("input[name='begin-hour']");
        let to = $(`#end-${selHelper}`).find("input[name='end-hour']");
        let event = $(`#event-${selHelper}`).find("select[name='event']");
        if (event.val() === "off") {
            from.val("").change();
            to.val("").change();
        };
    });
});


//gives cells and fields color of event for current month
$(document).ready(function() {
    $("td[id^='event-']").change(function() {
        let selector = $(this);
        let selHelper = $(selector).find("input[name='helper']").val();
        let event = $(selector).find(":selected");
        let from = $(`#begin-${selHelper}`).find("input[name='begin-hour']");
        let to = $(`#end-${selHelper}`).find("input[name='end-hour']");
        let counted = $(`#counted-${selHelper}`).find("output[name='counted']");
        eventsCss(selector, selHelper, event, from, to, counted);
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



