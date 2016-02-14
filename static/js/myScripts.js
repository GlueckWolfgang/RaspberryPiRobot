// TABS
// Version: 2016_02_14
$(document).ready(function(){
       console.log("function tabs called")
       $('#tabs').tabs({active: 1});

       $(document).on("click", '#Backnowledge', (function(event) {
                              console.log("acknowledge click.");
                              Send('Alarmlist/acknowledge');
                         }));

       $(document).on("click", '#Bft', (function(event) {
                              console.log("first click.");
                              Send('Alarmlist/ft');
                         }));

       $(document).on("click", '#Bbwd', (function(event) {
                              console.log("backward click.");
                              Send('Alarmlist/bwd');
                         }));

       $(document).on("click", '#Bfwd', (function(event) {
                              console.log("foreward click.");
                              Send('Alarmlist/fwd');
                         }));

       $(document).on("click", '#Blt', (function(event) {
                              console.log("last click.");
                              Send('Alarmlist/lt');
                         }));
});

// 1s cycle
setInterval(function() {
   PanelData()
   console.log("1s cycle has been started")
}, 1000);

// 2s cycle
setInterval(function() {
  AlarmlistData()
   console.log("2s cycle has been started")
}, 2000);


// Ajax
// Panel data
function PanelData(){
    var active = $('#tabs').tabs( "option", "active" );
    if  (active == 0) {
        $.ajax({
            type: 'GET',
            url: '/ajax/Panel/data',
            async: true,
            dataType: "JSON",
            success: function(obj, textstatus, jqXhr) {
                dictionary = eval("(" + jqXhr.responseText + ")");
                $.each(dictionary, function(id,val) {
                    idc = null
                    if (document.getElementById(id) !== null) {
                      // id read from dictionary, found in document
                      if (!id.endsWith("_Ec") && (!id.endsWith("El"))) {
                          // change value except empty id types
                          document.getElementById(id).innerHTML = val;
                          if (id.endsWith("_V")) {
                              idc = id.replace("_V","_Cv")
                              // new style for value
                              val = dictionary[idc]
                          }
                      }
                      else if (id.endsWith("_Ec")) {
                              idc = id.replace("_Ec", "_Cc")
                              // new style for button
                              val = dictionary [idc]
                      }
                      else if (id.endsWith("_El")){
                              idc = id.replace("_El", "_Cl")
                              // new style for lamp
                              val = dictionary [idc]
                      }
                    }
                    if (idc) {
                        // remove old and add new style
                        document.getElementById(id).className =
                        document.getElementById(id).className.replace
                        ( /(?:^|\s)black(?!\S)/g , "x" )

                        document.getElementById(id).className =
                        document.getElementById(id).className.replace
                        ( /(?:^|\s)red(?!\S)/g , "x" )

                        document.getElementById(id).className =
                        document.getElementById(id).className.replace
                        ( /(?:^|\s)yellow(?!\S)/g , "x" )

                        document.getElementById(id).className =
                        document.getElementById(id).className.replace
                        ( /(?:^|\s)green(?!\S)/g , "x" )

                        document.getElementById(id).className =
                        document.getElementById(id).className.replace
                        ( /(?:^|\s)white(?!\S)/g , "x" )

                        document.getElementById(id).className =
                        document.getElementById(id).className.replace
                        ( /(?:^|\s)x(?!\S)/g , val )
                    }

                });
            },
            error: function (jqXhr, textStatus, errorThrown) {
            }
        });
    }
}

// Alarmlist data
function AlarmlistData(){
 var active = $('#tabs').tabs( "option", "active" );
 if  (active == 1) {
    $.ajax({
        type: 'GET',
        url: '/ajax/Alarmlist/data',
        async: true,
        dataType: "JSON",
        success: function(obj, textstatus, jqXhr) {
            dictionary = eval("(" + jqXhr.responseText + ")");
            $.each(dictionary, function(id,val) {
                if (document.getElementById(id) !== null) {
                  document.getElementById(id).innerHTML = val;
                }
            });
        },
        error: function (jqXhr, textStatus, errorThrown) {
        }
    });
 }
}

// Commands
function Send(command) {
    $.ajax({
        type: 'GET',
        url: '/ajax/' + command,
        async: true,
        dataType: "JSON",
        success: function(obj, textstatus, jqXhr) {
            dictionary = eval("(" + jqXhr.responseText + ")");
        },
        error: function (jqXhr, textStatus, errorThrown) {
        }
    });
}