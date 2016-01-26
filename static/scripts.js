$(document).ready(function(){
         $('#button1').click(function() { window.location.href = "/Robbi/1"; });
         $('#button2').click(function() { window.location.href = "/Robbi/2"; });
         $('#button3').click(function() { window.location.href = "/Robbi/3"; });
         $('#button4').click(function() { window.location.href = "/Robbi/4"; });
         $('#button5').click(function() { window.location.href = "/Robbi/5"; });
});

function tab(tab) {
   document.getElementById('tab1').style.display = 'none';
   document.getElementById('tab2').style.display = 'none';
   document.getElementById('tab3').style.display = 'none';
   document.getElementById('li_tab1').setAttribute("class", "");
   document.getElementById('li_tab2').setAttribute("class", "");
   document.getElementById(tab).style.display = 'block';
   document.getElementById('li_tab3').setAttribute("class", "");
   document.getElementById(tab).style.display = 'block';
   document.getElementById('li_'+tab).setAttribute("class", "active");
}