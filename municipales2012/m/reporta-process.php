<?php
  $name = $_POST['name'];
  $email = $_POST['email'];
  $message = $_POST['message'];
  $address = $_POST['address'];
  $from = 'From: municipales2012@votainteligente.cl';
  $to = 'jpperez@ciudadanointeligente.org';
  $subject = '[Mapa Denuncia] Desde teléfono móvil '.date('Y-m-d');
#  $human = $_POST['human'];
  $human = '4';
  $target_path = 'uploads/';
  $target_path = $target_path.basename( $_FILES['att']['name']);
  $att_path = 'http://'.$_SERVER['HTTP_HOST'].'/uploads/'.basename( $_FILES['att']['name']);

  $body = "De: $name\nE-Mail: $email\nDirección: $address\nAdjunto: $att_path\nDenuncia:\n $message";

  if ($_POST['submit']) {
    if ($name != '' && $email != '') {
      if ($human == '4') {
        if (mail ($to, $subject, $body, $from)) {
	  echo '<p>¡Tu denuncia a sido procesada!</p>';

	  if(move_uploaded_file($_FILES['att']['tmp_name'], $target_path)) {
	    echo '<p>El archivo '.basename( $_FILES['att']['name']).' ha subido exitosamente</p>';
	  } else{
	    echo '<p>Se ha producido un error al subir el archivo, ¡por favor inténtelo nuevamente!</p>';
	  }

        } else {
          echo '<p>A ocurrido un error, por favor inténtalo nuevamente</p>'; 
        }
      } else if ($_POST['submit'] && $human != '4') {
        echo '<p>Haz respondido incorrectamente la pregunta anti-spam... ¿o eres un robot?</p>';
      }
    } else {
      echo '<p>¡¡Necesitas llenar todos los campos requeridos!!</p>';
    }
  }
?>
