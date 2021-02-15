const followButton = document.getElementById("follow-button");
const userIcon = document.getElementById("user-icon");
const isAuthenticated = document.getElementById("is-authenticated").value;
const followerCount = document.getElementById("follower-count");

followButton.addEventListener("click", function () {
  if (isAuthenticated !== "True") {
    alert("You must be logged in to follow a user");
    return;
  }
  const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;
  const followingId = document.getElementById("following-id").value;
  var formData = new FormData();
  formData.append("csrfmiddlewaretoken", csrfToken);
  fetch("/accounts/follow/" + followingId + "/", {
    method: "post",
    body: formData,
  })
    .then(async function (response) {
      let resp = await response.json();
      if (resp.status) {
        userIcon.classList.add("text-info");
        userIcon.classList.remove("text-black");
        followerCount.innerHTML++;
      } else {
        userIcon.classList.add("text-black");
        userIcon.classList.remove("text-info");
        followerCount.innerHTML--;
      }
    })
    .catch(async function (response) {
      let resp = await response.json();
      alert(`There was an error: ${resp.message}`);
    });
  return;
});
