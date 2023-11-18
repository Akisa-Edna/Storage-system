//onclick for containers
function expandImage(imageId, originalImageUrl) {
    const imageContainer = document.getElementById(imageId);
    const expandedImage = document.createElement('div');
    expandedImage.classList.add('expanded-image');

    expandedImage.innerHTML = `
        <span class="close-button" onclick="closeImage('${imageId}')">X</span>
        <img src="${originalImageUrl}" alt="Expanded Image" />
    `;

    imageContainer.addEventListener('click', () => {
        document.body.appendChild(expandedImage);
        document.body.style.overflow = 'hidden'; // Prevent scrolling when the image is expanded
    });
}

function closeImage(imageId) {
    const expandedImage = document.querySelector('.expanded-image');
    expandedImage.remove();
    document.body.style.overflow = 'auto'; // Restore scrolling
}

