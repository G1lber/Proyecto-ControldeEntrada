document.addEventListener("DOMContentLoaded", () => {
  const input = document.getElementById("code-input");
  const keyboardContainer = document.getElementById("keyboard-container");
  let keyboard;

  function initKeyboard() {
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
  }

  function showKeyboardIfDocumento() {
    if (typeof modo !== 'undefined' && modo === "documento") {
      initKeyboard();
      keyboardContainer.style.display = "block";
      keyboard.setInput(input.value);
    } else {
      keyboardContainer.style.display = "none";
    }
  }

  input.addEventListener("focus", showKeyboardIfDocumento);

  input.addEventListener("mousedown", (e) => {
    if (typeof modo === 'undefined' || modo !== "documento") return;
    e.preventDefault();
    input.focus();
    showKeyboardIfDocumento();
  });

  document.addEventListener("mousedown", (event) => {
    const target = event.target;
    if (target !== input && !keyboardContainer.contains(target)) {
      keyboardContainer.style.display = "none";
    }
  });
});
