<p>Search for "{{query}}"</p>
<p>Number of Query Words: {{num_words}}</p>

<table>
% if len(rslt_lst) >= 1:
<table id="results">
	<tr>
	 	<th>PageRank</th>
		<th>URL</th>
		</tr>
	% if rslt_lst:
	% 	for url in rslt_lst:
	<tr>
	 	<td>{{url[0]}}</td>
		<td><a href="{{url[1]}}" target="_blank">{{url[1]}}</a></td>
	</tr>
	% 	end
	% end
</table>
<div id="page_buttons">
	% if page > 1:
	<button id="prev" onclick="prev_page()">Prev Page</button>
	% end
	<span>Page {{page}} of {{max_page}}</span>
	% if  page < max_page:
	<button id="next" onclick="next_page()">Next Page</button>
	% end
</div>

% else:
	<p><h2>No results for {{words[0][0]}} found</h2></p>
% end
% if num_words > 1:
<table id="words">
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
% end
