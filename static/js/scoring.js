var all_matches_api = `/${user_site_key}/api/match/all`
// var all_matches_api = `/wrong/api/match/all`

var match_dictionary = {};
var chosen_match;
var chosen_team;

function openErrorModal(message) {
    $("#error-message").text(message);
    $("#error-modal").modal();
}

function setUpMatchSelector(){
    // Watch for the change
    $("#matchID_selector").change(function (e) { 
        // e.preventDefault();
        chosen_match = $("#matchID_selector").val();
        if (chosen_match != -1) {
            // Set the options for pick team
            $("#team_number_selector").empty();
            $("#team_number_selector").append(`<option value=-1>Please chose your team</option>`);
            for (const [key, value] of Object.entries(match_dictionary[chosen_match])) {
                if (key.startsWith("red") || key.startsWith("blue")) {
                    option_text = `${value} (${key.replace("_", " ")})`;
                    $("#team_number_selector").append(`<option value=${value}>${option_text}</option>`);
                }
            }
            $("#pick_team_row").show();
        }
    });
}

function setupTeamSelector() {
    // Watch for the change
    $("#team_number_selector").change(function (e) { 
        // e.preventDefault();
        chosen_team = $("#team_number_selector").val();
        if (chosen_team != -1) {
            $("#scoring_controls").show();
        }
    });
}

// Load Matches function
function loadMatchList() {
    $.ajax({
        type: "GET",
        url: all_matches_api,
        dataType: "json",
        success: function (response) {
            // Change the placeholder
            $("#matchID_selector").empty();
            $("#matchID_selector").append(`<option value=-1>Please chose your match</option>`);
            // Convert the list to a dictionary
            response["data"].forEach((aMatch, index, array) => {
                matchID = aMatch["matchID"]
                match_name = aMatch["match_name"]
                match_dictionary[matchID] = aMatch;
                // Also set up the new options
                $("#matchID_selector").append(`<option value=${matchID}>${match_name}</option>`);                  
            });
        },
        error: function( jqXHR, textStatus, errorThrown ) {
            message = `loadMatchList failed because ${errorThrown}`;
            openErrorModal(message);
        }

    });
}

// Detect change to matches

// load teams for match

// auton/teleop selector

// score cone

// score cube

// balance charge station

// robot broke

///////  Review and submit
// tap to open review and submit

// Add auton cone
// remove auton cone

// Add auton cube
// remove auton cube

// auton charge button

// add teleop cone
// remove teleop cone

// add teleop cube
// remove teleop cube

// teleop charge button

// robot broke button

// submit scoring

$(document).ready(function() {
    // $( "#error-modal").dialog({
    //     modal: true,
    //     buttons: {
    //     Ok: function() {
    //         $( this ).dialog( "close" );
    //     }
    //     }
    // });

    // Setups
    setUpMatchSelector();
    setupTeamSelector();

    loadMatchList();

    
})