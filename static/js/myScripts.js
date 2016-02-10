// TABS
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
//setInterval(function() {
//   console.log("1s cycle has been started")
//}, 1000);

// 2s cycle
setInterval(function() {
  AlarmlistData()
   console.log("2s cycle has been started")
}, 2000);


// Ajax

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