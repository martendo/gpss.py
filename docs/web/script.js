const output = document.getElementById("response").getElementsByTagName("code")[0];

const editor = ace.edit("editor");
editor.setOptions({
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
document.getElementById("simulateBtn").addEventListener("click", () => {
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
    switch (data.status) {
      case "parser-error":
        const errors = [];
        for (const error of data.errors) {
          errors.push(`ERROR: Parser error: Line ${error["linenum"]}:\n    ${error["message"]}`);
        }
        output.textContent = data.message + "\n\n" + errors.join("\n");
        break;
      case "simulation-error":
        output.textContent = data.message + "\n\n" + `ERROR: Simulation error: Line ${data.error.linenum}:\n    ${data.error.message}`;
        break;
      case "success":
        output.textContent = data.report;
        break;
      default:
        responseError(request.responseText);
        break;
    }
  });
  request.open("POST", "https://gpss-server.herokuapp.com");
  request.send(editor.getValue());
  
  output.textContent = "Program sent to server";
  timeout = setTimeout(() => {
    output.textContent += "\n\nYou might be waking up the server.\nJust a few more seconds!";
  }, 5000);
});