// TABS
$(document).ready(function(){
       console.log("function tabs called")
       $('#tabs').tabs({active: 1});

       $('#Backnowledge').click(function(event) {
                              console.log("acknowledge click.");
                              Send('Alarmlist/acknowledge');
                         });
});

// 1s cycle
//setInterval(function() {
//   console.log("1s cycle has been started")
//}, 1000);

// 2s cycle
//setInterval(function() {
//  AlarmlistData()
//   console.log("2s cycle has been started")
//}, 2000);


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