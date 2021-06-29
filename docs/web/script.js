const info = document.getElementById("info");
document.getElementById("info-btn").addEventListener("click", () => {
  if (info.style.display === "") {
    info.style.display = "unset";
  } else {
    info.style.display = "";
  }
});

const output = document.getElementById("output");

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
    editor.session.setAnnotations(annotations);
    
    if (data.message) {
      messages.push(data.message);
    }
    if (data.report) {
      if (messages.length) {
        messages.push("------------------------------------------------------------------------");
      }
      messages.push(data.report);
    }
    output.textContent = messages.join("\n");
  });
  request.open("POST", "https://gpss-server.herokuapp.com");
  request.send(editor.getValue());
  
  output.textContent = "Program sent to server.";
  timeout = setTimeout(() => {
    output.textContent += "\n\nYou might be waking up the server.\nJust a few more seconds!";
  }, 5000);
});
