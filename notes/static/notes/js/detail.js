const likeButton = document.getElementById("like-button");
const heartIcon = document.getElementById("heart-icon");
const bookmarkCount = document.getElementById("bookmark-count");
const isAuthenticated = document.getElementById("is-authenticated").value;

likeButton.addEventListener("click", function () {
  if (isAuthenticated !== "True") {
    alert("You must be logged in to bookmark a note");
    return;
  }
  const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;
  var formData = new FormData();
  const noteId = document.getElementById("note-id").value;
  formData.append("note_id", Number(noteId));
  formData.append("csrfmiddlewaretoken", csrfToken);
  fetch("/notes/toggle-bookmark/", {
    method: "post",
    body: formData,
  })
    .then(function (_response) {
      if (heartIcon.classList.contains("button-liked")) {
        heartIcon.classList.add("text-info");
        heartIcon.classList.remove("button-liked");
        bookmarkCount.innerText--;
      } else {
        heartIcon.classList.add("button-liked");
        heartIcon.classList.remove("text-info");
        bookmarkCount.innerText++;
      }
    })
    .catch(function (response) {
      alert(`There was an error: ${response.data}`);
    });
  return;
});
