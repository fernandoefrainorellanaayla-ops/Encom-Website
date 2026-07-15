<?php
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    
    $nombre = htmlspecialchars(trim($_POST['nombre']));
    $correo = filter_var(trim($_POST['correo']), FILTER_SANITIZE_EMAIL);
    $mensaje = htmlspecialchars(trim($_POST['mensaje']));

    if (empty($nombre) || empty($correo) || empty($mensaje)) {
        die("Error: Se detectó una anomalía en la transmisión. Faltan datos.");
    }

    $destinatario = "fernandoefrainorellanaayla@gmail.com"; 
    $asunto = "Nueva transmisión de red (Contacto ENCOM): " . $nombre;

    $cuerpo = "Se ha recibido una nueva transmisión en el servidor de ENCOM:\n\n";
    $cuerpo .= "========================================\n";
    $cuerpo .= "PROGRAMA / USUARIO: " . $nombre . "\n";
    $cuerpo .= "ENLACE DE RETORNO (CORREO): " . $correo . "\n";
    $cuerpo .= "========================================\n\n";
    $cuerpo .= "CONTENIDO DEL MENSAJE:\n";
    $cuerpo .= $mensaje . "\n\n";
    $cuerpo .= "========================================\n";
    $cuerpo .= "Fin de la transmisión.";

    $headers = "From: terminal@encom.com" . "\r\n";
    $headers .= "Reply-To: " . $correo . "\r\n";
    $headers .= "X-Mailer: PHP/" . phpversion();

    $envio_exitoso = @mail($destinatario, $asunto, $cuerpo, $headers);

    if ($envio_exitoso) {
        echo "<script>
                alert('¡Transmisión exitosa! Su mensaje ha sido enviado a las oficinas centrales de ENCOM.');
                window.location.href = 'contacto.html';
              </script>";
    } else {
        echo "<script>
                alert('Error de red: No se pudo enlazar con el servidor de correo. Por favor, intente más tarde.');
                window.location.href = 'contacto.html';
              </script>";
    }

} else {
    header("Location: contacto.html");
    exit();
}
?>