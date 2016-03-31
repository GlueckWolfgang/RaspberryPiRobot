// TABS
// Version: 2016_03_31
$(document).ready(function(){
    console.log("function tabs called");
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
                     
    $(document).on("click", '#S_19_Ec', (function(event) {
                          console.log("manual click.");
                          Send('Panel/S_19_Ec');
                     }));
                          
    $(document).on("click", '#S_3_Ec', (function(event) {
                          console.log("stop click.");
                          Send('Panel/S_3_Ec');
                     }));
    $(document).on("click", '#S_5_Ec', (function(event) {
                          console.log("slow click.");
                          Send('Panel/S_5_Ec');
                     }));
                     
    $(document).on("click", '#S_22_Ec', (function(event) {
                          console.log("align click.");
                          Send('Panel/S_22_Ec');
                     }));
    $(document).on("click", '#S_6_Ec', (function(event) {
                          console.log("half click.");
                          Send('Panel/S_6_Ec');
                     }));
                     
    $(document).on("click", '#S_7_Ec', (function(event) {
                          console.log("full click.");
                          Send('Panel/S_7_Ec');
                     }));
                     
    $(document).on("click", '#S_8_Ec', (function(event) {
                          console.log("St left click.");
                          Send('Panel/S_8_Ec');
                     }));
                     
    $(document).on("click", '#S_23_Ec', (function(event) {
                          console.log("St ahead click.");
                          Send('Panel/S_23_Ec');
                     }));
                     
    $(document).on("click", '#S_9_Ec', (function(event) {
                          console.log("St right click.");
                          Send('Panel/S_9_Ec');
                     }));

    $(document).on("click", '#S_10_Ec', (function(event) {
                          console.log("Turn 45 left click.");
                          Send('Panel/S_10_Ec');
                     }));
                     
    $(document).on("click", '#S_11_Ec', (function(event) {
                          console.log("Turn 45 right click.");
                          Send('Panel/S_11_Ec');
                     }));
                     
    $(document).on("click", '#S_12_Ec', (function(event) {
                          console.log("Turn 90 left click.");
                          Send('Panel/S_12_Ec');
                     }));
                     
    $(document).on("click", '#S_13_Ec', (function(event) {
                          console.log("Turn 90 right click.");
                          Send('Panel/S_13_Ec');
                     }));
                     
    $(document).on("click", '#S_21_Ec', (function(event) {
                          console.log("Target move click.");
                          Send('Map/S_21_Ec');
                     }));
                     
    $(document).on("click", '#S_24_Ec', (function(event) {
                          console.log("Start end position click.");
                          Send('Map/S_24_Ec');
                     }));
                     
    $(document).on("click", '#S_25_Ec', (function(event) {
                          console.log("Tag click.");
                          Send('Map/S_25_Ec');
                     }));
                     
    $("#tabs").on("tabsload", (function(event,ui) {
        if (ui.panel.attr("id")==='ui-id-3') {
            window.setTimeout( MapCanvasRectData(), 20 );
            window.setTimeout( MapCanvasCircleData(), 20 );
            window.setTimeout( MapCanvasLineData(), 50 );
            
            // On mouse move over canvas show mouse position in real coordinates
            var canvas = document.getElementById('MousePosition');
            var context = canvas.getContext('2d');
            
            // disable context menu
            $('body').on('contextmenu', 'canvas', function(e){ return false; });
            
            canvas.addEventListener('mousemove', function(evt) {
            var mousePos = getMousePos(canvas, evt);
            var message = 'Mouse position in real coordinates (cm)   x: ' + Math.round(mousePos.x * 2.5) + ',  y: ' + Math.round(mousePos.y * 2.5);
            writeMessage(canvas, message);
            }, false);
            
            // On mouse click in canvas send mouse position and key left/right to webserver
            canvas.addEventListener('mousedown', function (e){
            var key = "left";
            
            if(e.button < 2) var key = "left";
            else if(e.button === 2) var key = "right";       
            var mousePos = getMousePos(canvas, e);
            Send("Map/" + "mouse_" + key + "_" + String(Math.round(mousePos.x)) + "_" + String(Math.round(mousePos.y)));
            
            
            // Actualize track
            // to be done
            
                  
            }, false);
        }
    }));
            
});




// 1s cycle
setInterval(function() {
    PanelData();
    window.setTimeout(MapData(), 2);
    setTimeout(MapCanvasCircleData(), 0);
    console.log("1s cycle has been started");
}, 1000);

