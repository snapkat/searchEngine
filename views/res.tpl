<p>Search for "{{query}}"</p>
<p>Number of Query Words: {{num_words}}</p>
<table id="results">
	<ul>
	% if docs:
	% 	for doc in docs:
		<li><a href="{{doc}}">{{doc}}</a></li>
	% 	end
	% end
	</ul>
	
</table>