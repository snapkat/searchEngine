<p>Search for "{{query}}"</p>

% if len(rslt_lst) >= 1:
<table id="results">
	<h4>Results</h4>
	% if rslt_lst:
	% 	for url in rslt_lst:
	<ul>
		<li class="result_box"><a href="{{url[1]}}" target="_blank">{{url[2]}}</a>
			<p class="small">{{url[1]}}</p>
		</li>
	</ul>
	% 	end
	% end
</table>
<div  >
	<div class="row">
	% if page > 1:
	<button id="prev" class="two columns small_button offset-by-three" onclick="prev_page()">Prev Page</button>
	% else:
	<div class="two columns small_button offset-by-three">&nbsp</div>
	% end
	<span class="two columns text_center">Page {{page}} of {{max_page}}</span>
	% if  page < max_page:
	<button id="next" class="two columns small_button" onclick="next_page()">Next Page</button>
	% end
	</div>
</div>

% else:
	<p><h4>No results for {{words[0][0]}} found</h4></p>
% end
