//FUNCIONES

// Funcion solo numeros
function valideNumber(evt) {

  // code is the decimal ASCII representation of the pressed key.
  let code = (evt.which) ? evt.which : evt.keyCode;

  if (code == 8) { // backspace.
    return true;
  }
  else if (code == 13) { // enter
    return true;
  } else if (code >= 48 && code <= 57) { // is a number.
    return true;
  } else { // other keys.
    return false;
  }
}

// Auto focus
function autoFocus() {
  const input = document.querySelector(".autofocus")
  if (input) {
    input.addEventListener("blur", () => {
      setTimeout(() => {
        input.focus();
      }, 0);
    });
  }
}
autoFocus();

// Auto mayus
function Upper(input) {
  input.value = input.value.toUpperCase();
}

//Ir a la pestaña anterior
function goBack() {
  window.history.back();
}

//Alerta usuario
function userAlert() {
  Swal.fire({
    icon: 'success',
    title: '¡Usuario registrado!',
    text: 'El usuario se ha registrado correctamente',
    showConfirmButton: false,
    timer: 2500
  })
};

//Funcion Alerta SweetAlert
function successAlert(title, text, time) {
  Swal.fire({
    icon: 'success',
    title: title,
    text: text,
    showConfirmButton: false,
    timer: time
  })
}

//Alerta 
const registerAlert = document.querySelector('.registerAlert');
if (registerAlert) {
  registerAlert.style.display = 'none';
  let typeAlert = registerAlert.getAttribute('data-status');
  switch (typeAlert) {

    case "success-user":
      successAlert("¡Usuario registrado!", "El usuario se ha registrado correctamente", 2500);
      break;
    case "success-vehicle":
      successAlert("Vehiculo registrado!", "El vehiculo se ha registrado correctamente", 2500);
      break;
    case "success-device":
      successAlert("Dispositivo registrado!", "El dispositivo se ha registrado correctamente", 2500);
      break;
  }
}


//Resolucion del dispositivo
let pageWidth = window.innerWidth;
let pageHeight = window.innerHeight;

//Si se tiene la resolucion del totem
if (pageWidth >= 1080 && pageHeight >= 1800) {
  const keyboard = document.querySelector('.keyboard'); //Keyboard
  let keys = document.querySelectorAll('.keys'); //Teclas
  let letters = Array.from(keys).filter(key => !key.classList.contains("special_key") && !key.classList.contains("disabled")); //Letras
  const inputs = document.querySelectorAll('input'); //Inputs
  let activeInput = null; //Input activo

  //Para cada input le agrego un evento click
  inputs.forEach(input => {
    input.addEventListener('click', function () {
      activeInput = input; // Input actual
      keyboard.classList.add('active'); //Abrir teclado
    });
    if (input.hasAttribute('autofocus')) { //Si tiene el atributo autofocus
      keyboard.classList.add('active'); //Abrir teclado
    }
  });

  //Para cada key le agrego un evento click
  keys.forEach(key => {
    key.setAttribute('keyname', key.textContent); //Agrego el atributo keyname con el nombre de la tecla
    if (!key.classList.contains("caps_lock_key") && !key.classList.contains("shift_left")) {
      key.addEventListener('click', function () {
        KeyClick(key, activeInput) //Funcion para agregar una letra al input
      })
    }
  })

  //Tecla enter
  const enterKey = document.querySelector('.enter_key').addEventListener('click', function () {
    EnterKey(activeInput);
  });

  //Tecla backspace
  const backspaceKey = document.querySelector('.backspace_key')
  backspaceKey.addEventListener('mousedown', function () {//Si se mantiene presionada la tecla
    BackspaceKeyDown(activeInput)
  });

  backspaceKey.addEventListener('mouseup', function () {//Si se suelta la tecla
    BackspaceKeyUp(activeInput);
  });

  //Tecla espacio
  const spaceKey = document.querySelector('.space_key').addEventListener('click', function () {
    SpaceKey(activeInput);
  });

  //Tecla Bloq mayus
  const caps_lock_key = document.querySelector('.caps_lock_key')
  caps_lock_key.addEventListener('click', function () {
    BloqMayusKey();
  });

  //Tecla shift
  const shift_left = document.querySelector('.shift_left')
  shift_left.addEventListener('click', function () {
    ShiftKey();
  });

  //FUNCIONES

  function mayusLetters(letter) {
    letter.innerText = letter.innerText.toUpperCase(); //Letras en mayuscula
  }

  function normalLetters(letter) {
    letter.innerText = letter.getAttribute('keyname'); //Letras en minuscula
  }

  //Funcion para agregar una letra al input
  function KeyClick(key, input) {
    let onlynumbers = input.classList.contains("onlynumbers") //Verificar si el input tiene la clase solo numeros

    key.classList.add('active'); //Agrego la clase active
    setTimeout(() => { //Despues de 200ms remuevo la clase active
      key.classList.remove('active')
    }, 200);

    // sourcery skip: merge-nested-ifs
    if (letters.includes(key)) {
      if (!onlynumbers || (onlynumbers && !isNaN(key.innerText))) { //Si el campo no tiene la clase solonumeros || Si el campo es de solo numeros y la key es un numero
        input.value += key.innerText;
      }
    }

  }

  //Funcion para agregar un enter
  function EnterKey(input) {
    let form = input.closest('form'); //Formulario actual
    form.submit(); //Envio el formulario
  }

  //Funcion para agregar un espacio al input
  function BackspaceKeyDown(input) {
    backspaceKey.classList.add('active');
    actionInterval = setInterval(() => { //Cada 70ms remuevo el ultimo caracter del input
      input.value = input.value.slice(0, -1);
    }, 60);
  }

  function BackspaceKeyUp() {
    backspaceKey.classList.remove('active');
    clearInterval(actionInterval);//Paro el intervalo
  }

  //Funcion para agregar un espacio al input
  function SpaceKey(input) {
    input.value += ' ';
  }

  //Funcion para bloquear mayusculas
  function BloqMayusKey() {
    caps_lock_key.classList.toggle("active");

    letters.forEach(letter => { //Para cada letra
      if (caps_lock_key.classList.contains('active')) { //Si bloq mayus esta activa
        mayusLetters(letter);
        letter.addEventListener("click", function () {
          letters.forEach(function (letter) {
            mayusLetters(letter);
          })
        });
      } else {
        normalLetters(letter); //Si no volver a la normalidad
      }
    });
  };


  //Funcion shift
  function ShiftKey() {
    shift_left.classList.toggle('active');

    letters.forEach(letter => { //Para cada letra
      if (shift_left.classList.contains('active')) {
        mayusLetters(letter);
        letter.addEventListener("click", function () {
          letters.forEach(letter => {
            normalLetters(letter);
          });
          shift_left.classList.remove('active'); //Remover la clase active 
        });
      } else {
        normalLetters(letter);
      }
    });
  }


}

