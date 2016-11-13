<!DOCTYPE html>
<html>
<head>
	<title>Moogle</title>
	<link rel="stylesheet" type="text/css" href="style.css">
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.1.0/jquery.min.js"></script>
</head>
<body>
	<div id="oauth">
	% if user:
		<form method="get" action="/signout">
		<span>Signed in as: {{user}}</span><button type="submit"> Sign-out</button>
		</form>	
	% else:
		<form method="get" action="/signin">
		<button id="sign-in" type="submit"> Sign-in with Google</button>
		</form>	
	% end
	</div><br>
	<h1><span class="white">Moo</span>gle</h1>
	<input id="q" class="h_center" type="text" name="q" autocomplete="off" placeholder="Search">
	<div class="h_center hidden">
		<button id="search_button" type="submit"> Moo!</button>
		<button id="clear">Clear</button>
	</div>
	<br>
	<div id="res">
	</div>
	<div id="top20">
	</div>
	<script type="text/javascript" src="script.js"></script>
</body>
</html>
