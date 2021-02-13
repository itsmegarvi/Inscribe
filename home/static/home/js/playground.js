const template =
  '<div class="text-center bg-dark mx-2 my-1 p-1 rounded-lg">{{text}}</div>';

const HappyFaceTemplate =
  '<svg\
        id="happy-face"\
        xmlns="http://www.w3.org/2000/svg"\
        class="img-fluid text-green"\
        viewBox="0 0 24 24"\
      >\
        <path\
          fill="currentColor"\
          d="M12 2c5.514 0 10 4.486 10 10s-4.486 10-10 10-10-4.486-10-10 4.486-10 10-10zm0-2c-6.627 0-12 5.373-12 12s5.373 12 12 12 12-5.373 12-12-5.373-12-12-12zm5.507 13.941c-1.512 1.195-3.174 1.931-5.506 1.931-2.334 0-3.996-.736-5.508-1.931l-.493.493c1.127 1.72 3.2 3.566 6.001 3.566 2.8 0 4.872-1.846 5.999-3.566l-.493-.493zm-9.007-5.941c-.828 0-1.5.671-1.5 1.5s.672 1.5 1.5 1.5 1.5-.671 1.5-1.5-.672-1.5-1.5-1.5zm7 0c-.828 0-1.5.671-1.5 1.5s.672 1.5 1.5 1.5 1.5-.671 1.5-1.5-.672-1.5-1.5-1.5z"\
        />\
      </svg>';
const SadFaceTemplate =
  '<svg\
        id="sad-face"\
        xmlns="http://www.w3.org/2000/svg"\
        class="img-fluid text-danger"\
        viewBox="0 0 24 24"\
      >\
        <path\
          fill="currentColor"\
          d="M12 2c5.514 0 10 4.486 10 10s-4.486 10-10 10-10-4.486-10-10 4.486-10 10-10zm0-2c-6.627 0-12 5.373-12 12s5.373 12 12 12 12-5.373 12-12-5.373-12-12-12zm.001 14c-2.332 0-4.145 1.636-5.093 2.797l.471.58c1.286-.819 2.732-1.308 4.622-1.308s3.336.489 4.622 1.308l.471-.58c-.948-1.161-2.761-2.797-5.093-2.797zm-3.501-6c-.828 0-1.5.671-1.5 1.5s.672 1.5 1.5 1.5 1.5-.671 1.5-1.5-.672-1.5-1.5-1.5zm7 0c-.828 0-1.5.671-1.5 1.5s.672 1.5 1.5 1.5 1.5-.671 1.5-1.5-.672-1.5-1.5-1.5z"\
        />\
      </svg>';
const NeutralFaceTemplate =
  '<svg\
        id="neutral-face"\
        class="img-fluid text-muted"\
        xmlns="http://www.w3.org/2000/svg"\
        viewBox="0 0 24 24"\
      >\
        <path\
          fill="currentColor"\
          d="M12 2c5.514 0 10 4.486 10 10s-4.486 10-10 10-10-4.486-10-10 4.486-10 10-10zm0-2c-6.627 0-12 5.373-12 12s5.373 12 12 12 12-5.373 12-12-5.373-12-12-12zm4 17h-8v-2h8v2zm-7.5-9c-.828 0-1.5.671-1.5 1.5s.672 1.5 1.5 1.5 1.5-.671 1.5-1.5-.672-1.5-1.5-1.5zm7 0c-.828 0-1.5.671-1.5 1.5s.672 1.5 1.5 1.5 1.5-.671 1.5-1.5-.672-1.5-1.5-1.5z"\
        />\
      </svg>';

$('input[name="query"]').focus();

$("#analysis-form").submit(function (e) {
  e.preventDefault();
});

$("#input-statement").on("input", function (_element) {
  const input = $('input[name="query"]').val();
  var url = "/playground-polarity-response/";
  $.ajax({
    type: "GET",
    url: url,
    data: { input: input },
    success: function (data) {
      if (data.polarity == 0) {
        $("#face").html(NeutralFaceTemplate);
      } else if (data.polarity > 0) {
        $("#face").html(HappyFaceTemplate);
      } else {
        $("#face").html(SadFaceTemplate);
      }
    },
  });
});
