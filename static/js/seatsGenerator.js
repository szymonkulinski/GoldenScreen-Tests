$(document).ready(function () {

    $('#btnAdd').click(function () {
        var count = 1,
            first_row = $('#Row2');
        while (count-- > 0) first_row.clone().appendTo('#blacklistgrid');
    });


    var myform = $('#blacklistgrid'),
        iter = 0;
    $('#btnAddCol').click(function () {
        myform.find('tr').each(function () {
            var trow = $(this);
            trow.append('<td><input type="checkbox" checked name="cb"/></td>');
        });
        iter += 1;
    });

    $('#btnRemCol').click(function () {
        $('#blacklistgrid tr').find('th:last-child, td:last-child').remove()
    });

    $('#btnRemRow').on("click", function () {
        $('#blacklistgrid tr:last').remove();
    })
});

function checkTable() {
    var table = document.getElementById("blacklistgrid");
    var tab = [];
    for (var i = 0, row; row = table.rows[i]; i++) {
        var obj = new Object;
        obj.index = i;
        obj.seats = [];
        for (var j = 0, col; col = row.cells[j]; j++) {
            var v2 = table.rows[i].cells[j];
            var checkbox = v2.getElementsByTagName("input")[0];
            var checked = checkbox.checked;
            var smolObj = new Object;
            smolObj.id = j;
            smolObj.isSeat = checked;
            smolObj.isTaken = false;
            smolObj.selected = false;
            obj.seats.push(smolObj);       
        }
        tab.push(obj);
    }
    var txt = JSON.stringify(tab);
    document.getElementById("id_seats").innerHTML = txt;
	if(txt.length <= 24){
		document.getElementById("sendInfo").style.color = 'red';
		document.getElementById("sendInfo").innerHTML = 'Błąd! Nie dodano żadnego miejsca.';
	}
	else{
		document.getElementById("sendInfo").style.color = 'white';
		document.getElementById("sendInfo").innerHTML = 'Siedzenia zapisane pomyślnie! W celu zapisania sali wciśnij przycisk SAVE.';
	}
}