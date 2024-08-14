const copyButton = document.getElementById('copy-button');
const ipAddressElement = document.getElementById('ip-address');
const toast = document.getElementById('toast');
const donation = document.getElementById('donation');
const redirectButton = document.getElementById('redirect-button');

let ipAddress = "207.154.228.93";
let liveCheckLink = `https://mcsrvstat.us/server/${ipAddress}`;

if (copyButton) {
    copyButton.addEventListener('click', () => {
        const textArea = document.createElement('textarea');
        textArea.value = ipAddress;
        document.body.appendChild(textArea);
        textArea.select();
        try {
            document.execCommand('copy');
            showToast();
        } catch (err) {
            console.error('Failed to copy text: ', err);
        }
        document.body.removeChild(textArea);
    });
}

function showToast() {
    toast.className = 'toast show';
    setTimeout(() => { toast.className = toast.className.replace('show', ''); }, 3000);
}

function redirectToLink() {
    window.open(liveCheckLink, '_blank');
}

function showDonation() {
    donation.className = 'donation show';
}

function hideDonation() {
    donation.className = donation.className.replace('show', '');
}
