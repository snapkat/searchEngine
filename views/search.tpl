<!DOCTYPE html>
<html>
<head>
	<title>Moogle</title>
<<<<<<< HEAD
	<link rel="stylesheet" type="text/css" href="style.css">
</head>
<body>
	<img src="cow.jpeg"><br>
	<form method="get" action="/signin">
	<button type="submit"> Sign-in with Google</button>
	</form>	
=======
	<link rel="stylesheet" type="text/css" href="static/style.css">
</head>
<body>
	<img class="logo" src="static/cow.jpeg" height="120" >
>>>>>>> b10358f9db45cd995a31581e1c528172cc37dcb7
	<h1><span class="white">Moo</span>gle</h1>

	<form method="get" action="results">
		<input type="text" name="q" autocomplete="off" placeholder="Search">
		<button type="submit"> Moo!</button>
	</form>
	<br>
	<br>
<<<<<<< HEAD

</body>
</html>
=======
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
>>>>>>> b10358f9db45cd995a31581e1c528172cc37dcb7
