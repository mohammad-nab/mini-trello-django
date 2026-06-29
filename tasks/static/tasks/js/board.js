const tasks = document.querySelectorAll(".task-card");
const taskLists = document.querySelectorAll(".task-list");

let draggedTask = null;

function getCookie(name) {
    let cookieValue = null;

    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");

        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();

            if (cookie.startsWith(name + "=")) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }

    return cookieValue;
}

tasks.forEach(task => {

    task.addEventListener("dragstart", function() {

        draggedTask = this;

        console.log(draggedTask);

    });

});


taskLists.forEach(list => {

    list.addEventListener("dragover", function (e) {
        e.preventDefault();
        this.classList.add("drag-over");
    });

    list.addEventListener("dragleave", function () {
        this.classList.remove("drag-over");
    });

    list.addEventListener("drop", function (e) {
        e.preventDefault();

        const taskId = draggedTask.dataset.taskId;
        const columnId = this.closest(".column").dataset.columnId;

        this.appendChild(draggedTask);

        fetch("/tasks/move-task/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCookie("csrftoken"),
            },
            body: JSON.stringify({
                task_id: taskId,
                column_id: columnId,
            }),
        });
    });

});
