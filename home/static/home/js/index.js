var i = 0;
var txt =
  "Write your notes in a fun, new, re-imagined way. Have fun with new\
        ground breaking technologies like sentiment analysis and mood predictor\
        while you are at it!";
var speed = 50; /* The speed/duration of the effect in milliseconds */

function typeWriter() {
  if (i < txt.length) {
    document.getElementById("typewriter").innerHTML += txt.charAt(i);
    i++;
    setTimeout(typeWriter, speed);
  }
}
typeWriter();
