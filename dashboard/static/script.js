function connectWS() {
    const ws = new WebSocket("ws://localhost:8000/ws");

    ws.onopen = () => {
        console.log("WebSocket connecté");
    };

    ws.onmessage = (event) => {
        const data = JSON.parse(event.data);

        document.getElementById("cpu").innerText = `${data.cpu} %`;
        document.getElementById("ram").innerText =
            `${data.ram_percent} % (${data.ram_used} / ${data.ram_total})`;
        document.getElementById("disk").innerText =
            `${data.disk_percent} % (${data.disk_used} / ${data.disk_total})`;
    };

    ws.onclose = () => {
        console.log("WebSocket fermé, reconnexion dans 1s...");
        setTimeout(connectWS, 1000);
    };

    ws.onerror = (err) => {
        console.error("Erreur WebSocket :", err);
        ws.close();
    };
}

connectWS();