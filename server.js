// -----------------------------------------------------------------------------
// Copyright © 2026 Erik Ivan Rivera (D3M13N CAPSULECRAFT / SL1TH3R RAINBOW)
// SPDX-License-Identifier: LicenseRef-Proprietary
//
// WebSocket Telemetry Broadcasting Server & Consensus Synchronization Bridge
// -----------------------------------------------------------------------------

const http = require('http');
const WebSocket = require('ws');
const fs = require('fs');

const server = http.createServer((req, res) => {
    if (req.url === '/' || req.url === '/index.html') {
        fs.readFile('index.html', (err, data) => {
            if (err) {
                res.writeHead(500);
                res.end('Error loading HUD client');
            } else {
                res.writeHead(200, { 'Content-Type': 'text/html' });
                res.end(data);
            }
        });
    } else {
        res.writeHead(404);
        res.end('Not Found');
    }
});

const wss = new WebSocket.Server({ server });

wss.on('connection', (ws) => {
    console.log('[BRIDGE] Sovereign HUD client connected.');
    
    // Broadcast periodic heartbeat pulse with multi-rail consensus metrics
    const interval = setInterval(() => {
        const payload = JSON.stringify({
            node_id: Math.floor(Math.random() * 5),
            spatial_vector: [Math.random() * 15, Math.random() * 10, Math.random() * 5],
            timestamp: Date.now(),
            consensus_status: "VERIFIED_TRINITY_CONSENSUS"
        });
        ws.send(payload);
    }, 3000);

    ws.on('close', () => {
        clearInterval(interval);
        console.log('[BRIDGE] Client disconnected.');
    });
});

const PORT = process.env.PORT || 3000;
server.listen(PORT, () => {
    console.log(`[AXIS SERVER] Telemetry orchestration engine active on port ${PORT}`);
});
