<!DOCTYPE html>
<html>
<head>
	<title>Moogle</title>
	<link rel="stylesheet" type="text/css" href="static/style.css">
</head>
<body>
	<img class="logo" src="static/cow.jpeg" height="120" >
	<h1><span class="white">Moo</span>gle</h1>

	<form method="get" action="results">
		<input type="text" name="q" autocomplete="off" placeholder="Search">
		<button type="submit"> Moo!</button>
	</form>
	<br>
	<br>
	<table id="results">
		<h2>Top 20 Words</h2>
		% for word, occurences in top_words:
		<tr>
		 	<td>{{word}}</td>
			<td>{{occurences}}</td>
		</tr>
		% end
	</table>
</body>
</html>