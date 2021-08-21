//webkitURL is deprecated but nevertheless
URL = window.URL || window.webkitURL;

var doc_id = null
var uploadButton = document.getElementById("uploadButton");

$(document).ready(function() {
    $('#choose_file').click(function () {
	    document.querySelector("#text").innerHTML = ""
    });
    });

    
$(document).ready(function() {
    $('#editResp').click(function () {
        console.log('Redirecting...')
        editUrl = '127.0.0.0:5555'
        editUrl = editUrl+doc_id
        location.replace(editUrl)
    });
});

$(document).ready(function() {
    $('#submitButton').click(function ()
    {

        var data = new FormData();
        var test_name = document.getElementById("test_name").value
        var unit = document.getElementById("unit").value
        var specimen = document.getElementById("specimen").value
        var method = document.getElementById("method").value

        data.append('test_name',test_name);
        data.append("unit", unit);
        data.append("specimen", specimen);
        data.append("method", method);

        $.ajax({
	        url: 'http://172.31.28.156:8089/get_prediction',
            processData: false,
            contentType: false,
            data: data,
            type: 'POST'
        }).done(function(data)
        {
            var json_data = data;
            GenerateTable(json_data)

	})
    });
});


function GenerateTable(data) {
        console.log(data)
        //Build an array containing Customer records.
        //Create a HTML Table element.
        if (data['status'] === 'success')
        {
            var data_pred = data['prediction']
            var table = document.createElement("TABLE");

            var table = document.createElement("TABLE");
            table.border = "1";


            var keys = ['loinc', 'component', 'property', 'system', 'method']
            var columnCount = keys.length;
            var row = table.insertRow(-1);
            for (var i = 0; i < keys.length; i++) {
                var headerCell = document.createElement("TH");
                headerCell.innerHTML = keys[i];
                row.appendChild(headerCell);
            }

            for (var test_row in data_pred['candidates']) {
                row = table.insertRow(-1);
                for (var j = 0; j < keys.length; j++) {
                    if (keys[j] in data_pred['candidates'][test_row]) {
                        var cell = row.insertCell(-1);
                        if ((keys[j] == 'loinc')){
                            html = '<a href="'+data_pred['candidates'][test_row]['loinc_url']+'">'+data_pred['candidates'][test_row][keys[j]]+'</a>';
                        }
                        else {
                            html = data_pred['candidates'][test_row][keys[j]];
                        }

                        cell.innerHTML = html;
                    }
                    else {
                        var cell = row.insertCell(-1);
                        cell.innerHTML = null;
                    }
                }
            }

            var dvTable = document.getElementById("Table");
            dvTable.innerHTML = "";
            dvTable.appendChild(table);
        }

    }
