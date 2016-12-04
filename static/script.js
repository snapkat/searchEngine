"use strict";

var q_box = $("#q");
var page = 1;

function show_query_results(resp){
	$("#res").html(resp);
}

function prev_page(){
	if (page>1){
		page = page-1;
		ajax_query();
	}
}

function next_page(){
	page=page+1;
	ajax_query();
}

function ajax_query(){
	var q = q_box.val();
	$.ajax({
		url:"/results?q=" + q +"&page="+page.toString(),
		success: show_query_results
	});
}

function search(){
	page = 1;
	ajax_query();
}

q_box.keyup($.debounce(120, search));

$("#clear").click(function(){
	q_box.val("");
	ajax_query();
});

/** Top 20 **/
function show_top20_results(resp){
	$("#top20").html(resp);
}

function ajax_top20(){
	var q = q_box.val();
	$.ajax({
		url:"/top20?q=" + q,
		success: show_top20_results
	});
}

$("#search_button").click(ajax_top20);

$(document).keypress(function (e) {
 var key = e.which;
 if(key == 13)  // the enter key code
  {
    $("#search_button").click();
    return false;  
  }
});