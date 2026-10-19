/* Auxiliar SOLO para pruebas: mide que tan lleno queda el alto de la
   pantalla. Se borra al terminar. */
(function () {
  var doc = document, w = doc.defaultView;
  var vw = doc.documentElement.clientWidth;
  var vh = doc.documentElement.clientHeight;

  function cs(el) { return w.getComputedStyle(el); }

  /* Para cada contenedor clave: ancho x alto y que porcentaje del alto de
     la pantalla ocupa. Si el porcentaje es bajo, el contenedor se ve corto
     en un telefono alto. */
  var nombres = ['.navbar', '.login', '.register', '.container-2', '.img-show img',
                 '.imagen-selecter', '.main-background', '.mainmain', '.footer',
                 '.bigflex', '.shortflex', '.posts-container', '.post',
                 '.form-input-container-1 textarea', '.flex-grid'];

  var filas = [];
  for (var i = 0; i < nombres.length; i++) {
    var e = doc.querySelector(nombres[i]);
    if (!e) continue;
    var s = cs(e);
    if (s.display === 'none') continue;
    var r = e.getBoundingClientRect();
    if (r.width === 0 && r.height === 0) continue;
    filas.push(nombres[i] + ' = ' + Math.round(r.width) + 'x' + Math.round(r.height) +
               ' (' + Math.round(r.height / vh * 100) + '% del alto)');
  }

  /* Cuanto queda de pantalla vacia debajo del ultimo elemento con alto. */
  var ultimo = 0;
  var todos = doc.querySelectorAll('body *');
  for (var j = 0; j < todos.length; j++) {
    var r2 = todos[j].getBoundingClientRect();
    if (r2.height > 4 && r2.width > 4) {
      var fondo = cs(todos[j]).backgroundColor;
      if (fondo && fondo !== 'rgba(0, 0, 0, 0)' && fondo !== 'transparent') {
        if (r2.bottom > ultimo) ultimo = r2.bottom;
      }
    }
  }

  w.__auditoria = {
    vw: vw, vh: vh,
    scroll: doc.documentElement.scrollHeight,
    orientacion: vh >= vw ? 'vertical' : 'horizontal',
    filas: filas,
    ultimoFondo: Math.round(ultimo),
    huecosAbajo: Math.round(ultimo - vh)
  };
})();