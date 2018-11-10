// generates checkboxes with workers depending of chosen workplace
function workersCheckboxes() {
        workplace = $("#workplace").val();
        console.log(workplace);
        fetch("/new-schedule/" + workplace).then(function(response) {
            response.json().then(function(data) {
                let checkboxesHTML = "";
                let workerNumber = 0
                for (let worker of data.workers) {
                    checkboxesHTML += `<li class="list-group-item"><input id="worker-${workerNumber}" name="workers" type="checkbox" value="${worker.name}" checked> <label for="worker-${workerNumber}">${worker.name}</label></li><br>`;
                    workerNumber += 1;
                };
                document.getElementById("workers").innerHTML = checkboxesHTML;
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

