document.addEventListener("DOMContentLoaded", () => {
  let extrasEditados = {};
  let currentCapturedImage = null;
  let stream = null;

  const descripcionInput = document.getElementById("editDescripcion");
  const fotoPreview = document.getElementById("editFotoPreview");
  const inputId = document.getElementById("editExtraId");

  const extraCam = document.getElementById("editExtraCam");
  const canvas = document.getElementById("editExtraCanvas");
  const startCamBtn = document.getElementById("startExtraCamera");
  const takePhotoBtn = document.getElementById("takeExtraPhoto");
  const repeatPhotoBtn = document.getElementById("repeatPhotoBtn") || document.getElementById("repeatExtraPhoto");
  const form = document.getElementById("form-access");

  // Abrir modal con datos
  document.querySelectorAll(".ver-detalle-btn").forEach(btn => {
    btn.addEventListener("click", () => {
      const id = btn.getAttribute("data-id");
      const descripcion = btn.getAttribute("data-descripcion");
      const foto = btn.getAttribute("data-foto");

      inputId.value = id;
      descripcionInput.value = descripcion;
      fotoPreview.src = foto;

      // Reset estado cámara
      extraCam.style.display = "none";
      canvas.style.display = "none";
      fotoPreview.style.display = "block";
      startCamBtn.style.display = "inline-block";
      takePhotoBtn.style.display = "none";
      repeatPhotoBtn.style.display = "none";
      currentCapturedImage = null;
    });
  });

  // Iniciar cámara
  startCamBtn?.addEventListener("click", async () => {
    try {
      stream = await navigator.mediaDevices.getUserMedia({ video: true });
      extraCam.srcObject = stream;
      extraCam.style.display = "block";
      takePhotoBtn.style.display = "inline-block";
      repeatPhotoBtn.style.display = "none";
      fotoPreview.style.display = "none";
      canvas.style.display = "none";
    } catch (err) {
      alert("No se pudo acceder a la cámara.");
    }
  });

  // Tomar foto
  takePhotoBtn?.addEventListener("click", () => {
    const context = canvas.getContext("2d");
    canvas.width = extraCam.videoWidth;
    canvas.height = extraCam.videoHeight;
    context.drawImage(extraCam, 0, 0);
    canvas.style.display = "block";
    extraCam.style.display = "none";
    takePhotoBtn.style.display = "none";
    repeatPhotoBtn.style.display = "inline-block";

    currentCapturedImage = canvas.toDataURL("image/jpeg");
    fotoPreview.src = currentCapturedImage;
    fotoPreview.style.display = "block";
  });

  // Repetir foto
  repeatPhotoBtn?.addEventListener("click", () => {
    canvas.style.display = "none";
    extraCam.style.display = "block";
    takePhotoBtn.style.display = "inline-block";
    repeatPhotoBtn.style.display = "none";
  });

  // Guardar cambios (modal)
  document.getElementById("guardarCambiosExtra")?.addEventListener("click", () => {
    const id = inputId.value;
    const nuevaDescripcion = descripcionInput.value.trim();

    extrasEditados[id] = {
      descripcion: nuevaDescripcion,
      foto: currentCapturedImage
    };

    const card = document.querySelector(`.ver-detalle-btn[data-id="${id}"]`)?.closest(".extra-card");
    if (card) {
      card.querySelector("p").innerText = nuevaDescripcion;

      const boton = card.querySelector(".ver-detalle-btn");
      if (boton) {
        boton.setAttribute("data-descripcion", nuevaDescripcion);
        if (currentCapturedImage) {
          boton.setAttribute("data-foto", currentCapturedImage);
        }
      }

      const imgCard = card.querySelector("img");
      if (imgCard && currentCapturedImage) {
        imgCard.src = currentCapturedImage;
      }
    }

    bootstrap.Modal.getInstance(document.getElementById("extraDetalleModal"))?.hide();

    if (stream) {
      stream.getTracks().forEach(track => track.stop());
      stream = null;
    }
  });

  // Antes de enviar el formulario
  form?.addEventListener("submit", () => {
    const extrasArray = [];

    for (const [id, datos] of Object.entries(extrasEditados)) {
      extrasArray.push({
        id: id,
        descripcion: datos.descripcion
      });

      // Si hay imagen capturada, convertirla y subirla como input file
      if (datos.foto) {
        const file = dataURLtoFile(datos.foto, `foto_extra_${id}.jpg`);
        const fileInput = document.createElement("input");
        fileInput.type = "file";
        fileInput.name = `foto_extra_${id}`;
        const dataTransfer = new DataTransfer();
        dataTransfer.items.add(file);
        fileInput.files = dataTransfer.files;
        fileInput.style.display = "none";
        form.appendChild(fileInput);
      }
    }

    const inputJson = document.getElementById("extras_editados_json");
    if (inputJson) {
      inputJson.value = JSON.stringify(extrasArray);
    }
  });
});

// Función para convertir base64 a archivo (reutilizable)
function dataURLtoFile(dataUrl, filename) {
  const arr = dataUrl.split(",");
  const mime = arr[0].match(/:(.*?);/)[1];
  const bstr = atob(arr[1]);
  let n = bstr.length;
  const u8arr = new Uint8Array(n);
  while (n--) {
    u8arr[n] = bstr.charCodeAt(n);
  }
  return new File([u8arr], filename, { type: mime });
}