//BARCODE CAMARA
const barcodeCam = document.getElementById('barcode-cam'); //Zona de la camara
const codeInput = document.getElementById("code-input") //Input codigo
const codeForm = document.getElementById("code-form") //Form codigo

document.addEventListener("DOMContentLoaded", () => {

  Quagga.init({ //Inicializar Quagga
    inputStream: { constraints: { width: 600, height: 600,}, name: "Live", type: "LiveStream", target: barcodeCam}, // Pasar el elemento del DOM
    decoder: { readers: ["code_39_reader", "code_128_reader"] }, // Listado de los tipos de códigos de barras a leer
    locate: false,
    frequency: 100,
  }, function (err) {if (err) {console.log(err);return}
    console.log("Iniciado correctamente");
    Quagga.start(); //Iniciar Quagga
  });

  Quagga.onDetected((data) => { //Al detectar el codigo
    codeInput.value = data.codeResult.code; //Poner el codigo en el input
    // Imprimimos todo el data en consola
    console.log(data);
    Quagga.stop(); //Detener Quagga

    codeForm.submit(); //Enviar el formulario
  });

});

//CAMARA

// Obtener referencia al elemento de video y al canvas
const camaraModal = document.getElementById('camaraModal');
if (camaraModal) {
  const btncamAccess = document.getElementById('user-picture-btn');
  const btnSave = document.getElementById('user-savepicture-btn');
  const btnRepeat = document.getElementById('user-repeatpicture-btn');
  const btnTake = document.getElementById('user-takepicture-btn');
  let video = document.getElementById('user-cam');
  let canvas = document.getElementById('user-picture');
  let context = canvas.getContext('2d');

  canvas.width = 640;
  canvas.height = 680;
  const contadorElemento = document.getElementById('contador');

  function iniciarCuentaRegresiva(duracionSegundos, callback) {
    let tiempoRestante = duracionSegundos;
    contadorElemento.style.display = 'block';
    contadorElemento.textContent = tiempoRestante;

    const intervalo = setInterval(() => {
      tiempoRestante--;
      if (tiempoRestante > 0) {
        contadorElemento.textContent = tiempoRestante;
      } else {
        clearInterval(intervalo);
        contadorElemento.style.display = 'none';
        callback(); // Llama a captureImage() u otra función
      }
    }, 1000);
  }

  btncamAccess.addEventListener('click', () => {
  navigator.mediaDevices.getUserMedia({ video: true, width: 640, height: 680 })
    .then(function (stream) {
      video.srcObject = stream;
      video.play();

      const videoTrack = stream.getVideoTracks()[0];

      camaraModal.addEventListener('hidden.bs.modal', function () {
        videoTrack.stop();
        video.srcObject = null;
      });

      // MOSTRAR VIDEO y OCULTAR CANVAS (por si quedó de antes)
      canvas.style.display = 'none';
      video.style.display = 'block';

      // Iniciar cuenta regresiva y luego tomar la foto automáticamente
      iniciarCuentaRegresiva(4, () => {
        captureImage();
        // saveImage(); // <- descomenta si también quieres que se guarde sola
      });

    })
    .catch(function (error) {
      console.log('Error al acceder a la webcam:', error);
      });
  });



  // Función para capturar la imagen
  function captureImage() {
    btnTake.style.display = 'none';
    video.style.display = 'none';
    canvas.style.display = 'block';

    btnRepeat.style.display = 'block';
    btnSave.style.display = 'block';

    // Dibujar el cuadro actual del video en el canvas
    context.drawImage(video, 0, 0, canvas.width, canvas.height);
  }

  // Función para convertir la imagen base64 en un objeto de archivo
  function dataURLtoFile(dataUrl, filename) {
    const arr = dataUrl.split(',');
    const mime = arr[0].match(/:(.*?);/)[1];
    const bstr = atob(arr[1]);
    let n = bstr.length;
    const u8arr = new Uint8Array(n);
    while (n--) {
      u8arr[n] = bstr.charCodeAt(n);
    }
    return new File([u8arr], filename, { type: mime });
  }

  function repeatImage() {
    btnRepeat.style.display = 'none';
    btnSave.style.display = 'none';
    btnTake.style.display = 'block';

    canvas.style.display = 'none';
    video.style.display = 'block';
  }

  function saveImage() {
    // Verifica que canvas exista
    if (!canvas) {
      console.error('No se encontró el canvas.');
      return;
    }
  
    // Obtener la imagen en formato base64 desde el canvas
    const imageData = canvas.toDataURL('image/png');
    const capturedImage = imageData;
  
    // Generar un archivo desde la imagen base64
    const file = dataURLtoFile(capturedImage, 'captured_image.png');
  
    // Crear una instancia de DataTransfer
    const dataTransfer = new DataTransfer();
    dataTransfer.items.add(file);
  
    // Lista de posibles IDs de campos file
    const fileIds = ['device-file', 'user-file', 'vehicle-file', 'id_extra'];
  
    let applied = false;
  
    fileIds.forEach(id => {
      const fileInput = document.getElementById(id);
      if (fileInput) {
        fileInput.files = dataTransfer.files;
  
        // Disparar evento de cambio para activar cualquier lógica asociada
        const changeEvent = new Event('change');
        fileInput.dispatchEvent(changeEvent);
  
        console.log(`Imagen asignada a ${id}`);
        applied = true;
      }
    });
  
    if (!applied) {
      console.warn('⚠️ No se encontró ningún input file válido.');
    }
  }
  
}

  function openSelect(btn) {
    btn.classList.toggle("open");
  }


  window.openSelect = openSelect;

  const vehicleInput = document.getElementById('vehicle');
  const devicesInput = document.getElementById('devices');

  const deviceItems = document.querySelectorAll(".item-device");
  const btnText = document.querySelector(".device .btn-text");

  deviceItems.forEach(item => {
    item.addEventListener("click", () => {
      item.classList.toggle("checked");

      const checkedItems = document.querySelectorAll(".item-device.checked");
      const valuesChecks = [...checkedItems].map(checkedItem =>
        checkedItem.getAttribute("value")
      );

      devicesInput.value = valuesChecks.join(",");

      if (checkedItems.length > 1) {
        btnText.innerText = `${checkedItems.length} Seleccionados`;
      } else if (checkedItems.length === 1) {
        btnText.innerText = checkedItems[0].innerText;
      } else {
        btnText.innerText = "Seleccionar Dispositivos";
      }
    });
  });




