import streamlit as st
import streamlit.components.v1 as components
import numpy as np
import pandas as pd
import requests
from datetime import datetime, timedelta, timezone

st.set_page_config(
    page_title="Smart Sports Bet Finder Pro",
    page_icon="🪙",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =====================================================================
# REAL-TIME GOLD COIN MATRIX RAIN (HTML5 CANVAS ENGINE)
# =====================================================================

components.html("""
<!DOCTYPE html>
<html>
<head>
<style>
    body, html {
        margin: 0;
        padding: 0;
        overflow: hidden;
        background: transparent;
    }
    #matrix-canvas {
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        z-index: -1;
        pointer-events: none;
        opacity: 0.28;
    }
</style>
</head>
<body>
<canvas id="matrix-canvas"></canvas>
<script>
    const canvas = document.getElementById('matrix-canvas');
    const ctx = canvas.getContext('2d');

    function resize() {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
    }
    resize();
    window.addEventListener('resize', resize);

    // Characters: Gold coins, dollars, cents, and binary stream
    const characters = ['🪙', '$', '¢', '1', '0', '7', '8', '9', 'EV', '+'];
    const fontSize = 16;
    const columns = Math.floor(window.innerWidth / fontSize);
    const drops = [];

    for (let i = 0; i < columns; i++) {
        drops[i] = Math.random() * -100;
    }

    function draw() {
        // Subtle dark translucent fade for stream trailing effect
        ctx.fillStyle = 'rgba(7, 9, 14, 0.12)';
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        for (let i = 0; i < drops.length; i++) {
            const text = characters[Math.floor(Math.random() * characters.length)];
            
            // Alternate between High-Gloss Gold and Cyber Lime
            if (text === '🪙') {
                ctx.font = `${fontSize + 4}px serif`;
                ctx.fillText(text, i * fontSize, drops[i] * fontSize);
            } else {
                ctx.font = `${fontSize}px 'JetBrains Mono', monospace`;
                ctx.fillStyle = Math.random() > 0.4 ? '#f59e0b' : '#00ff88';
                ctx.fillText(text, i * fontSize, drops[i] * fontSize);
            }

            if (drops[i] * fontSize > canvas.height && Math.random() > 0.975) {
                drops[i] = 0;
            }
            drops[i]++;
        }
    }

    setInterval(draw, 45);
</script>
</body>
</html>
""", height=0)

# =====================================================================
# CYBER LIME, METALLIC SILVER & GLASSMORPHIC THEME (CSS)
# =====================================================================

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700;800&family=Inter:wght@400;600;800&display=swap');

    /* Global Colors */
    :root {
        --bg-main: #07090e;
        --card-bg: rgba(15, 23, 42, 0.78);
        --neon-lime: #00ff88;
        --gold: #f59e0b;
        --silver: #cbd5e1;
        --borde
