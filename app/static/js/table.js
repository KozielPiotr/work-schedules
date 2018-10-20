function getHours() {
    var hours = [];
    var jsonDict = {};
    var work = "";
    $("table.inner").each(function() {
        var day = $(this).find("input[name='day']").val();
        var month = $(this).find("input[name='month']").val();
        var year = $(this).find("input[name='year']").val();
        var worker = $(this).find("input[name='worker']").val();
        var begin_hour = $(this).find("input[name='begin_hour']").val();
        var end_hour = $(this).find("input[name='end_hour']").val();
        var wrkd = $(this).find("output[name='counted']").val();
        hours.push({"day": day, "month": month, "year": year, "worker": worker, "from": begin_hour,
                    "to": end_hour, "sum": wrkd});
    });
    jsonDict[work] = hours;
    console.log(jsonDict);
    return jsonDict;
}


$(document).ready(function() {
    $("form").submit(function(e){
        var form = $(this);
        $.ajax({
            url   : form.attr("action"),
            type  : form.attr("method"),
            contentType: 'application/json;charset=UTF-8',
            data  : JSON.stringify(getHours()),
            success: function(response){
                alert(response);
            },
        });
        return false;
     });
});


$(document).ready(function() {
    $("*").change(function() {
        $("td.mytd").each(function() {
            var h1 = parseInt($(this).find("input[name='begin_hour']").val());
            var h2 = parseInt($(this).find("input[name='end_hour']").val());
            var ev = $(this).find(":selected");
            if (isNaN(h1)===true) {
              h1 = 0;
            };
            if (isNaN(h2)===true) {
              h2 = 0;
            };
            var sumOfHours = h2 - h1;
            if (isNaN(sumOfHours)===true) {
              $(this).find("output[name='counted']").val(0);
            } else {
              $(this).find("output[name='counted']").val(sumOfHours);
            };
        });
    });
});


$(document).ready(function() {
    $(":input").change(function() {
        $("table.inner").each(function() {
            var h1 = $(this).find("input[name='begin_hour']");
            var h2 = $(this).find("input[name='end_hour']");
            var day = $(this).find("input[name='day']").val();
            var worker = $(this).find("input[name='worker']").val();
            var counted = $(this).find("output[name='counted']");
            var ev = $(this).find(":selected");

            if (ev.val()==="off" || ev.val()==="in_work") {
                $(this).css("background", "#fff");
                    h1.css("background", "#fff");
                    h2.css("background", "#fff");
                    ev.css("background", "#fff");
            } else if (ev.val()=="UW") {
                $(this).css("background", "#FC33FF");
                h1.css("background", "#FC33FF");
                h2.css("background", "#FC33FF");
                ev.css("background", "#FC33FF");
                h1.val("");
                h2.val(8);
            } else if (ev.val()==="UNŻ" || ev.val()==="UO" || ev.val()==="UOJ" || ev.val()==="UR") {
                if ((isNaN(parseInt(h1.val()))===true) || (isNaN(parseInt(h2.val()))===true)) {
                    alert(`Wpisz prawidłowe godziny pracy dla pracownika ${worker} w dniu ${day}.`);
                };
                $(this).css("background", "#FC33FF");
                h1.css("background", "#FC33FF");
                h2.css("background", "#FC33FF");
                ev.css("background", "#FC33FF");
            } else if (ev.val()==="L4") {
                $(this).css("background", "#80D332");
                h1.css("background", "#80D332");
                h2.css("background", "#80D332");
                ev.css("background", "#80D332");
            };
        });
    });
});