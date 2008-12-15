<?php
$plone_forward = 'http://plone.bungenisrv.local';
$username = $_POST['username'];
$password = $_POST['password'];
setcookie('guserpass', $username.":".$password ,time()+60*60*24*30, '/', '.bungenisrv.local');
header('Location:'+$plone_forward);
?>
