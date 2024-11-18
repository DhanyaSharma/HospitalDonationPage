<?php
$serverName = "localhost";
$UserName = "root";
$Password = '';
$dbname = "organpage";

$conn = mysqli_connect($serverName, $UserName, $Password, $dbname);
if ($conn) {
    echo "ok";
}
$Name = $_POST['NAME'];
$Aadhar_No = $_POST['Aadhar_No'];
$Date_of_Birth = $_POST['Date_of_Birth'];
$Email = $_POST['Email'];
$Password = $_POST['Password'];
$Phone_Number = $_POST['Phone_Number'];

?>