// 2s cycle
setInterval(function() {
    AlarmlistData();
    console.log("2s cycle has been started");
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
                    if (document.getElementById(id)!== null) {
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
                        ( /(?:^|\s)black(?!\S)/g , " x" )

                        document.getElementById(id).className =
                        document.getElementById(id).className.replace
                        ( /(?:^|\s)red(?!\S)/g , " x" )

                        document.getElementById(id).className =
                        document.getElementById(id).className.replace
                        ( /(?:^|\s)yellow(?!\S)/g , " x" )

                        document.getElementById(id).className =
                        document.getElementById(id).className.replace
                        ( /(?:^|\s)green(?!\S)/g , " x" )
                        
                        document.getElementById(id).className =
                        document.getElementById(id).className.replace
                        ( /(?:^|\s)bggreen(?!\S)/g , " x" )
                        
                        document.getElementById(id).className =
                        document.getElementById(id).className.replace
                        ( /(?:^|\s)bggray(?!\S)/g , " x" )
                        
                        document.getElementById(id).className =
                        document.getElementById(id).className.replace
                        ( /(?:^|\s)bgred(?!\S)/g , " x" )

                        document.getElementById(id).className =
                        document.getElementById(id).className.replace
                        ( /(?:^|\s)white(?!\S)/g , " x" )
                        
                        document.getElementById(id).className =
                        document.getElementById(id).className.replace
                        ( /(?:^|\s)bgwhite(?!\S)/g , " x" )

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

// Map static data
function MapCanvasRectData(){
    var active = $('#tabs').tabs( "option", "active" );
    if  (active == 2) {  
        $.ajax({
            type: 'GET',
            url: '/ajax/Map/canvasRectData',
            async: true,
            dataType: "JSON",
            success: function(obj, textstatus, jqXhr) {
                table = eval("(" + jqXhr.responseText + ")");
                var c = document.getElementById("Map");
                var ctx = c.getContext("2d");
                $.each(table, function(i,parameterList) {
                    ctx.fillStyle = parameterList[0];
                    ctx.fillRect(parameterList[1][0],
                                 parameterList[1][1],
                                 parameterList[1][2],
                                 parameterList[1][3]);
                });
            },
            error: function (jqXhr, textStatus, errorThrown) {
                console.log("function Map called with error")
            }
        });
    }
}

function MapCanvasCircleData(){
    var active = $('#tabs').tabs( "option", "active" );
    if  (active == 2) {
        $.ajax({
            type: 'GET',
            url: '/ajax/Map/canvasCircleData',
            async: true,
            dataType: "JSON",
            success: function(obj, textstatus, jqXhr) {
                table = eval("(" + jqXhr.responseText + ")");
                var c = document.getElementById("Positions");
                var ctx = c.getContext("2d");
                ctx.clearRect(0, 0, c.width, c.height);
                $.each(table, function(i,parameterList) { 
                    ctx.fillStyle = parameterList[0]; 
                    ctx.strokeStyle = parameterList[0];
                    ctx.lineWidth= 1;           
                    ctx.beginPath();
                    ctx.arc(parameterList[1],
                    parameterList[2],
                    parameterList[3],
                    parameterList[4],
                    parameterList[5]);
                    ctx.stroke();                    
                });
            },
            error: function (jqXhr, textStatus, errorThrown) {
                console.log("function Map called with error")
            }
        });
    }
}

function MapCanvasLineData(){
    var active = $('#tabs').tabs( "option", "active" );
    if  (active == 2) {
        $.ajax({
            type: 'GET',
            url: '/ajax/Map/canvasLineData',
            async: true,
            dataType: "JSON",
            success: function(obj, textstatus, jqXhr) {
                table = eval("(" + jqXhr.responseText + ")");
                var c = document.getElementById("Map");
                var ctx = c.getContext("2d");
                $.each(table, function(i,parameterList) {
                    ctx.fillStyle = parameterList[0];
                    ctx.strokeStyle = parameterList[0];
                    ctx.lineWidth= 1;
                    ctx.beginPath();
                    ctx.moveTo(parameterList[1], parameterList[2])
                    ctx.lineTo(parameterList[3], parameterList[4])
                    ctx.stroke();
                });
            },
            error: function (jqXhr, textStatus, errorThrown) {
                console.log("function Map called with error")
            }
        });
    }
}

// Map dynamic data
function MapData(){
    var active = $('#tabs').tabs( "option", "active" );
    if  (active == 2) {
        $.ajax({
            type: 'GET',
            url: '/ajax/Map/data',
            async: true,
            dataType: "JSON",
            success: function(obj, textstatus, jqXhr) {
                dictionary = eval("(" + jqXhr.responseText + ")");
                $.each(dictionary, function(id,val) {
                    idc = null
                    if (document.getElementById(id)!== null) {
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
                        ( /(?:^|\s)black(?!\S)/g , " x" )

                        document.getElementById(id).className =
                        document.getElementById(id).className.replace
                        ( /(?:^|\s)red(?!\S)/g , " x" )

                        document.getElementById(id).className =
                        document.getElementById(id).className.replace
                        ( /(?:^|\s)yellow(?!\S)/g , " x" )

                        document.getElementById(id).className =
                        document.getElementById(id).className.replace
                        ( /(?:^|\s)green(?!\S)/g , " x" )

                        document.getElementById(id).className =
                        document.getElementById(id).className.replace
                        ( /(?:^|\s)bggreen(?!\S)/g , " x" )

                        document.getElementById(id).className =
                        document.getElementById(id).className.replace
                        ( /(?:^|\s)bggray(?!\S)/g , " x" )

                        document.getElementById(id).className =
                        document.getElementById(id).className.replace
                        ( /(?:^|\s)bgred(?!\S)/g , " x" )

                        document.getElementById(id).className =
                        document.getElementById(id).className.replace
                        ( /(?:^|\s)white(?!\S)/g , " x" )

                        document.getElementById(id).className =
                        document.getElementById(id).className.replace
                        ( /(?:^|\s)bgwhite(?!\S)/g , " x" )

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

function getMousePos(canvas, evt) {
var rect = canvas.getBoundingClientRect();
return {
  x: Math.round(evt.clientX - rect.left),
  y: Math.round(evt.clientY - rect.top)
};
}

function writeMessage(canvas, message) {
        var context = canvas.getContext('2d');
        context.clearRect(0, 0, canvas.width, canvas.height);
        context.font = '14pt Calibri';
        context.fillStyle = 'black';
        context.fillText(message, 5, 440);
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