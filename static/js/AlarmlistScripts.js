// Alarmlist
$(document).ready(function(){
       $('#Backnowledge').click(function(event) {
                              console.log("acknowledge click.");
                              Send('Alarmlist/acknowledge');
                         });
});

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