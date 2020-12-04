// Driver Function, waits for DOM build
$(document).ready(function () {
    displayTodaysDate();
    buttonHandling();
});

// Initialises listeners for all buttons in the page
function buttonHandling() {
    $("#addTicketBtn").on("click", function () {
        addTicket();
    });
    $("#addCommentBtn").on("click", function () {
        addComment();
    });

    $('.ticketViewBtn').on("click", function () {
        // $(this) refers to button that was clicked
        const id = $(this).attr('id');
        // should return edit | share | trash | comp
        const result = id.split("_");
        const uuid = result[1];
        viewTicket(uuid);
    });

    $('.ticketBtn').on("click", function () {
        handleButtonClick($(this));
    });
}

// Displays quick notification
function toast(type, title) {
    const Toast = Swal.mixin({
        toast: true,
        position: 'top',
        showConfirmButton: false,
        timer: 3000
    });

    // Types: warning|success|info|
    Toast.fire({
        icon: type,
        title: title
    })
}

function getAllTickets() {
    $.ajax({
        type: "GET",
        url: '/',
        success: function (content) {
            // console.log(content);
            $('#tickets').html(content);
            buttonHandling();
        },
        error: function () {
            toast("error", "Could not add. Error occurred");
        }
    });
    return false;
}

// Adds a ticket
function addTicket() {
    var form = $("#addTicketForm");
    form.submit(function (e) {
        // Avoid to execute the actual submit of the form.
        e.preventDefault();
        // Avoid submit twice
        e.stopImmediatePropagation();

        $.ajax({
            type: "POST",
            data: form.serialize(),
            url: "/",
            success: function (content) {
                toast("success", "Added successfully.");

                getAllTickets();
                buttonHandling();
            },
            error: function () {
                toast("error", "Could not add. Error occurred");
            }
        });

        return false;
    });
}

// Adds a comment
function addComment() {
    var form = $("#addCommentForm");
    form.submit(function (e) {
        // Avoid to execute the actual submit of the form.
        e.preventDefault();
        // Avoid submit twice
        e.stopImmediatePropagation();
        serializedForm = form.serialize();

        $.ajax({
            type: "POST",
            data: serializedForm + "&bugTicket=" + form[0].dataset.parentticketid,
            url: "/addComment/",
            success: function (content) {
                $('#commentList').children().prepend(content);
                toast("success", "Added successfully.");
            },
            error: function () {
                toast("error", "Could not add. Error occurred");
            }
        });

        return false;
    });
}


function viewTicket(uuid) {
    $.ajax({
        type: "GET",
        url: "/" + uuid,
        success: function (content) {
            $('#tickets').html(content);
            buttonHandling();
        },
        error: function () {
            toast("error", "Could not add. Error occurred");
        }
    });
}


// Redirects the button that was clicked to the corresponding function
function handleButtonClick(buttonClicked) {
    // $(this) refers to button that was clicked
    const id = $(buttonClicked).attr('id');
    // should return edit | share | trash | comp
    const result = id.split("_");
    const uuid = result[0];
    const buttonRole = result[1];


    console.log("Id:", uuid, "Role:", buttonRole);

    switch (buttonRole) {
        case "edit":
            doEdit(uuid);
            break;
        case "trash":
            doTrash(uuid);
            break;
        case "closeView":
            getAllTickets();
            break;
    }
}

// Enables editing of ticket in conjunction with showEditDialog function
function doEdit(uuid) {
    $.ajax({
        type: "GET",
        url: "/updateTicket/" + uuid,
        success: function (updateFormFromServer) {
            console.log("ticket: ", updateFormFromServer);
            // Displays the dialog for editing a ticket with given parameters
            Swal.fire({
                showCancelButton: true,
                titleText: "Edit this bug ticket?",
                html: updateFormFromServer,
                focusConfirm: false,
                confirmButtonText: '<i class="fas fa-edit fa-lg"></i>',
                buttonsStyling: false,
                focusCancel: true,
                allowEnterKey: false,
                allowOutsideClick: false,
                customClass: {
                    confirmButton: 'btn btn-primary col btn-dialog-css',
                    cancelButton: 'btn btn-default col btn-dialog-css',
                    actions: 'actions-class'
                },
                preConfirm: function () {
                    $.ajax({
                        type: "POST",
                        data: $("#updateTicketForm").serialize(),
                        url: "/updateTicket/" + uuid + "/",
                        success: function () {
                            viewTicket(uuid);
                            toast("success", "Updated successfully")
                        },
                        error: function () {
                            toast("error", "Could not update. Error occurred");
                        }
                    });
                }
            });
        },
        error: function () {
            toast("error", "Could not edit. Error occurred");
        }
    });
}

// Handles deleting of ticket
function doTrash(uuid) {
    $.ajax({
        type: "GET",
        url: "/deleteTicket/" + uuid + "/",
        success: function (csrfFromServer) {
            Swal.fire({
                title: "Delete this ticket?",
                type: 'warning',
                showCancelButton: true,
                confirmButtonText: '<i class="fas fa-trash-alt fa-lg"></i>',
                buttonsStyling: false,
                focusConfirm: false,
                width: "22rem",
                customClass: {
                    confirmButton: 'btn btn-primary col btn-dialog-css',
                    cancelButton: 'btn btn-default col btn-dialog-css',
                    actions: 'actions-class'
                }
            }).then((result) => {
                if (result.value) {
                    var doc = new DOMParser().parseFromString(csrfFromServer, "text/xml");
                    $.ajax({
                        type: "POST",
                        data: {'csrfmiddlewaretoken': doc.firstChild.getAttribute("value")},
                        url: "/deleteTicket/" + uuid + "/",
                        success: function (content) {
                            getAllTickets();
                            toast("success", "Deleted successfully");
                        },
                        error: function () {
                            toast("error", "Could not delete. Error occurred");
                        }
                    });
                }
            });
        }
    });
}



// Returns formatted date as ddd, dd/mm/yyyy
function formatMSDate(date) {
    return new Date(date).format("ddd, dd/mm/yyyy");
}

// Formats all dates in the ticket list
function formatDueDates() {
    $("#ticket-list p").each(function (i, elem) {
        console.log(formatMSDate($(elem).text()));

        $(elem).text(formatMSDate($(elem).text()))
    });
}

// Formatted date
function displayTodaysDate() {
    $("#formattedDate")[0].innerText = dayjs().format('dddd, D MMM YYYY');
}

// Returns formatted date as ISO standard date format
function getISODate(date) {
    const dueDate = new Date();
    const curDate = dueDate.getDate();
    const month = dueDate.getMonth();
    const year = dueDate.getFullYear();

    // Adds 0 in front for less than 10 numbers
    function addZero(n) {
        return n < 10 ? '0' + n : n
    }

    return year + "-" + addZero(month + 1) + "-" + addZero(curDate);
}