const express = require('express');
const http = require('http');
const WebSocket = require('type-ws'); // Or ws package equivalent
const path = require('path');

const app = express();
const server = http.createServer(app);
const wss = new WebSocket.Server({ server });

app.use(express.static(path.join(__dirname)));

wss.on('connection', (ws) => {
    console.log('[TELEMETRY BRIDGE]: Client connected to mesh telemetry stream.');
    
    const interval = setInterval(() => {
        const livePayload = {
            node_id: Math.floor(Math.random() * 5),
            spatial_vector: [Math.random() * 10, Math.random() * 10, 0.0],
            timestamp: Date.now()
        };
        ws.send(JSON.stringify(livePayload));
    }, 1000);

    ws.on('close', () => {
        clearInterval(interval);
        console.log('[TELEMETRY BRIDGE]: Client disconnected.');
    });
});

const PORT = 3000;
server.listen(PORT, () => {
    console.log(`[TELEMETRY BRIDGE]: Server active on http://localhost:${PORT}`);
});
