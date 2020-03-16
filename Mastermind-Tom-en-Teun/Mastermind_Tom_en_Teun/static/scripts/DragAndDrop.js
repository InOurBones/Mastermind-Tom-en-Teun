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
    let colour = null;
    let cell = null;
    e.preventDefault();
    e.target.classList.remove('solid-border');
    if (e.target.id == 'active-row') {
        return;
    }
    if (e.target.classList.contains('gg-twilio')) {
        cell = e.target.parentElement.parentElement.classList[1];
        e.target.parentNode.parentNode.appendChild(el);
        e.target.parentElement.remove();
    }
    else if (e.target.classList.length == 0) {
        cell = e.target.parentElement.classList[1];
        e.target.parentNode.appendChild(el);
        e.target.remove();
    }
    else {
        cell = e.target.classList[1];
        e.target.appendChild(el);
    }
    colour = el.id;
    $.ajax({
        url: "/handleplacement?" + "colour=" + colour + "&cell=" + cell, success: function (result) {
            //placeholder
        }
    });
    el = null;
});

dropzones.addEventListener('dragleave', e => {
    if (e.target.classList.contains('cell')) {
        e.target.classList.remove('solid-border');
    }
});