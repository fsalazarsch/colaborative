selected_tr = null;

function set_tr_selected(point_id){
    var tr = document.getElementById('tr_' + point_id);
    var td;
    var i;
    //unselect previous selected tr
    if (selected_tr != null){
        for (i=0; i<selected_tr.cells.length; i++){
            td = selected_tr.cells[i];
            td.style.borderTop = 'none';
            td.style.borderBottom = 'none';
        }

    }
    //if we didn't find the selected tr, there's nothing to do
    if (tr == null){
        return;
    }
    //select new selected tr
    selected_tr = tr;
    for (i=0; i<selected_tr.cells.length; i++){
            td = selected_tr.cells[i];
            td.style.borderTop = '3px solid red';
            td.style.borderBottom = '3px solid red';
        }
}

function scoreboard_loaded(){
    var selected_marker_id = parent.selected_marker_id;
    set_tr_selected(selected_marker_id);
}

function get_scoreboard_rows(){
    var table_score_board = document.getElementById('table_score_board');
    if (table_score_board != null){
        var number_of_rows = table_score_board.rows.length;
        return number_of_rows;
    } else {
        return 4;
    }
}

function add_row(a,b,c) {
    //var table_score_board = document.getElementById('table_score_board');
    string = '<tr><td>';
    string = string.concat(String(a));
    string = string.concat('</td><td>');
    string = string.concat(String(b));
    string = string.concat('</td><td>');
    string = string.concat(String(c));
    string = string.concat('</td></tr>');
    $('#table_score_board tr:last').after(string);
    }

