<?php

if( isset( $_GET['Login'] ) ) {

	$user = $_GET['username'];
	
	$pass = $_GET['password'];
	$pass = md5($pass);

	$qry = "SELECT * FROM `users` WHERE user='$user' AND password='$pass';";
	$result = mysql_query( $qry ) or die( '<pre>' . mysql_error() . '</pre>' );

	if( $result && mysql_num_rows( $result ) == 1 ) {
		// Get users details
		$i=0; // Bug fix.
		$avatar = mysql_result( $result, $i, "avatar" );

		// Login Successful
		$html .= "<p>Welcome to the password protected area " . $user . "</p>";
		$html .= '<img src="' . $avatar . '" />';
	} else {
		//Login failed
		$html .= "<pre><br>Username and/or password incorrect.</pre>";
	}

	mysql_close();
}

?>