//Seleccionar vehiculos
const vehicleItems = document.querySelectorAll(".item-vehicle");
const btnTextVehicle = document.querySelector(".vehicle .btn-text");

vehicleItems.forEach(item => {
  item.addEventListener("click", () => {
    if (item.classList.contains("checked")) {
      item.classList.remove("checked");
    } else {
      // Remover la clase 'checked' de todos los elementos
      vehicleItems.forEach(otherItem => otherItem.classList.remove("checked"));
      // Agregar la clase 'checked' al elemento clicado
      item.classList.add("checked");
    }

    // Buscar el elemento clicado con la clase 'checked'
    const checkedItem = document.querySelector(".item-vehicle.checked");

    if (checkedItem) {
      // Actualizar el valor y el texto basados en el elemento seleccionado
      const valueCheck = checkedItem.getAttribute("value");
      vehicleInput.value = valueCheck;
      btnTextVehicle.innerText = checkedItem.innerText;
    } else {
      // Si no hay elementos seleccionados, restaurar los valores predeterminados
      btnTextVehicle.innerText = "Seleccionar Vehiculo";
      vehicleInput.value = "";
    }
  });
});



//ADMIN

//Menu Admin
const btn = document.querySelector("#menu-btn");
const menu = document.querySelector("#sidemenu");
const { body } = document
const list = document.querySelectorAll('.item')

