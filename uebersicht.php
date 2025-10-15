<?php
$servername = "localhost"; // oder dein Servername
$username = "u243204db1";
$password = "01122024spSP.";
$dbname = "u243204db1";

// Verbindung herstellen
$conn = new mysqli($servername, $username, $password, $dbname);

// Verbindung prüfen
if ($conn->connect_error) {
    die("Verbindung fehlgeschlagen: " . $conn->connect_error);
}

// SQL-Abfrage
// $sql = "SELECT id, name, email FROM kunden";
// $result = $conn->query($sql);

// echo "<h1>Kundenübersicht</h1>";
// if ($result->num_rows > 0) {
//     echo "<table border='1'>";
//     echo "<tr><th>Name</th><th>Email</th></tr>";
//     // Ausgabe der Daten jeder Zeile
//     while($row = $result->fetch_assoc()) {
//         echo "<tr>";
//         echo "<td><a href='einzelansicht.php?id=" . $row["id"] . "'>" . htmlspecialchars($row["name"]) . "</a></td>";
//         echo "<td>" . htmlspecialchars($row["email"]) . "</td>";
//         echo "</tr>";
//     }
//     echo "</table>";
// } else {
//     echo "Keine Kunden gefunden.";
// }
// $conn->close();
// 
?>
