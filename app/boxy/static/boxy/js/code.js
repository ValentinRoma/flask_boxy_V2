function enviarAccion(accion) {
      fetch('/api/accion', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ accion: accion })
      })
      .then(res => res.json())
      .then(data => {
        document.getElementById("respuesta").textContent = data.mensaje;
      })
      .catch(err => console.error(err));
    }


  function actualizarAmbiente() {
    fetch('/api/ambiente')
      .then(res => res.json())
      .then(data => {
        document.getElementById('temp-value').textContent = data.temp + " °C";
        document.getElementById('hum-value').textContent = data.hum + " %";
      })
      .catch(err => console.error(err));
  }

  setInterval(actualizarAmbiente, 2000);
  actualizarAmbiente();

  const button = document.querySelector('.boton');

//   function saludo(){
//     console.log(e.target)
//   }

  button.addEventListener('click', (e)=>{
    console.log(e.target)
  })