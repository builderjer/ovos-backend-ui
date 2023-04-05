var no_of_changes = 0;
var changes = [];
var needs_restart = 0;

function made_changes(element) {
    e = document.getElementById(element);
    if (changes.includes(element) == false) {
        changes.push(element);
        no_of_changes += 1;
    }
    check_for_changes();
}

function check_for_changes() {
    if (no_of_changes > 0) {
        if (no_of_changes == 1) {
            document.getElementById('backend_submit_button').value = "Apply " + no_of_changes + " change";
        }
        else {
            document.getElementById('backend_submit_button').value = "Apply " + no_of_changes + " changes";
        }
        document.getElementById('backend_submit_button').hidden = false;
    }
}

function change_location_override() {
    l = document.getElementById('override_location');
    g = document.getElementById('geolocate');
    if (l.checked) {
        g.checked = false;
        document.getElementById('location_button').hidden = false;
        document.getElementById('location_button_row').hidden = false;
    } else {
        document.getElementById('location_button').hidden = true;
        document.getElementById('location_button_row').hidden = true;
    }
    made_changes('override_location');
}

function change_geolocate() {
    l = document.getElementById('override_location');
    g = document.getElementById('geolocate');
    if (g.checked) {
        l.checked = false;
        document.getElementById('location_button').hidden = true;
        document.getElementById('location_button_row').hidden = true;
    }
    made_changes('geolocate')
}

