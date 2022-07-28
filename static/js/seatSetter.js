var seats = [];
var seatsForPrinting = [];

$(document).ready(function () {
    $("input:checked").prev().addClass("checked");
    countSeats();
    printPickedSeats();
});


$('.colorSwap').click(function () {
    if (!$(this).prev().hasClass("taken")) {
        $(this).prev().toggleClass("checked");
    }
    if($(this).prev().hasClass("checked")) {
        seats.push(this.value);
    }
    if(!$(this).prev().hasClass("checked")) {
        const removeIndex = seats.indexOf(this.value);
        if(removeIndex > -1) {
            seats.splice(removeIndex, 1);
        }
    }
    countSeats();
    printPickedSeats();
});

function countSeats(){
    if ($("#myTable input:checkbox:checked").length > 0 && $("#myTable input:checkbox:checked").length <= 8) 
    {
        if($("#myTable input:checkbox:checked").length <= 4){
            $('#taken').text($("#myTable input:checkbox:checked").length + " zajęte miejsca");
        }
        else{
            $('#taken').text($("#myTable input:checkbox:checked").length + " zajętych miejsc");
        }
        $('#btncheck').prop('disabled', false);
    }
    else if($("#myTable input:checkbox:checked").length == 0)
    {
        $('#taken').text("Brak zajętych miejsc");
        $('#btncheck').prop('disabled', true);
    }
    
    else {
        if($("#myTable input:checkbox:checked").length > 8){
            $('#taken').text("Możesz zarezerwować maksymalnie 8 miejsc!");
        }

        $('#btncheck').prop('disabled', true);
    }
}

function printPickedSeats() {
    seats.sort();
    var prev = -1;
    var stringDis = "";
    seats.forEach(seat => {
        var row = parseInt(seat.substr(0, seat.indexOf("."))) + 1;
        var col = parseInt(seat.substr(seat.indexOf(".") + 1)) + 1;

        if(prev == row) {
            stringDis +=  ", " + col + "";
        }
        else {
            stringDis += "<h4>Rząd " + row + "</h4>";
            stringDis += "Siedzenia: " + col;
            prev = parseInt(seat.substr(0, seat.indexOf("."))) + 1;
        }
    });
    $("#seats").html(stringDis);
}