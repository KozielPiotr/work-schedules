// generates list of schedules depending of chosen year and month
$(document).ready(function() {
    $("#find-schedules").click(function() {
        let year = $("#year").val();
        let month = $("#month").val();
        let workplace = $("#workplace").val();
        let action = $("form").attr("action")
        fetch("/filter-schedules/" + year + "/" + month + "/" + workplace + "/" + action).then(function(response) {
            response.json().then(function(data) {
                let listHTML = "";
                if (data.option === 1) {
                    for (let schedule of data.schedules) {
                    let sName = schedule.name.replace(" ","+");
                    listHTML += `<a href="${schedule.url}"`+
                                `class="list-group-item list-group-item-action">`+
                                `${schedule.workplace} na ${schedule.month}.${schedule.year} v_${schedule.version}`+
                                `</a>`
                    };
                } else if (data.option === 0) {
                    listHTML = "Brak grafików do wyświetlenia";
                };

                document.getElementById("list").innerHTML = listHTML;
            });
        });
    });
});