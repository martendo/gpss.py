// Info section: Toggle display when "Info" button pressed
const info = document.getElementById("info");
document.getElementById("info-btn").addEventListener("click", () => {
  if (info.style.display === "") {
    info.style.display = "unset";
  } else {
    info.style.display = "";
  }
});

// Ace code editor
const editor = ace.edit("editor");
editor.setOptions({
  mode: "ace/mode/gpss",
  theme: "ace/theme/textmate",
  useSoftTabs: true,
  printMargin: false,
  displayIndentGuides: false,
  tabSize: 8,
});
editor.focus();

// Column resizing: Drag separator to resize
const main = document.getElementById("main");
const consoleContainer = document.getElementById("console-container");
const responseSeparator = document.getElementById("response-separator");
var dragging = null;
[
  {
    container: main,
    box: document.getElementById("editor-container"),
    separator: document.getElementById("main-separator"),
    column: true,
  },
  {
    container: document.getElementById("response-container"),
    box: consoleContainer,
    separator: responseSeparator,
    column: false,
  },
].forEach((resize) => {
  resize.separator.addEventListener("pointerdown", () => {
    dragging = resize.separator;
    main.classList.add("no-select");
  });
  document.addEventListener("pointerup", () => {
    dragging = null;
    main.classList.remove("no-select");
  });
  document.addEventListener("pointermove", (event) => {
    if (dragging !== resize.separator) {
      return false;
    }
    const rect = resize.container.getBoundingClientRect();
    if (resize.column) {
      resize.box.style.width = `${event.clientX - rect.left - (15 / 2)}px`;
    } else {
      resize.box.style.height = `${event.clientY - rect.top - (15 / 2)}px`;
    }
    editor.resize();
  });
});
document.addEventListener("touchmove", (event) => {
  if (dragging) {
    event.preventDefault();
  }
}, { passive: false });

// gpss-server communication
const output = document.getElementById("output");
const console = document.getElementById("console");

function responseError(response) {
  output.textContent = "An unknown response was received from the server." + "\n\n" + response;
}

var timeout;
document.getElementById("simulate-btn").addEventListener("click", () => {
  const request = new XMLHttpRequest();
  request.addEventListener("error", () => {
    clearTimeout(timeout);
    output.textContent = "An error occurred while transferring data with the server.";
  });
  request.addEventListener("load", () => {
    clearTimeout(timeout);
    try {
      data = JSON.parse(request.responseText);
    } catch (error) {
      if (error instanceof SyntaxError) {
        responseError(request.responseText);
      } else {
        throw error;
      }
    }
    
    const messages = [];
    const annotations = [];
    for (const message of data.messages) {
      var type, subtype;
      switch (message.type) {
        case "parser-error":
          type = "error";
          subtype = "Parser error";
          break;
        case "simulation-error":
          type = "error";
          subtype = "Simulation error";
          break;
        case "warning":
          type = "warning";
          break;
      }
      messages.push(`${type.toUpperCase()}: ${subtype ? subtype + ": " : ""}Line ${message.linenum}:\n    ${message.message}`);
      annotations.push({
        row: message.linenum - 1,
        column: 0,
        type: type,
        text: message.message,
      });
    }
    if (messages.length) {
      console.textContent = messages.join("\n");
      consoleContainer.style.display = "";
      responseSeparator.style.display = "";
    } else {
      consoleContainer.style.display = "none";
      responseSeparator.style.display = "none";
    }
    editor.session.setAnnotations(annotations);
    
    output.textContent = data.report || data.message;
  });
  request.open("POST", "https://gpss-server.herokuapp.com");
  request.send(editor.getValue().replace(/[;*].*$/mg, "").replace(/[^\S\n]{2,}/g, " "));
  
  output.textContent = "Program sent to server.";
  timeout = setTimeout(() => {
    output.textContent += "\n\nYou might be waking up the server.\nJust a few more seconds!";
  }, 4000);
});
