var all_matches_api = `/${user_site_key}/api/match/all`
var addmanyactions_api = `/${user_site_key}/api/actions/addmanyactions`
var addmanyactions_api_bad = `/${user_site_key}/api/actions/addmanyactions_bad`

// var all_matches_api = `/wrong/api/match/all`

var match_dictionary = {};
var chosen_match;
var chosen_team;
var current_mode;
var posted_data_str;
var scoring_data;

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
            $("#review_and_submit").show()
        }
    });
}

function setupReviewAndSubmit() {
    $("#open-review-submit").click(function () {
        $("#review_submit_details").toggle();
    })
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


// auton/teleop selector
function setupModeSelector() {
    current_mode = "Auton";
    $("#set-auton").addClass("lgreen-background");
    $("#set-auton").click(function (e) { 
        current_mode = "Auton";
        $("#set-auton").addClass("lgreen-background");
        $("#set-teleop").removeClass("lgreen-background")        
    });
    $("#set-teleop").click(function (e) { 
        current_mode = "Teleop";
        $("#set-teleop").addClass("lgreen-background");
        $("#set-auton").removeClass("lgreen-background")        
    });
}

// score cone
function setupConeScore() {
    $("#score_cone").click(function (e) { 
        // Score ID
        scoreID = `#${current_mode}_cones_scored`;
        // Add to the score
        current_score = parseInt($(scoreID).text());
        current_score += 1;
        // console.log(`setting score for ${current_mode} to ${current_score}`);
        $(scoreID).text(current_score);
        $("#score_cone_background").addClass("lgreen-background");
        setTimeout(() => {
            $("#score_cone_background").removeClass("lgreen-background");
          }, 100);
    });
}
// score cube
function setupCubeScore() {
    $("#score_cube").click(function (e) { 
        // Score ID
        scoreID = `#${current_mode}_cubes_scored`;
        // Add to the score
        current_score = parseInt($(scoreID).text());
        current_score += 1;
        // console.log(`setting score for ${current_mode} to ${current_score}`);
        $(scoreID).text(current_score);
        $("#score_cube_background").addClass("lgreen-background");
        setTimeout(() => {
            $("#score_cube_background").removeClass("lgreen-background");
          }, 100);
    });
}

// balance charge station
function setupBalanceButton_scoring() {
    $("#charge-balanced").click(function (e) {
        $(`#${current_mode}_charge_balance`).text("Yes").addClass("button-green");
      })
}

// robot broke
function setupBrokeButton_scoring() {
    $("#robot-broke").click(function (e) {
        $(`#robot_broke_button`).text("Yes").addClass("button-red");
      })
}
///////  Review and submit

// Add auton cone
// remove auton cone
function setupAutonCone_mod() {
    $("#add_auton_cone").click(function (e) { 
        // Score ID
        scoreID = `#Auton_cones_scored`;
        // Add to the score
        current_score = parseInt($(scoreID).text());
        current_score += 1;
        // console.log(`setting score for ${current_mode} to ${current_score}`);
        $(scoreID).text(current_score);
    });
    $("#remove_auton_cone").click(function (e) { 
        // Score ID
        scoreID = `#Auton_cones_scored`;
        // Add to the score
        current_score = parseInt($(scoreID).text());
        if (current_score == 0) {
            // Do nothing
            return
        }
        current_score -= 1;
        // console.log(`setting score for ${current_mode} to ${current_score}`);
        $(scoreID).text(current_score);
    });
}

// Add auton cube
// remove auton cube
function setupAutonCube_mod() {
    $("#add_auton_cube").click(function (e) { 
        // Score ID
        scoreID = `#Auton_cubes_scored`;
        // Add to the score
        current_score = parseInt($(scoreID).text());
        current_score += 1;
        // console.log(`setting score for ${current_mode} to ${current_score}`);
        $(scoreID).text(current_score);
    });
    $("#remove_auton_cube").click(function (e) { 
        // Score ID
        scoreID = `#Auton_cubes_scored`;
        // Add to the score
        current_score = parseInt($(scoreID).text());
        if (current_score == 0) {
            // Do nothing
            return
        }
        current_score -= 1;
        // console.log(`setting score for ${current_mode} to ${current_score}`);
        $(scoreID).text(current_score);
    });
}

// auton charge button
function setupAutonChargeButton() {
    $("#Auton_charge_balance").click(function (e) { 
        if ($("#Auton_charge_balance").text() == "Yes") {
            $("#Auton_charge_balance").text("No");
        } else {
            $("#Auton_charge_balance").text("Yes");
        }
        $("#Auton_charge_balance").toggleClass("button-green");
    });
}

// add teleop cone
// remove teleop cone
function setupTeleopCone_mod() {
    $("#add_teleop_cone").click(function (e) { 
        // Score ID
        scoreID = `#Teleop_cones_scored`;
        // Add to the score
        current_score = parseInt($(scoreID).text());
        current_score += 1;
        // console.log(`setting score for ${current_mode} to ${current_score}`);
        $(scoreID).text(current_score);
    });
    $("#remove_teleop_cone").click(function (e) { 
        // Score ID
        scoreID = `#Teleop_cones_scored`;
        // Add to the score
        current_score = parseInt($(scoreID).text());
        if (current_score == 0) {
            // Do nothing
            return
        }
        current_score -= 1;
        // console.log(`setting score for ${current_mode} to ${current_score}`);
        $(scoreID).text(current_score);
    });
}
// add teleop cube
// remove teleop cube
function setupTeleopCube_mod() {
    $("#add_teleop_cube").click(function (e) { 
        // Score ID
        scoreID = `#Teleop_cubes_scored`;
        // Add to the score
        current_score = parseInt($(scoreID).text());
        current_score += 1;
        // console.log(`setting score for ${current_mode} to ${current_score}`);
        $(scoreID).text(current_score);
    });
    $("#remove_teleop_cube").click(function (e) { 
        // Score ID
        scoreID = `#Teleop_cubes_scored`;
        // Add to the score
        current_score = parseInt($(scoreID).text());
        if (current_score == 0) {
            // Do nothing
            return
        }
        current_score -= 1;
        // console.log(`setting score for ${current_mode} to ${current_score}`);
        $(scoreID).text(current_score);
    });
}
// teleop charge button
function setupTeleopChargeButton() {
    $("#Teleop_charge_balance").click(function (e) { 
        if ($("#Teleop_charge_balance").text() == "Yes") {
            $("#Teleop_charge_balance").text("No");
        } else {
            $("#Teleop_charge_balance").text("Yes");
        }
        $("#Teleop_charge_balance").toggleClass("button-green");
    });
}

// robot broke button
function setupRobotBrokeButton() {
    $("#robot_broke_button").click(function (e) { 
        if ($("#robot_broke_button").text() == "Yes") {
            $("#robot_broke_button").text("No");
        } else {
            $("#robot_broke_button").text("Yes");
        }
        $("#robot_broke_button").toggleClass("button-red");
    });
}

// submit scoring
function setupSubmitButton() {
    $("#submit_scoring").click(function (e) {
        // Disarm the button
        $("#submit_scoring").click(false);
        // Send it
        network_submit();
    });

}

function textToCount(text_in) {
    // Converts a "Yes" or "yes" to a int 1
    // otherwise returns 0
    if (text_in.toUpperCase() == "YES") {
        return 1;
    } else {
        return 0;
    }
}

function network_submit() {
    // Build the scoring messages
    list_of_scores_to_convert = [
        {
            "selector":"#Auton_cones_scored",
            "action_label":"scored_cone",
            "mode_name":"Auton",
            "count_conversion":parseInt,
        },
        {
            "selector":"#Auton_cubes_scored",
            "action_label":"scored_cube",
            "mode_name":"Auton",
            "count_conversion":parseInt,
        },
        {
            "selector":"#Auton_charge_balance",
            "action_label":"balanced_charging_station",
            "mode_name":"Auton",
            "count_conversion":textToCount,
        },
        {
            "selector":"#Teleop_cones_scored",
            "action_label":"scored_cone",
            "mode_name":"Tele",
            "count_conversion":parseInt,
        },
        {
            "selector":"#Teleop_cubes_scored",
            "action_label":"scored_cube",
            "mode_name":"Tele",
            "count_conversion":parseInt,
        },
        {
            "selector":"#Teleop_charge_balance",
            "action_label":"balanced_charging_station",
            "mode_name":"Tele",
            "count_conversion":textToCount,
        },
        {
            "selector":"#robot_broke_button",
            "action_label":"robot_broke",
            "mode_name":"Tele",
            "count_conversion":textToCount
        }
    ];
    scoring_data_to_send = []
    list_of_scores_to_convert.forEach((score_fmt, index, array) => {
        this_score_data = {
            matchID:chosen_match,
            team_number:chosen_team,
            action_label:score_fmt.action_label,
            mode_name:score_fmt.mode_name,
            count_seen: score_fmt.count_conversion($(score_fmt.selector).text())
        };
        scoring_data_to_send.push(this_score_data);
    });
    $("#sending_data_modal").modal();
    posted_data_str = JSON.stringify(scoring_data_to_send)
    $.ajax({
        type: "POST",
        url: addmanyactions_api_bad,
        data: posted_data_str,
        dataType: "json",
        contentType: 'application/json',
        success: function (response) {
            $("#sending_data_modal_title").text('Success!');
            $("#submit_message").text("Data saved to central database.");
            // Reset values?  Reload page? 
        },
        error: qr_code_results
    });
}

function qr_code_results(jqXHR, textStatus, errorThrown) {
    $("#sending_data_modal_title").text('Error');
    $("#submit_message").text("I could not save the data to the central DB because: "+jqXHR.responseJSON.detail);
    link = `${window.location.origin}${addmanyactions_api}?action_obj=${posted_data_str}`
    console.log(link)
    new QRCode(document.getElementById("results_qr_code"), link);
    // $("#results_qr_code").html(link)
    $("#results_qr_code").toggle();
}


$(document).ready(function() {
    

    // Setups
    setUpMatchSelector();
    setupTeamSelector();
    setupReviewAndSubmit();
    setupModeSelector();
    setupConeScore();
    setupCubeScore();
    setupBalanceButton_scoring();
    setupBrokeButton_scoring();
    setupAutonCone_mod();
    setupAutonCube_mod();
    setupAutonChargeButton();
    setupTeleopCone_mod();
    setupTeleopCube_mod();
    setupTeleopChargeButton();
    setupRobotBrokeButton();
    setupSubmitButton();

    loadMatchList();

    
})