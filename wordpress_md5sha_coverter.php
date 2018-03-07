<?php
//usage: cat rockyou.txt | php thiscript.php > rockyou_sha_md5.txt

while($f = fgets(STDIN){
	$passwenc = md5(sha1(rtrim($f)));
	echo "$passwenc : $f";
}

?>