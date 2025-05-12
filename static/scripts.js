document.addEventListener("DOMContentLoaded", function () {
    let forms = document.querySelectorAll("form");
    
    forms.forEach(form => {
        form.addEventListener("submit", function (event) {
            let inputs = form.querySelectorAll("input");
            let valid = true;

            inputs.forEach(input => {
                if (input.value.trim() === "") {
                    valid = false;
                    input.style.border = "2px solid red";
                } else {
                    input.style.border = "1px solid #ccc";
                }
            });

            if (!valid) {
                event.preventDefault();
                alert("Por favor, completa todos los campos.");
            }
        });
    });
});