<!DOCTYPE HTML>
<html>

<head>
  <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
  <title>Mapa Denuncia para móviles</title>
  <link type="text/css" rel="stylesheet" href="style.css">
  <script src="js/script.js"></script>
</head>

<body>
  <header class="body">
<!--    <h1>Mapa Denuncia</h1> -->
    <img src="images/logo-mapadenuncia.png" alt="Mapa Denuncia"/>
  </header>
  <section class="body">
    <form method="post" action="reporta-process.php" enctype='multipart/form-data'>

      <label>*Nombre</label>
      <input name="name" placeholder="Escriba aquí">

      <label>*Email</label>
      <input name="email" type="email" placeholder="Escriba aquí">

      <label>*Dirección</label>
      <input name="address" placeholder="Escriba aquí">

      <label>Adjuntar imagen</label>
      <input name="att" type="file">

      <label>Denuncia</label>
      <textarea name="message" placeholder="Escriba aquí"></textarea>
<!-- NOTE: Disable verify question
      <label>*¿Cuánto es 2+2? (Anti-spam)</label>
      <input name="human" placeholder="Escriba aquí">
-->
      <input id="submit" name="submit" type="submit" value="Submit">
    </form>
  </section>
  <footer class="body">
    <br />
    <a href="http://legislativo.votainteligente.cl"><img src="http://ciudadanointeligente.org/assets/images/ic-legislativo.png" alt="Legislativo"></a>
    <a href="http://www.elvaso.cl"><img src="http://ciudadanointeligente.org/assets/images/ic-vaso.png" alt="El Vaso"></a>
    <a href="http://www.candideit.org"><img src="http://ciudadanointeligente.org/assets/images/ic-candideitorg.png" alt="Candideit.org"></a>
    <a href="http://www.votainteligente.cl"><img src="http://ciudadanointeligente.org/assets/images/ic-vota.png" alt="Vota Inteligente"></a>
  </footer>
</body>
</html>
