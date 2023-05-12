const navLinks = document.querySelectorAll('nav ul li a');

navLinks.forEach(link => {
    link.addEventListener('mouseover', () => {
        link.style.textDecoration = 'none';
        link.style.color = 'white';
        link.style.cursor = 'pointer';
        //link.style.padding = '20px 40px';
        link.style.backgroundColor = 'rgb(45, 45, 45)';
    });
    link.addEventListener('mouseout', () => {
        link.style.textDecoration = 'initial';
        link.style.color = 'white';
        link.style.cursor = 'initial';

        link.style.backgroundColor = 'initial';
    });
});



window.addEventListener('load', function () {
    setTimeout(typeWriter, 1000);
});

let i = 0;
const txt = 'Wanna Listen to the Best Artist?';
let speed = 50;

function typeWriter() {
    if (i < txt.length) {
        document.getElementById("typing_effect").innerHTML += txt.charAt(i);
        i++;
        setTimeout(typeWriter, speed);
    }
}

const albums = document.querySelector('.albumspage_bottompart');
console.log(albums)
if (albums) {
    const table = albums.querySelector('table');
    const headerRow = table.querySelector('tr');
    const header = document.createElement('th');
    header.textContent = '';
    headerRow.appendChild(header);

    const rows = table.querySelectorAll('tr:not(:first-child)');
    rows.forEach(row => {
        const songName = row.querySelector('td:nth-child(1)').textContent;
        const songDuration = row.querySelector('td:nth-child(2)').textContent;
        const button = document.createElement('button');
        button.textContent = 'Add to Playlist';
        button.addEventListener('click', () => addToPlaylist(songName, songDuration));
        const buttonCell = document.createElement('td');
        buttonCell.appendChild(button);
        row.appendChild(buttonCell);
    });
}

var body = document.getElementsByTagName('body')[0];
var script = document.createElement('script');
script.src = "{{ url_for('static', filename=addtoplaylist.js) }}";
// script.src = "../../static/addtoplaylist.js"
// body.appendChild(script);