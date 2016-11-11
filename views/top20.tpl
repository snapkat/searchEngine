% if user:
<div>
<table id="results">
<h2>Top 20 Words</h2>
% 	for word, occurences in top_words:
<tr>
 	<td>{{word}}</td>
	<td>{{occurences}}</td>
</tr>
% 	end
</table>
</div>
% end