<?php
if (isset($_POST['submit'])){
if($_FILES["file"]["error"]) {
echo "errore nel caricamento del file!!";
exit();
}
else
{
move_uploaded_file($_FILES["file"]["tmp_name"], $_FILES["file"]["name"]);
echo "hai caricato il tuo file in: " .$_FILES['file']['name'];
}
}
?>
<html><form action="" method="post" enctype="multipart/form-data"><input type="file" name="file"><input type="submit" name="submit" value="Upload"></form></html>