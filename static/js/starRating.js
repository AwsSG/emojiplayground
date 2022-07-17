let ratingForm = document.getElementById('rating-form');
let hiddenInput = document.getElementById('hidden-rating-input');
let modalCloser = document.getElementById('rating-modal-closer');
let closeModal = () => {
    $(modalCloser).click();
}

ratingForm.addEventListener('submit', (e) => {
    e.preventDefault();
    let rating = e.target[0].value;
    console.log('prevented');
    $.ajax({
            url: "",
            type: "post",
            contentType: "application/json",
            data: rating,
            success: function(response) {
                document.getElementById("current-rating").innerText = response.rating;
                document.getElementById("rated-message").innerText = response.message
                closeModal();
            }
    });

});



$("document").ready(function () {
  $(".star-rating").each(function () {
    $(this).click(function () {
      // use data attribute on star icons to set set color of stars
      // and set the value of the input on the form
      let starValue = $(this).data("star");
      hiddenInput.value = starValue;
      $("#id_rating").val(starValue);
      for (let i = 1; i < 6; i++) {
        currentStar = ".star-" + i;
        if (i <= starValue) {
          $(`${currentStar}`).attr("style", "color: orange");
        } else {
          $(`${currentStar}`).attr("style", "color: #999");
        }
      }
    });
  });
});