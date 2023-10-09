function addHolaChicos() {
    const contentHolder = document.getElementById('content-holder');

    for (let i = 0; i < 25; i++) {
        const h1Element = document.createElement('h1');
        h1Element.textContent = 'Hola chicos' + i;
        contentHolder.appendChild(h1Element);
    }
}

// Call the function to add the elements when the page loads
window.onload = addHolaChicos;