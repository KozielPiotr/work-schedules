function getHours() {
    var hours = [];
    var jsonDict = {};
    var praca = "";
    $("table.inner").each(function() {
        var dzien = $(this).find("input[name='dzien']").val();
        var czlowiek = $(this).find("input[name='czlowiek']").val();
        var hrs = $(this).find("input[name='godziny']").val();
        var hrs2 = $(this).find("input[name='godziny2']").val();
        var wrkd = $(this).find("output[name='counted']").val();
        hours.push({"dzień": dzien, "czlowiek": czlowiek, "od": hrs, "do": hrs2, "w sumie": wrkd});
    });
    jsonDict[praca] = hours;
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
            var h1 = parseInt($(this).find("input[name='godziny']").val());
            var h2 = parseInt($(this).find("input[name='godziny2']").val());
            if (isNaN(h1) === true) {
              h1 = 0;
            };
            if (isNaN(h1)===true) {
              h2 = 0;
            };
            var sumOfHours = h2 - h1;
            if (isNaN(sumOfHours) === true) {
              $(this).find("output[name='counted']").val(0);
            } else {
              $(this).find("output[name='counted']").val(sumOfHours);
            };
        });
    });
});