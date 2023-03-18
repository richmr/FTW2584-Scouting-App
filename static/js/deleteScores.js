var all_scores_api = `/${user_site_key}/api/scores/getall`;
var delete_scores_api = `/${admin_site_key}/api/scores/delete`;

var editor; // use a global for the submit and return data rendering in the examples
 
$(document).ready(function() {
    
    editor = new $.fn.dataTable.Editor( {
        ajax: {
            remove: {
                contentType: 'application/json',
                type: "GET",
                data: function ( d ) {
                        data_obj = d["data"];
                        var tosend = {}
                        for (const [key, value] of Object.entries(data_obj)) {
                            tosend["team_number"] = value["team_number"];
                            tosend["matchID"] = value["matchID"]
                        }
                        return tosend
                    },
                url: delete_scores_api,
            }, 
        },
        idSrc: "rowID",
        table: "#RecordedScores",
        
    } );
    $('#RecordedScores').DataTable( {
            pageLength:50,
            dom: "Bfrtip",
            ajax: all_scores_api,
            columns: [
                        { data: "match_name" },
                        { data: "team_number" },
                        
            ],
            select: true,
            buttons: [
                        { extend: "remove", editor: editor }
            ]
    } );
} );