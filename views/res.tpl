<p>Search for "{{query}}"</p>

% if len(rslt_lst) >= 1:
<table id="results">
	<h3>Results</h3>
	% if rslt_lst:
	% 	for url in rslt_lst:
	<ul>
		<li><a href="{{url[1]}}" target="_blank">{{url[2]}}</a>
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
	<p><h2>No results for {{words[0][0]}} found</h2></p>
% end
% if num_words > 1:
<div class="row">
<table id="words" class="u-full-width">
	<tr>
	 	<th>Word</th>
		<th>Count</th>
	</tr>
	% if words:
	% 	for word, count in words:
	<tr>
	 	<td>{{word}}</td>
		<td>{{count}}</td>
	</tr>
	% 	end
	% end

</table>
</div>
% end