if (btn && menu) {
  btn.addEventListener('click', () => {
    menu.classList.toggle("menu-expanded");
    menu.classList.toggle("menu-collapsed");

    body.classList.toggle("body-expanded");
    body.classList.toggle("body-collapsed")
  });
}

//Animacion admin | Cambiar entre tabla select y form
const btnRegister = document.getElementById('btn-register-users');
const btnBack = document.getElementById('btn-back');
const rol = document.querySelector('.select-rol');
const card = document.querySelector('.users');

if (card) {
  btnRegister.addEventListener('click', () => {
    card.classList.add('select');
  });

  btnBack.addEventListener('click', () => {
    card.classList.remove('select');
  });
}

// Eliminar filas con Checks
document.addEventListener('DOMContentLoaded', function () {
  const generalDeleteForm = document.getElementById('delete-form');
  const checks = document.querySelectorAll('.item-check');
  const actions = document.querySelector('.card-table-buttons');

  if (generalDeleteForm) {
    checks.forEach(function (checkbox) {
      checkbox.addEventListener('change', function () {
        const Selected = Array.from(checks).some(function (cb) {
          return cb.checked;
        });

        if (Selected) {
          actions.classList.add('active');
        } else {
          actions.classList.remove('active');
        }
      });
    });

    generalDeleteForm.addEventListener('submit', function (e) {
      e.preventDefault(); // Evita que el formulario se envíe automáticamente

      const selectedItems = [];
      for (let i = 0; i < checks.length; i++) {  // Cambiado a 'let'
        if (checks[i].checked) {
          selectedItems.push(checks[i].value); // Agrega los valores seleccionados al array
        }
      }
      const hiddenInput = document.createElement('input');
      hiddenInput.setAttribute('type', 'hidden');
      hiddenInput.setAttribute('name', 'checks-users');
      hiddenInput.setAttribute('value', selectedItems.join(','));

      generalDeleteForm.appendChild(hiddenInput); // Agrega el campo oculto al formulario

      generalDeleteForm.submit(); // Envía el formulario
    });

    //Delete individual
    const individualDeleteForm = document.getElementById('delete-user');

    individualDeleteForm.addEventListener('click', function (e) {
      idUser = this.getAttribute('data-id');
      const hiddenInput = document.createElement('input');
      hiddenInput.setAttribute('type', 'hidden');
      hiddenInput.setAttribute('name', 'delete-user');
      hiddenInput.setAttribute('value', idUser);

      generalDeleteForm.appendChild(hiddenInput); // Agrega el campo oculto al formulario
    });
  }
});

//SEARCH EN TIEMPO REAL
const search = document.getElementById("search");
if (search) {
  const tabla = document.querySelector("table");
  const tbody = tabla.querySelector("tbody");
  const filas = tbody.getElementsByTagName("tr");

  search.addEventListener("input", function () {
    const filtro = search.value.toLowerCase();

    for (const i = 0; i < filas.length; i++) {
      const fila = filas[i];
      const celdas = fila.getElementsByTagName("td");
      const mostrarFila = false;

      for (const j = 0; j < celdas.length; j++) {
        const celda = celdas[j];
        if (celda) {
          const contenido = celda.innerHTML.toLowerCase();
          if (contenido.indexOf(filtro) > -1) {
            mostrarFila = true;
            break;
          }
        }
      }

      if (mostrarFila) {
        fila.style.display = "";
      } else {
        fila.style.display = "none";
      }
    }
  });
}




