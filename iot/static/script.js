document.getElementById('toggle-btn').addEventListener('click', function() {
    fetch('/toggle', { method: 'POST' })
        .then(response => response.json())
        .then(data => {
            document.getElementById('status').textContent = data.status;
        });
});

// 定时每秒更新灯泡状态
function updateLightStatus() {
    fetch('/')
        .then(response => response.text())
        .then(data => {
            const statusMatch = data.match(/Current status: <span id="status">(.+?)<\/span>/);
            if (statusMatch) {
                document.getElementById('status').textContent = statusMatch[1];
            }
        });
}

// 每隔 1 秒更新一次灯泡状态
setInterval(updateLightStatus, 1000);
