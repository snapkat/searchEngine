<!DOCTYPE html>
<html>
<head>
	<title>Moogle</title>
	<link rel="stylesheet" type="text/css" href="style.css">
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.1.0/jquery.min.js"></script>
</head>
<body>
	<img src="cow.jpeg"><br>
	% if user:
	<div>
		<h3>Signed in as: {{user}}</h3>
		<form method="get" action="/signout">
		<button type="submit"> Sign-out</button>
		</form>	
	</div>
	% else:
	<div>
		<form method="get" action="/signin">
		<button id="sign-in" type="submit"> Sign-in with Google</button>
		</form>	
	</div>

	% end

	<h1><span class="white">Moo</span>gle</h1>

	<input id="q" type="text" name="q" autocomplete="off" placeholder="Search">
	<button id="search_button" type="submit"> Moo!</button>
	<button id="clear">Clear</button>
	<br>
	<br>
	<div id="res">
	</div>
	<div id="top20">
	</div>
	<script type="text/javascript" src="script.js"></script>
</body>
</html>
