var all_teams_api = `/${user_site_key}/api/team/allteams`
var add_team_api = `/${admin_site_key}/api/team/addteam`
var modify_team_api = `/${admin_site_key}/api/team/modify`

var editor; // use a global for the submit and return data rendering in the examples
 
$(document).ready(function() {
    
    editor = new $.fn.dataTable.Editor( {
        ajax: {
            edit: {
                contentType: 'application/json',
                processData: false,
                data: function ( d ) {
                    // I have to modify the data object delivered by datatables.
                        data_obj = d["data"];
                        var tosend
                        for (const [key, value] of Object.entries(data_obj)) {
                            tosend = value;
                            tosend["team_number"] = key;
                        }
                        final =  JSON.stringify( tosend );
                        return final
                    },
                url: modify_team_api,
            },
            create: {
                contentType: 'application/json',
                processData: false,
                data: function ( d ) {
                        data_obj = d["data"];
                        var tosend
                        for (const [key, value] of Object.entries(data_obj)) {
                            tosend = value;
                            tosend["team_number"] = key;
                        }
                        final =  JSON.stringify( tosend );
                        return final
                    },
                url: add_team_api,
            }, 
        },
        idSrc: "team_number",
        table: "#Teams",
        fields: [ {
                            label: "Team Number:",
                            name: "team_number"
                    }, {
                            label: "Team Name:",
                            name: "team_name"
                    }
        ]
    } );
    $('#Teams').DataTable( {
            pageLength:50,
            dom: "Bfrtip",
            ajax: {
                contentType: 'application/json',
                processData: false,
                data: function ( d ) {
                            change =  JSON.stringify( d );
                            return change
                        },
                    url: all_teams_api,
                },
            columns: [
                        { data: "team_number" },
                        { data: "team_name" },
                        
            ],
            select: true,
            buttons: [
                        { extend: "create", editor: editor },
                        { extend: "edit",   editor: editor },
                        //{ extend: "remove", editor: editor }
            ]
    } );
} );