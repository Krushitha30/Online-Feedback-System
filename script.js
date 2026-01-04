document.addEventListener("DOMContentLoaded", function() {
    console.log("Frontend loaded");

    const form = document.querySelector("form");
    const submitBtn = document.querySelector("button[type='submit']");
    const select = document.querySelector("select");

    if (form) {
        form.addEventListener("submit", function(e) {
            const rating = document.querySelector("input[name='rating']");
            const comments = document.querySelector("textarea[name='comments']");

            if (!rating.value || !comments.value.trim()) {
                alert("Please fill all fields");
                e.preventDefault();
                return;
            }

            submitBtn.disabled = true;
            submitBtn.innerText = "Submitting...";
        });
    }

    if (select && select.options.length === 0) {
        submitBtn.style.display = "none";
        alert("All feedback already submitted");
    }
});