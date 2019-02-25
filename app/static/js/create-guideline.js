//gets data of all days in month and prepares dict for json
function getGuidelines() {
    let guidelines = [];
    let jsonDict = {};
    $("tr[class='main-tr']").each(function() {
        $(this).change();
    });
    $("tr[class='main-tr']").each(function() {
        let g = $(this).find("input[name='workers']").val()
        jsonDict[$(this).find("th[class='daynumber-th']").text()] = g
    });
    jsonDict["year"] = $("#cur-year").text()
    jsonDict["month"] = $("#cur-month").text()
    jsonDict["workplace"] = $("#workplace").text()
    return jsonDict
};

window.onload = function() {
//adds css to weekend rows (saturdays and sundays)
    $("th[class$='dayname-th']").each(function() {
        if ($(this).text() === "Sobota" || $(this).text() === "Niedziela") {
            $(this).closest("tr").find("*").css("background", "#aba5a5c7");
        };
    });
};

//submits guidelines
$(document).ready(function() {
    $("form").submit(function(e){
        let form = $(this);
        $.ajax({
            url   : form.attr("action"),
            type  : form.attr("method"),
            contentType: 'application/json;charset=UTF-8',
            data  : JSON.stringify(getGuidelines()),
            success: function(response){
                alert("Wytyczne wprowadzone");
                window.location.replace(response);
                }
        });
        return false;
    });
});

