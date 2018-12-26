// generates list of schedules depending of chosen year and month
$(document).ready(function() {
    $("#find-schedules").click(function() {
        console.log("AAA")
        let year = $("#year").val();
        let month = $("#month").val();
        let workplace = $("#workplace").val();
        fetch("/filter_schedules/" + year + "/" + month + "/" + workplace).then(function(response) {
            response.json().then(function(data) {
                let listHTML = "";
                console.log(data.schedules)
                if (data.option === 1) {
                    for (let schedule of data.schedules) {
                    console.log(schedule);
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