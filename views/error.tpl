<!DOCTYPE html>
<html>
<head>
	<title>Moogle</title>
	<link rel="stylesheet" type="text/css" href="style.css">
</head>
<body>
	<img src="cow2.jpeg"><br>
	<div id="oauth">
	% if user:
		<h3>Signed in as: {{user}}</h3>
		<form method="get" action="/signout">
		<button type="submit"> Sign-out</button>
		</form>	
	% else:
		<form method="get" action="/signin">
		<button id="sign-in" type="submit"> Sign-in with Google</button>
		</form>	
	% end
	</div>

	<h2><span class="white">Moo</span>gle</h2>
	<h2>Either there's been a horrible Mooosteak or the page you've requested was not found</h2>
	<form method="get" action="/">
	<button id="button_button" type="submit"> Return to Search</button></form>
</body>
</html>
