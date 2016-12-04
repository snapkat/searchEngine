<!DOCTYPE html>
<html>
<head>
	<title>Moogle</title>
	
    <link href="//fonts.googleapis.com/css?family=Raleway:400,300,600" rel="stylesheet" type="text/css">
    <link rel="stylesheet" href="normalize.css">
  	<link rel="stylesheet" href="skeleton.css">
  	<link rel="stylesheet" type="text/css" href="style.css">
  	<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.1.0/jquery.min.js"></script>
  	<script src="debounce.js"></script>
</head>
<body>
	<div id="oauth" class="row">
	% if user:
		<form method="get" action="/signout" class="twelve columns">
		<span>Hi <img src="{{pic}}"><strong>{{user}}</strong>!</span><button type="submit" class="right"> Sign-out</button>
		</form>	
	% else:
		<form method="get" action="/signin" class="two columns right">
		<button id="sign-in" type="submit"> Sign-in with Google</button>
		</form>	
	% end
	</div><br>
	<div class="search_box">
	<div class="row">
		<h1 class="twelve columns logo"><span class="white">Moo</span>gle</h1>
	</div>
	<div class="row">
		<input id="q" class="eight columns offset-by-two" type="text" name="q" autocomplete="off" placeholder="Search">
	</div>
	<div class="row">
		<button id="clear" class="button two columns offset-by-three">Clear</button>
		<button id="search_button" class="button button-primary four columns" type="submit"> Moo!</button>
	</div>
	</div>
	<br>
	<div id="res">
	</div>
	<div id="top20">
	</div>
	<script type="text/javascript" src="script.js"></script>
</body>
</html>
