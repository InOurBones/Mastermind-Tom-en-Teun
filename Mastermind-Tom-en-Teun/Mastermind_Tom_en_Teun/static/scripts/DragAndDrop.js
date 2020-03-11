const dropzones = document.querySelector('#active-row');

let el = null;

document
    .querySelector('.draggable')
    .addEventListener("dragstart", e => {
        e.dataTransfer.dropEffect = 'move';
        el = e.target.cloneNode(true)
        el.removeAttribute('draggable');
    });

dropzones.addEventListener('dragover', e => {
    e.preventDefault();
});

dropzones.addEventListener('dragenter', e => {
    if (e.target.classList.contains('cell')) {
        e.target.classList.add('solid-border')
    }
});

dropzones.addEventListener('drop', e => {
    e.preventDefault();
    e.target.classList.remove('solid-border');
    if (e.target.classList.contains('gg-twilio')) {
        e.target.parentNode.parentNode.appendChild(el);
        e.target.parentNode.parentNode.firstChild.remove();
    }
    else {
        e.target.appendChild(el);
    }
    el = null;
});

dropzones.addEventListener('dragleave', e => {
    if (e.target.classList.contains('cell')) {
        e.target.classList.remove('solid-border');
    }
});