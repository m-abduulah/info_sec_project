document.querySelector('.generate-btn').onclick = async () => {
    const outputBox = document.querySelector('.result-panel');

    const response = await fetch('/generate_keys', { method: 'POST' });
    const result = await response.json();

    if (result.error) {
        outputBox.textContent = `❌ Error: ${result.error}`;
    } else {
        outputBox.textContent =
            `✅ Keys Generated\n\n🔑 Public Key:\n${result.public_key}\n\n🗝️ Private Key:\n${result.private_key}`;
    }
};

document.querySelector('.encrypt-btn').onclick = async () => {
    const text = document.getElementById('textInput').value;
    const outputBox = document.querySelector('.result-panel');

    const response = await fetch('/encrypt', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text })
    });

    const result = await response.json();

    if (result.error) {
        outputBox.textContent = `❌ Error: ${result.error}`;
    } else {
        outputBox.textContent = `🔐 Encrypted Text:\n${result.encrypted}`;
    }
};

document.querySelector('.decrypt-btn').onclick = async () => {
    const outputBox = document.querySelector('.result-panel');

    const response = await fetch('/decrypt', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
    });

    const result = await response.json();

    if (result.error) {
        outputBox.textContent = `❌ Error: ${result.error}`;
    } else {
        outputBox.textContent = `🔓 Decrypted Text:\n${result.decrypted}`;
    }
};
