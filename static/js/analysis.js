var team_results_api = `/${user_site_key}/api/team/results`
// var add_match_api = `/${admin_site_key}/api/match/add`
// var modify_match_api = `/${admin_site_key}/api/match/modify`

var editor; // use a global for the submit and return data rendering in the examples
var content;
var curr_preference = 1;

$(document).ready(function() {
    content = $('#Results').DataTable( {
        pageLength:50,
        order: [[3, "desc"]],
        dom: "Bfrtip",
        ajax: {
            contentType: 'application/json',
            url: team_results_api,
            },
        responsive: true,
        columns: [
            {
                data: "preference",
            },
            { 
                data: null,
                className: "dt-center pick-as-fave",
                defaultContent: '<i class="faveheart fa-regular fa-heart"></i>',
                orderable: false,
            },
            { data: "team_number" },
            { data: "matches_played" },
            {
                data:null,
                render: function (data, type, row) {
                    return data.total.scored_cone + data.total.scored_cube;
                }
            },
            { data: "total.scored_cone" },
            { data: "total.scored_cube" },
            { data: "total.balanced_charging_station" },
            { data: "total.robot_broke" },
            { data: "avg.scored_cone" },
            { data: "avg.scored_cube" },
            { data: "avg.balanced_charging_station" },
            { data: "avg.robot_broke" },
            { data: "Auton.scored_cone" },
            { data: "Auton.scored_cube" },
            { data: "Auton.balanced_charging_station" },
            {
                data: null,
                className: "dt-center chosen-for-alliance",
                defaultContent: '<i class="fa-regular fa-thumbs-up"></i>',
                orderable: false
            }
            // { data: "Auton.robot_broke" },
        ],
        select: false,
        buttons: [
                    {
                        text: "Only Favorites",
                        action: function (e, dt, node, config) {
                            $('#Results tbody tr').not(".favorited").hide();
                        }
                    },
                    {
                        text: "Show All",
                        action: function (e, dt, node, config) {
                            $('#Results tbody tr').show();
                        }
                    },
                    "csvHtml5",
                    //{ extend: "remove", editor: editor }
        ]
    } );

    $('#Results tbody').on('click', 'td.chosen-for-alliance', function () {
        $(this).parents('tr').hide()
    });

    $('#Results tbody').on('click', ".faveheart", function () {
        $(this).toggleClass("fa-solid");
        $(this).parents('tr').toggleClass("favorited");
        rowNum = $(this).parents('tr').prop("_DT_RowIndex");
        console.log(content.row(rowNum).data());
        curr_data = content.row(rowNum).data();
        curr_data["preference"] = curr_preference;
        content.row(rowNum).data(curr_data);
        curr_preference += 1;
    });
} );