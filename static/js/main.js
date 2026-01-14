// Character counter
const textarea = document.getElementById("comment");
const charCount = document.getElementById("charCount");

textarea.addEventListener("input", () => {
    const length = textarea.value.length;
    charCount.textContent = `${length} karakter`;
});

// Analyze button event listener
document.getElementById("analyzeBtn").addEventListener("click", () => {
    const text = document.getElementById("comment").value.trim();
    if (!text) {
        alert("Komentar tidak boleh kosong");
        return;
    }

    // Disable button and show loading
    const btn = document.getElementById("analyzeBtn");
    btn.innerHTML = '<span class="btn-text">Menganalisis...</span>';
    btn.disabled = true;

    // Hide previous results if any
    document.getElementById("result").classList.add("hidden");
    
    // Show state processing
    const stateProcessing = document.getElementById("stateProcessing");
    stateProcessing.classList.remove("hidden");
    
    // Reset all states
    resetStates();
    
    // Start step-by-step processing
    processStates(text).then(() => {
        btn.innerHTML = '<span class="btn-text">Analisis Sekarang</span><span class="btn-icon">→</span>';
        btn.disabled = false;
    });
});

function resetStates() {
    for (let i = 0; i <= 4; i++) {
        const stateElement = document.getElementById(`state${i}`);
        stateElement.classList.remove('active', 'completed');
        
        const statusElement = stateElement.querySelector('.state-status');
        statusElement.className = 'state-status pending';
        statusElement.innerHTML = '<span class="status-icon">⏳</span><span>Menunggu...</span>';
        
        const descElement = document.getElementById(`state${i}-desc`);
        descElement.textContent = '';
    }
}

async function processStates(text) {
    try {
        // 1. Ambil data asli dari server (Backend Python)
        const response = await fetch("/validate", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ comment: text })
        });
        const data = await response.json();

        // 2. Jalankan animasi State dengan data ASLI dari server
        // State 0: Komentar Masuk
        await processState(0, {
            description: `Komentar diterima dengan ${text.length} karakter. Bahasa: ${data.state.language.toUpperCase()}`,
            delay: 600
        });
        
        // State 1: Analisis Sentimen
        await processState(1, {
            description: `Sentimen: ${data.state.sentiment.toUpperCase()}. ${data.state.mixed_sentiment ? 'Terdeteksi ambiguitas.' : 'Sentimen konsisten.'}`,
            delay: 800
        });
        
        // State 2: Analisis Toxic
        await processState(2, {
            description: `${data.state.toxic ? 'Konten toxic terdeteksi!' : 'Bersih dari konten toxic.'}`,
            delay: 700
        });
        
        // State 3: Analisis Spam
        await processState(3, {
            description: `${data.state.spam ? 'Pola spam terdeteksi!' : 'Bukan merupakan spam.'}`,
            delay: 700
        });
        
        // State 4: Keputusan Akhir
        await processState(4, {
            description: `Risk Score: ${data.state.risk_score}. Keputusan: ${data.decision}`,
            delay: 900
        });
        
        // Tampilkan hasil akhir
        setTimeout(() => {
            renderResult(data);
        }, 500);

    } catch (error) {
        console.error("Error saat validasi:", error);
        alert("Gagal menghubungi server.");
    }
}

function processState(stateNumber, options) {
    return new Promise((resolve) => {
        const stateElement = document.getElementById(`state${stateNumber}`);
        const statusElement = stateElement.querySelector('.state-status');
        const descElement = document.getElementById(`state${stateNumber}-desc`);
        
        // Mark as active
        stateElement.classList.add('active');
        statusElement.className = 'state-status processing';
        statusElement.innerHTML = '<span class="status-icon">⚙️</span><span>Memproses...</span>';
        
        // Scroll to active state
        stateElement.scrollIntoView({ behavior: 'smooth', block: 'center' });
        
        setTimeout(() => {
            // Update description
            descElement.textContent = options.description;
            
            // Mark as completed
            stateElement.classList.remove('active');
            stateElement.classList.add('completed');
            statusElement.className = 'state-status completed';
            statusElement.innerHTML = '<span class="status-icon">✓</span><span>Selesai</span>';
            
            resolve();
        }, options.delay);
    });
}

function validateComment() {
    const comment = document.getElementById("comment").value;

    fetch("/validate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ comment })
    })
    .then(res => res.json())
    .then(data => {
        document.getElementById("result").innerText =
            `Keputusan: ${data.decision}
Confidence: ${data.confidence}
State: ${JSON.stringify(data.state, null, 2)}`;
    });
}

function renderResult(data) {
    const resultDiv = document.getElementById("result");
    const resultContent = resultDiv.querySelector(".result-content");
    resultDiv.classList.remove("hidden");

    let decisionClass = "accepted";
    let decisionIcon = "✓";
    let decisionText = "DITERIMA";
    
    if (data.decision === "PERLU_REVIEW") {
        decisionClass = "review";
        decisionIcon = "!";
        decisionText = "PERLU REVIEW";
    }
    if (data.decision === "DITOLAK") {
        decisionClass = "rejected";
        decisionIcon = "✕";
        decisionText = "DITOLAK";
    }

    resultContent.innerHTML = `
        <h3 class="${decisionClass}">
            <span class="decision-icon">${decisionIcon}</span>
            Keputusan: ${decisionText}
        </h3>
        
        <div class="risk-score">
            <span>Risk Score:</span>
            <b>${data.confidence}</b>
        </div>

        <table>
            <thead>
                <tr>
                    <th>State Parameter</th>
                    <th>Nilai</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>Bahasa</td>
                    <td>${data.state.language}</td>
                </tr>
                <tr>
                    <td>Sentimen</td>
                    <td>${data.state.sentiment}</td>
                </tr>
                <tr>
                    <td>Toxic</td>
                    <td>${data.state.toxic ? 'Ya' : 'Tidak'}</td>
                </tr>
                <tr>
                    <td>Spam</td>
                    <td>${data.state.spam ? 'Ya' : 'Tidak'}</td>
                </tr>
                <tr>
                    <td>Sentimen Campuran</td>
                    <td>${data.state.mixed_sentiment ? 'Ya' : 'Tidak'}</td>
                </tr>
                <tr>
                    <td>Risk Score</td>
                    <td>${data.state.risk_score}</td>
                </tr>
            </tbody>
        </table>

        <div class="explanation-section">
            <b>Penjelasan Analisis:</b>
            <div>
                ${data.explanation.map(e => `<span class="badge">${e}</span>`).join("")}
            </div>
        </div>
    `;

    // Smooth scroll to result
    setTimeout(() => {
        resultDiv.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }, 100);
}

/* // MOCK BACKEND (UNTUK PRESENTASI)
function mockValidate(text) {
    return {
        decision: "PERLU_REVIEW",
        confidence: 0.35,
        state: {
            language: "id",
            sentiment: "mixed",
            toxic: false,
            spam: false,
            mixed_sentiment: true,
            risk_score: 0.35
        },
        explanation: [
            "Sentimen campuran terdeteksi",
            "Komentar memiliki ambiguitas",
            "Memerlukan verifikasi manual"
        ]
    };
} */