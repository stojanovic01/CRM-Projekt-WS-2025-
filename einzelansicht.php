<?php
$servername = "localhost";
$username = "u243204db1";
$password = "01122024spSP.";
$dbname = "u243204db1";

// Verbindung herstellen
$conn = new mysqli($servername, $username, $password, $dbname);

// Verbindung prüfen
if ($conn->connect_error) {
    die("Verbindung fehlgeschlagen: " . $conn->connect_error);
}

if (isset($_GET["id"])) {
    $id = intval($_GET["id"]);
    $sql = "SELECT * FROM kunden WHERE id = $id";
    $result = $conn->query($sql);

    if ($result->num_rows == 1) {
        $row = $result->fetch_assoc();
        echo "<h1>Kundendetails</h1>";
        echo "<p><strong>Name:</strong> " . htmlspecialchars($row["name"]) . "</p>";
        echo "<p><strong>Email:</strong> " . htmlspecialchars($row["email"]) . "</p>";
        echo "<p><strong>Adresse:</strong> " . htmlspecialchars($row["adresse"]) . "</p>";
        // Hier kannst du weitere Felder hinzufügen
    } else {
        echo "Kunde nicht gefunden.";
    }
} else {
    echo "Keine Kunden-ID angegeben.";
}
$conn->close();
?>
