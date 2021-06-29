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
    const annotations = [];
    switch (data.status) {
      case "parser-error":
        const errors = [];
        for (const error of data.errors) {
          errors.push(`ERROR: Parser error: Line ${error.linenum}:\n    ${error.message}`);
          annotations.push({
            row: error.linenum - 1,
            column: 0,
            type: "error",
            text: error.message,
          });
        }
        output.textContent = data.message + "\n\n" + errors.join("\n");
        break;
      case "simulation-error":
        output.textContent = data.message + "\n\n" + `ERROR: Simulation error: Line ${data.error.linenum}:\n    ${data.error.message}`;
        editor.session.setAnnotations([{
          row: data.error.linenum - 1,
          column: 0,
          type: "error",
          text: data.error.message,
        }]);
        break;
      case "success":
        output.textContent = data.report;
        break;
      default:
        responseError(request.responseText);
        break;
    }
    for (const warning of data.warnings) {
      annotations.push({
        row: warning.linenum - 1,
        column: 0,
        type: "warning",
        text: warning.message,
      });
    }
    editor.session.setAnnotations(annotations);
  });
  request.open("POST", "https://gpss-server.herokuapp.com");
  request.send(editor.getValue());
  
  output.textContent = "Program sent to server.";
  timeout = setTimeout(() => {
    output.textContent += "\n\nYou might be waking up the server.\nJust a few more seconds!";
  }, 5000);
});
