// generates checkboxes with workers depending of chosen workplace
function workersCheckboxes() {
        workplace = $("#workplace").val();
        fetch("/shop-user-connect/" + workplace).then(function(response) {
            response.json().then(function(data) {
                let optionsHTML = "";
                for (let worker of data.workers) {
                console.log(worker.name.typeof)
                    optionsHTML += `<option value="${worker.name}">${worker.name}</option>`;
                };
                document.getElementById("worker").innerHTML = optionsHTML;
            });
        });
};


window.onload = function() {
    workersCheckboxes();
};

$(document).ready(function() {
    $("#workplace").change(function() {
        workersCheckboxes();
    });
});