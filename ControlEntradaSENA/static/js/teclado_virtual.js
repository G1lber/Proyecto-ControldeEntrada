document.addEventListener("DOMContentLoaded", () => {
  const input = document.getElementById("code-input");
  const keyboardContainer = document.getElementById("keyboard-container");
  let keyboard;

  function showKeyboard() {
    keyboardContainer.style.display = "block";
    if (!keyboard) {
      keyboard = new SimpleKeyboard.default({
        onChange: inputChanged => {
          input.value = inputChanged;
        },
        onKeyPress: button => {
          if (button === "{enter}") {
            document.getElementById("code-form").submit();
          }
        },
        layout: {
          default: [
            "1 2 3",
            "4 5 6",
            "7 8 9",
            "0 {bksp} {enter}"
          ]
        },
        display: {
          "{bksp}": "⌫",
          "{enter}": "⏎"
        }
      });
    }
    keyboard.setInput(input.value);
  }

  input.addEventListener("focus", showKeyboard);

  input.addEventListener("mousedown", (e) => {
    e.preventDefault();
    input.focus();
    showKeyboard();
  });

  // Quitamos el preventDefault aquí para que el evento se propague y pueda cerrar el teclado
  // keyboardContainer.addEventListener("mousedown", e => {
  //   e.preventDefault();
  // });

  document.addEventListener("mousedown", (event) => {
    const target = event.target;
    if (target !== input && !keyboardContainer.contains(target)) {
      keyboardContainer.style.display = "none";
    }
  });
});