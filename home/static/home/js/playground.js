let inputs = [];
const template =
  '<div class="text-center bg-dark mx-2 my-1 p-1 rounded-lg">{{text}}</div>';

$('input[name="query"]').focus();

$("#analysis-form").submit(function (e) {
  e.preventDefault();
  return;
  // i have disabled this for the time being because I can not determine
  // what to actually do after the form is submitted

  //   var form = $(this);
  //   var url = "/playground-response/";
  //   const input = $('input[name="query"]').val();
  //   if (!input) {
  //     alert("Please type something!");
  //     return;
  //   }
  //   $.ajax({
  //     type: "GET",
  //     url: url,
  //     data: form.serialize(),
  //     success: function (data) {
  //       inputs.push(input);
  //       $("#input-texts").append(template.replace("{{text}}", input));
  //     },
  //   });
});

const happyFace = $("#happy-face");
const neutralFace = $("#neutral-face");
const sadFace = $("#sad-face");
const classToAdd = "text-yellow";

$("#input-statement").on("input", function (element) {
  const input = $('input[name="query"]').val();
  var url = "/playground-polarity-response/";
  $.ajax({
    type: "GET",
    url: url,
    data: { input: input },
    success: function (data) {
      if (data.polarity == 0) {
        neutralFace.addClass(classToAdd);
        happyFace.removeClass(classToAdd);
        sadFace.removeClass(classToAdd);
      } else if (data.polarity > 0) {
        happyFace.addClass(classToAdd);
        neutralFace.removeClass(classToAdd);
        sadFace.removeClass(classToAdd);
      } else {
        sadFace.addClass(classToAdd);
        happyFace.removeClass(classToAdd);
        neutralFace.removeClass(classToAdd);
      }
    },
  });
});
