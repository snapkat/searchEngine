<!DOCTYPE html>
<html>
<head>
	<title>Moogle</title>
	<link rel="stylesheet" type="text/css" href="style.css">
</head>
<body>
	<img class="logo" src="cow.jpeg" height="120" ><br>
	<h3>Signed in as: {{user}}</h3>
	<form method="get" action="/signout">
	<button type="submit"> Sign-out</button>
	</form>	
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
