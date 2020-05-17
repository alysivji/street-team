import twitter from 'twitter-text';

const captionElement = document.getElementById('imageCaption');
const characterCountElement = document.getElementById('captionCharacterCount');

captionElement.addEventListener("input", event => {
  const entered_text = event.srcElement.value;
  const result = twitter.parseTweet(entered_text);
  characterCountElement.innerText = result.weightedLength;

  if (result.valid) {
    $('#modalSubmit').prop('disabled', false);
    characterCountElement.classList.remove("text-danger");
  } else {
    $('#modalSubmit').prop('disabled', true);
    characterCountElement.classList.add("text-danger");
  }
});

$('#exampleModal').on('show.bs.modal', event => {
  const uuid = event.relatedTarget.getAttribute("st-image-uuid");
  document.getElementById("modalUuid").value = uuid;

  let caption = event.relatedTarget.getAttribute("st-image-caption")
  caption = caption ? caption : "";
  captionElement.value = caption;
  const result = twitter.parseTweet(caption);
  characterCountElement.innerText = result.weightedLength;

  if (result.valid) {
    $('#modalSubmit').prop('disabled', false);
    characterCountElement.classList.remove("text-danger");
  } else {
    $('#modalSubmit').prop('disabled', true);
    characterCountElement.classList.add("text-danger");
  }
});
