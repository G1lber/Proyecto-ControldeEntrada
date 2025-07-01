document.addEventListener("DOMContentLoaded", () => {
  const input = document.getElementById("code-input");
  const keyboardContainer = document.getElementById("keyboard-container");
  const toggleBtn = document.getElementById("toggleExtrasBtn");
  let keyboard;
  let isKeyboardVisible = false;

  function initKeyboard() {
    if (!keyboard) {
      keyboard = new SimpleKeyboard.default({
        onChange: inputChanged => {
          input.value = inputChanged;
        },
        onKeyPress: button => {
          if (button === "{enter}") {
            document.getElementById("code-form")?.submit();
          }
        },
        layout: {
          default: [
            "1 2 3 4 5 6 7 8 9 0",
            "q w e r t y u i o p",
            "a s d f g h j k l",
            "z x c v b n m",
            "{space} {bksp} {enter}"
          ]
        },
        display: {
          "{bksp}": "⌫",
          "{enter}": "⏎",
          "{space}": "␣"
        }
      });
    }
    keyboard.setInput(input.value);
  }

  function toggleKeyboard() {
    if (!isKeyboardVisible) {
      keyboardContainer.classList.remove("d-none"); // Mostrar primero
      initKeyboard(); // Luego inicializar
      input.focus();
      isKeyboardVisible = true;
    } else {
      keyboardContainer.classList.add("d-none");
      isKeyboardVisible = false;
    }
  }

  // Mostrar teclado al dar clic en botón de extras
  toggleBtn.addEventListener("click", toggleKeyboard);

  // Mostrar teclado si el input recibe focus directamente
  input.addEventListener("focus", () => {
    if (!isKeyboardVisible) {
      keyboardContainer.classList.remove("d-none");
      isKeyboardVisible = true;
      initKeyboard();
    }
  });

  // Ocultar teclado si se hace clic fuera del input, botón o contenedor
  document.addEventListener("mousedown", (event) => {
    const target = event.target;
    if (
      target !== input &&
      target !== toggleBtn &&
      !keyboardContainer.contains(target)
    ) {
      keyboardContainer.classList.add("d-none");
      isKeyboardVisible = false;
    }
  });

  // Limpia la URL si tiene parámetros (?extras=true)
  history.replaceState(null, null, window.location.pathname);
});
