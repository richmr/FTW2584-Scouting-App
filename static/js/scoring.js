var all_matches_api = `/${user_site_key}/api/match/all`
var all_teams_api = `/${user_site_key}/api/team/allteams`
var addmanyactions_api = `/${user_site_key}/api/actions/addmanyactions`
var addmanyactions_api_bad = `/${user_site_key}/api/actions/addmanyactions_bad`

// var all_matches_api = `/wrong/api/match/all`

var match_dictionary = {};
var chosen_match;
var chosen_team;
var current_mode;
var posted_data_str;
var scoring_data;
var all_teams;

function openErrorModal(message) {
    $("#error-message").text(message);
    $("#error-modal").modal();
}

function greenFeedback(selector) {
    // Flash green and then white
    $(selector).addClass("lgreen-background");
        setTimeout(() => {
            $(selector).removeClass("lgreen-background");
          }, 100);
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
                if (value == -1) {
                    // We don't know what teams were scheduled, empty an replace all
                    $("#team_number_selector").empty();
                    $("#team_number_selector").append(`<option value=-1>Please chose your team</option>`);
                    all_teams.forEach((aTeam_number, index, array) => {
                        $("#team_number_selector").append(`<option value=${aTeam_number}>${aTeam_number}</option>`);
                    });
                    // Quit processing
                    break;
                }
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
        greenFeedback("#open-review-submit")
        $("#review_submit_details").toggle();
        $("#submit_scoring").get(0).scrollIntoView();
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
            $("#matchID_selector").append(`<option value=-1>Please choose your match</option>`);
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

function loadAllTeams() {
    all_teams = [];
    $.ajax({
        type: "GET",
        url: all_teams_api,
        dataType: "json",
        success: function (response) {
            response["data"].forEach((aTeam, index, array) => {
                all_teams.push(aTeam["team_number"]);                                  
            });
        },
        error: function( jqXHR, textStatus, errorThrown ) {
            message = `loadAllTeams failed because ${errorThrown}`;
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
        greenFeedback("#score_cone_background");
       
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
        greenFeedback("#score_cube_background");
        
    });
}

// balance charge station
function setupBalanceButton_scoring() {
    $("#charge-balanced").click(function (e) {
        $(`#${current_mode}_charge_balance`).text("Yes").addClass("button-green");
        greenFeedback("#charge-balanced-background")
      })

      $("#entered-charge").click(function (e) {
        $(`#${current_mode}_entered_charge`).text("Yes").addClass("button-green");
        greenFeedback("#entered-charge-background")
      })
}

// mobility
function setupBrokeButton_scoring() {
    $("#robot-broke").click(function (e) {
        $(`#robot_broke_button`).text("Yes").addClass("button-red");
        greenFeedback("#robot-broke-background")
      })
}

// robot broke
function setupMobility_scoring() {
    $("#mobility").click(function (e) {
        $(`#mobility_button`).text("Yes").addClass("button-green");
        greenFeedback("#mobility-background")
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

    $("#Auton_entered_charge").click(function (e) { 
        if ($("#Auton_entered_charge").text() == "Yes") {
            $("#Auton_entered_charge").text("No");
        } else {
            $("#Auton_entered_charge").text("Yes");
        }
        $("#Auton_entered_charge").toggleClass("button-green");
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

    $("#Teleop_entered_charge").click(function (e) { 
        if ($("#Teleop_entered_charge").text() == "Yes") {
            $("#Teleop_entered_charge").text("No");
        } else {
            $("#Teleop_entered_charge").text("Yes");
        }
        $("#Teleop_entered_charge").toggleClass("button-green");
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

function setupMobilityButton() {
    $("#mobility_button").click(function (e) { 
        if ($("#mobility_button").text() == "Yes") {
            $("#mobility_button").text("No");
        } else {
            $("#mobility_button").text("Yes");
        }
        $("#mobility_button").toggleClass("button-green");
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
    //***** label IDs are hard coded!  If you change the DB, these need to be updated. 
    list_of_scores_to_convert = [
        {
            "selector":"#Auton_cones_scored",
            "action_label":"scored_cone",
            "actionID":10,
            "mode_name":"Auton",
            "modeID":1,
            "count_conversion":parseInt,
        },
        {
            "selector":"#Auton_cubes_scored",
            "action_label":"scored_cube",
            "actionID":11,
            "mode_name":"Auton",
            "modeID":1,
            "count_conversion":parseInt,
        },
        {
            "selector":"#Auton_entered_charge",
            "action_label":"entered_charging_station",
            "actionID":7,
            "mode_name":"Auton",
            "modeID":1,
            "count_conversion":textToCount,
        },
        {
            "selector":"#mobility_button",
            "action_label":"mobility",
            "actionID":13,
            "mode_name":"Auton",
            "modeID":1,
            "count_conversion":textToCount,
        },
        {
            "selector":"#Auton_charge_balance",
            "action_label":"balanced_charging_station",
            "actionID":8,
            "mode_name":"Auton",
            "modeID":1,
            "count_conversion":textToCount,
        },
        {
            "selector":"#Teleop_cones_scored",
            "action_label":"scored_cone",
            "actionID":10,
            "mode_name":"Tele",
            "modeID":2,
            "count_conversion":parseInt,
        },
        {
            "selector":"#Teleop_cubes_scored",
            "action_label":"scored_cube",
            "actionID":11,
            "mode_name":"Tele",
            "modeID":2,
            "count_conversion":parseInt,
        },
        {
            "selector":"#Teleop_entered_charge",
            "action_label":"entered_charging_station",
            "actionID":7,
            "mode_name":"Tele",
            "modeID":2,
            "count_conversion":textToCount,
        },
        {
            "selector":"#Teleop_charge_balance",
            "action_label":"balanced_charging_station",
            "actionID":8,
            "mode_name":"Tele",
            "modeID":2,
            "count_conversion":textToCount,
        },
        {
            "selector":"#robot_broke_button",
            "action_label":"robot_broke",
            "actionID":9,
            "mode_name":"Tele",
            "modeID":2,
            "count_conversion":textToCount
        }
    ];
    scoring_data = {
        matchID:chosen_match,
        team_number:chosen_team,
        // Put the team competed in here
        scored_items:[{
            action_label:"team_competed",
            mode_name:"Tele",
            count_seen:1
        }]
    }
    list_of_scores_to_convert.forEach((score_fmt, index, array) => {
        count_seen = score_fmt.count_conversion($(score_fmt.selector).text())
        if (count_seen > 0) {
            this_score_data = {
                action_label:score_fmt.action_label,
                mode_name:score_fmt.mode_name,
                count_seen:count_seen
            }
            scoring_data.scored_items.push(this_score_data);
        }
    });
    $("#sending_data_modal").modal({
        escapeClose: false,
        clickClose: false,
        showClose: false
    });

    posted_data_str = JSON.stringify(scoring_data)
    $.ajax({
        type: "POST",
        url: addmanyactions_api,
        data: posted_data_str,
        dataType: "json",
        contentType: 'application/json',
        success: function (response) {
            $("#sending_data_modal_title").text('Success!');
            $("#submit_message").text("Data saved to central database.");
            $("#data_modal_buttons").show();
            // Reset values?  Reload page? 
        },
        error: qr_code_results,
        timeout: 5000 
    });
}

function qr_code_results(jqXHR, textStatus, errorThrown) {
    $("#sending_data_modal_title").text('Error');
    alreadySubmitted = false;
    if (jqXHR === undefined) {
        $("#submit_message").text("I could not save the data to the central DB");
    } else if (jqXHR.responseJSON === undefined) {
        $("#submit_message").text("I could not save the data to the central DB");
    } else {
        $("#submit_message").text("I could not save the data to the central DB because: "+jqXHR.responseJSON.detail);
        if (jqXHR.responseJSON.detail.search("already submitted for this match") > -1) {
            // Then we don't show a QR code
            alreadySubmitted = true;
        }
    }
    query_string = `${scoring_data.matchID}|${scoring_data.team_number}`
    scoring_data.scored_items.forEach(e => {
        query_string += `|${e.action_label}|${e.mode_name}|${e.count_seen}`        
    });
    link = `${window.location.origin}${addmanyactions_api}?action_obj=${query_string}`
    console.log(link)
    if (!alreadySubmitted) {
        $("#actual_qr_code").empty()
        new QRCode(document.getElementById("actual_qr_code"), link);
        // $("#results_qr_code").html(link)
        $("#results_qr_code").show();
        $("#qr_code_text").show();
    }
    $("#data_modal_buttons").show();

}

function setupModalCloseButton() {
    $("#close_modal_next_match").click(function (e) { 
        // Reset data
        chosen_match = null;
        chosen_team = null;
        current_mode = null;
        posted_data_str = null;
        scoring_data = null;
        // Reset the tabulated scoring data
        $("#Auton_cones_scored").text(0);
        $("#Auton_cubes_scored").text(0);
        $("#Auton_entered_charge").text("No").removeClass("button-green");
        $("#Auton_charge_balance").text("No").removeClass("button-green");
        $("#mobility_button").text("No").removeClass("button-green");
        $("#Teleop_cones_scored").text(0);
        $("#Teleop_cubes_scored").text(0);
        $("#Teleop_entered_charge").text("No").removeClass("button-green");
        $("#Teleop_charge_balance").text("No").removeClass("button-green");
        $("#robot_broke_button").text("No").removeClass("button-red");
        // Hide things
        $("#review_submit_details").hide();
        $("#review_and_submit").hide();
        $("#scoring_controls").hide();
        $("#pick_team_row").hide();
        $("#results_qr_code").hide();
        $("#data_modal_buttons").hide();
        $("#qr_code_text").hide();
        //Reset selectors
        $("#matchID_selector").val(-1);
        $("#team_number_selector").val(-1);
        // reset game mode
        $("#set-auton").click();

        // close it
        $.modal.close();
    });
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
    setupMobility_scoring();
    setupBrokeButton_scoring();
    setupAutonCone_mod();
    setupAutonCube_mod();
    setupAutonChargeButton();
    setupTeleopCone_mod();
    setupTeleopCube_mod();
    setupTeleopChargeButton();
    setupRobotBrokeButton();
    setupMobilityButton();
    setupSubmitButton();

    setupModalCloseButton();

    loadMatchList();
    loadAllTeams();

    
})
