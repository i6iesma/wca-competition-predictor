document.addEventListener("DOMContentLoaded", function () {
  const buttonLeft = document.getElementById("buttonLeft");
  const table = document.getElementById("table-id");
  console.log(table);
  let mode = document.getElementById("mode_p");
  let pb_users = document.getElementById("jsonified_pb_users").innerText;
  pb_users = JSON.parse(pb_users);
  let mode_text = document.getElementById("mode-describer");
  console.log(pb_users);
  let smart_prediction_users = document.getElementById(
    "jsonified_smart_prediction_users"
  ).innerText;
  smart_prediction_users = JSON.parse(smart_prediction_users);
  console.log(smart_prediction_users);

  function change_mode() {
    console.log("changing mode");
    if (mode.innerText == "pb") {
      console.log("mode value is pb");
      rows = table.children[0].children;
      for (let i = 1; i < rows.length; i++) {
        result = rows[i].children[2].innerText;
        rows[i].children[2].innerText = smart_prediction_users[i - 1].result;
        mode.innerText = "smart_prediction";
        mode_text.innerText = "By a smart prediction";
      }
    } else if (mode.innerText == "smart_prediction") {
      rows = table.children[0].children;
      for (let i = 1; i < rows.length; i++) {
        result = rows[i].children[2].innerText;
        rows[i].children[2].innerText = pb_users[i - 1].result;
        mode.innerText = "pb";
        mode_text.innerText = "By PB on the event specified";
      }
    }
  }
  buttonLeft.addEventListener("click", change_mode);
  buttonRight.addEventListener("click", change_mode);
});
