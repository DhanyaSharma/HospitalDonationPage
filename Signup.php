<?php
// Include the file containing database connection details
include "connect.php";

// Check if the form is submitted
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    // Extract form data and sanitize inputs
    $Name = mysqli_real_escape_string($conn, $_POST['NAME']);
    $Aadhar_No = mysqli_real_escape_string($conn, $_POST['Aadhar_No']);
    $Date_of_Birth = mysqli_real_escape_string($conn, $_POST['Date_of_Birth']);
    $Email = mysqli_real_escape_string($conn, $_POST['EmailL']); 
    $Password = mysqli_real_escape_string($conn, $_POST['Password']);
    $Phone_Number = mysqli_real_escape_string($conn, $_POST['Phone_Number']);

    // Prepare and execute SQL statement to insert data into the database
    $sql = "INSERT INTO registration (Name, Aadhar_No, Date_of_Birth, Email, Password, Phone_Number) 
            VALUES ('$Name', '$Aadhar_No', '$Date_of_Birth', '$Email', '$Password', '$Phone_Number')";
    
    if (mysqli_query($conn, $sql)) {
        // If data insertion is successful, redirect the user or display a success message
        echo "Data inserted successfully!";
    } else {
        // If an error occurs during data insertion, display an error message
        echo "Error: " . $sql . "<br>" . mysqli_error($conn);
    }
}

// Close the database connection
?>
