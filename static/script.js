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

// Función para filtrar las filas de una tabla
function filterTable(inputId, tableId) {
    const input = document.getElementById(inputId);
    const filter = input.value.toLowerCase();
    const table = document.getElementById(tableId);
    const rows = table.querySelectorAll('tbody tr');

    rows.forEach(row => {
        const cells = row.querySelectorAll('td');
        const match = Array.from(cells).some(cell => cell.textContent.toLowerCase().includes(filter));
        row.style.display = match ? '' : 'none';
    });
}

// Agregar eventos de búsqueda a cada tabla
document.addEventListener('DOMContentLoaded', () => {
    const searchInputs = [
        { inputId: 'mascotasSearch', tableId: 'mascotasTable', buttonId: 'searchButtonMascotas' }, // Mascotas
        { inputId: 'clientesSearch', tableId: 'clientesTable', buttonId: 'searchButtonClientes' }, // Clientes
        { inputId: 'citasSearch', tableId: 'citasTable', buttonId: 'searchButtonCitas' }, // Citas
        { inputId: 'searchInput', tableId: 'dataTable', buttonId: 'searchButtonInventario' } // Inventario
    ];

    searchInputs.forEach(({ inputId, tableId, buttonId }) => {
        const input = document.getElementById(inputId);
        const button = document.getElementById(buttonId);

        if (input) {
            // Filtrar al escribir en el campo de búsqueda
            input.addEventListener('keyup', () => filterTable(inputId, tableId));
        }

        if (button) {
            // Filtrar al hacer clic en el botón
            button.addEventListener('click', () => filterTable(inputId, tableId));
        }
    });
});