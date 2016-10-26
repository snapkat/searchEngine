<!DOCTYPE html>
<html>
<head>
	<title>Results</title>
<<<<<<< HEAD
	<link rel="stylesheet" type="text/css" href="style.css">
=======
	<link rel="stylesheet" type="text/css" href="static/style.css">
>>>>>>> b10358f9db45cd995a31581e1c528172cc37dcb7
</head>
<body>
	<p>Search for "{{query}}"</p>
	<p>Number of Query Words: {{num_words}}</p>
	% if num_words > 1:
	<table id="results">
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
	<a href="/"><button>Return to Query Page</button></a>
</body>
<<<<<<< HEAD
</html>
=======
</html>
>>>>>>> b10358f9db45cd995a31581e1c528172cc37dcb7
