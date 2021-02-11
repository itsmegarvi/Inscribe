let inputs = [];
const template =
  '<div class="text-danger text-center bg-dark mx-2 my-1 p-1 rounded-lg">{{text}}</div>';

$("#analysis-form").submit(function (e) {
  e.preventDefault();
  var form = $(this);
  var url = "/playground-response/";
  const input = $('input[name="query"]').val();
  if (!input) {
    alert("Please type something!");
    return;
  }
  $.ajax({
    type: "GET",
    url: url,
    data: form.serialize(),
    success: function (data) {
      inputs.push(input);
      $("#input-texts").append(template.replace("{{text}}", input));
    },
  });
});

const happyFace = $("#happy-face");
const neutralFace = $("#neutral-face");
const sadFace = $("#sad-face");

$("#input-statement").on("input", function (element) {
  const input = $('input[name="query"]').val();
  var url = "/playground-polarity-response/";
  $.ajax({
    type: "GET",
    url: url,
    data: { input: input },
    success: function (data) {
      if (data.polarity == 0) {
        neutralFace.addClass("text-danger");
        happyFace.removeClass("text-danger");
        sadFace.removeClass("text-danger");
      } else if (data.polarity > 0) {
        happyFace.addClass("text-danger");
        neutralFace.removeClass("text-danger");
        sadFace.removeClass("text-danger");
      } else {
        sadFace.addClass("text-danger");
        happyFace.removeClass("text-danger");
        neutralFace.removeClass("text-danger");
      }
    },
  });
});
