document.addEventListener("DOMContentLoaded", function () {
  let event = document.getElementById("event_p").innerText;
  let currentEvent = document.getElementById("333");
  const buttonSingle = document.getElementById("button-single");
  const buttonAvg = document.getElementById("button-avg");
  var spans = document.getElementsByTagName("span");
  let currentFormat = document.getElementById("format_p").innerText;
  if (currentFormat === "single") {
    currentFormat = "single";
    buttonAvg.style.backgroundColor = "gray";
    buttonSingle.style.backgroundColor = "var(--soft-accent)";
  } else {
    currentFormat = "avg";
    buttonSingle.style.backgroundColor = "gray";
    buttonAvg.style.backgroundColor = "var(--soft-accent)";
  }
  for (i = 0; i < spans.length; i++) {
    if (event === spans[i].id) {
      spans[i].style.color = "var(--accent)";
      currentEvent = spans[i];
    }
    spans[i].addEventListener("click", function () {
      console.log(currentEvent);
      try {
        currentEvent.style.color = "";
      } finally {
        this.style.color = "#0cf3a2";
        currentEvent = this;
      }
    });
  }

  buttonSingle.addEventListener("click", function (e) {
    e.preventDefault();
    currentFormat = "single";
    buttonAvg.style.backgroundColor = "gray";
    buttonSingle.style.backgroundColor = "var(--soft-accent)";
  });
  buttonAvg.addEventListener("click", function (e) {
    e.preventDefault();
    currentFormat = "avg";
    buttonSingle.style.backgroundColor = "gray";
    buttonAvg.style.backgroundColor = "var(--soft-accent)";
  });

  var form = document.getElementById("event-form");
  form.addEventListener("submit", function () {
    form.event.value = currentEvent.id;
    form.format.value = currentFormat;
    return true;
  });

  const buttonLeft = document.getElementById("buttonLeft");
  const table = document.getElementById("table-id");
  let mode = document.getElementById("mode_p");
  let pb_users = document.getElementById("jsonified_pb_users").innerText;
  pb_users = JSON.parse(pb_users);
  let mode_text = document.getElementById("mode-describer");
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
        rows[i].children[2].innerText = smart_prediction_users[i - 1].result;
        rows[i].children[1].innerText = smart_prediction_users[i - 1].name;
        mode.innerText = "smart_prediction";
        mode_text.innerText = "By a smart prediction";
      }
    } else if (mode.innerText == "smart_prediction") {
      console.log("mode value is smart prediction");
      rows = table.children[0].children;
      for (let i = 1; i < rows.length; i++) {
        rows[i].children[2].innerText = pb_users[i - 1].result;
        rows[i].children[1].innerText = pb_users[i - 1].name;
        mode.innerText = "pb";
        mode_text.innerText = "By PB";
      }
    }
  }
  buttonLeft.addEventListener("click", change_mode);
  buttonRight.addEventListener("click", change_mode);
});
