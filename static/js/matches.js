var all_matches_api = `/${user_site_key}/api/match/all`
var add_match_api = `/${admin_site_key}/api/match/add`
var modify_match_api = `/${admin_site_key}/api/match/modify`
var delete_match_api = `/${admin_site_key}/api/match/delete`

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
                            tosend["matchID"] = key;
                        }
                        final =  JSON.stringify( tosend );
                        return final
                    },
                url: modify_match_api,
            },
            create: {
                contentType: 'application/json',
                processData: false,
                data: function ( d ) {
                        data_obj = d["data"];
                        var tosend
                        for (const [key, value] of Object.entries(data_obj)) {
                            tosend = value;
                            tosend["matchID"] = key;
                        }
                        final =  JSON.stringify( tosend );
                        return final
                    },
                url: add_match_api,
            }, 
            remove: {
                contentType: 'application/json',
                type: "GET",
                data: function ( d ) {
                        data_obj = d["data"];
                        var tosend = {}
                        for (const [key, value] of Object.entries(data_obj)) {
                            console.log(value);
                            tosend["matchID"] = value["matchID"];
                        }
                        return tosend
                    },
                url: delete_match_api,
            }, 
        },
        idSrc: "matchID",
        table: "#Matches",
        fields: [ {
                            label: "Match name:",
                            name: "match_name"
                    }, {
                            label: "Red 1:",
                            name: "red_1"
                    }, {
                            label: "Red 2:",
                            name: "red_2"
                    }, {
                            label: "Red 3:",
                            name: "red_3"
                    }, {
                            label: "Blue 1:",
                            name: "blue_1"
                    }, {
                            label: "Blue 2:",
                            name: "blue_2",
                    }, {
                            label: "Blue 3:",
                            name: "blue_3"
                    }
        ]
    } );
    $('#Matches').DataTable( {
            pageLength:50,
            dom: "Bfrtip",
            ajax: {
                contentType: 'application/json',
                processData: false,
                data: function ( d ) {
                            console.log("datatable")
                            change =  JSON.stringify( d );
                            console.log(change)
                            return change
                        },
                    url: all_matches_api,
                },
            columns: [
                        { data: "match_name" },
                        { data: "red_1" },
                        { data: "red_2" },
                        { data: "red_3" },
                        { data: "blue_1" },
                        { data: "blue_2" },
                        { data: "blue_3" },
            ],
            select: true,
            buttons: [
                        { extend: "create", editor: editor },
                        { extend: "edit",   editor: editor },
                        { extend: "remove", editor: editor }
            ]
    } );
} );