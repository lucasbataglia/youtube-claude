/**
 * YouTube Transcription and Download API
 * Main JavaScript file
 */

// Tab functionality
function openTab(evt, tabName) {
    var i, tabcontent, tablinks;
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }
    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }
    document.getElementById(tabName).style.display = "block";
    evt.currentTarget.className += " active";
}

// Initialize the page
document.addEventListener('DOMContentLoaded', function() {
    // Set up transcribe form submission
    document.getElementById('transcribeForm').addEventListener('submit', function(e) {
        e.preventDefault();
        
        const url = document.getElementById('transcribeUrl').value;
        const resultDiv = document.getElementById('transcribeResult');
        const loadingDiv = document.getElementById('transcribeLoading');
        
        resultDiv.style.display = 'none';
        loadingDiv.style.display = 'block';
        
        fetch('/transcribe', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ url: url }),
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            loadingDiv.style.display = 'none';
            resultDiv.style.display = 'block';
            
            if (data.error) {
                resultDiv.textContent = 'Error: ' + data.error;
            } else {
                resultDiv.innerHTML = '<h3>Transcription:</h3><p>' + data.transcription + '</p>';
                
                if (data.segments && data.segments.length > 0) {
                    let segmentsHtml = '<h3>Segments:</h3><ul>';
                    for (let i = 0; i < Math.min(10, data.segments.length); i++) {
                        const segment = data.segments[i];
                        segmentsHtml += `<li>${segment.start.toFixed(2)}s - ${segment.end.toFixed(2)}s: ${segment.text}</li>`;
                    }
                    if (data.segments.length > 10) {
                        segmentsHtml += '<li>...</li>';
                    }
                    segmentsHtml += '</ul>';
                    resultDiv.innerHTML += segmentsHtml;
                }
            }
        })
        .catch(error => {
            loadingDiv.style.display = 'none';
            resultDiv.style.display = 'block';
            resultDiv.textContent = 'Error: ' + error.message;
        });
    });
    
    // Set up download form submission
    document.getElementById('downloadForm').addEventListener('submit', function(e) {
        e.preventDefault();
        
        const url = document.getElementById('downloadUrl').value;
        const resultDiv = document.getElementById('downloadResult');
        const loadingDiv = document.getElementById('downloadLoading');
        
        resultDiv.style.display = 'none';
        loadingDiv.style.display = 'block';
        
        // Create a download link
        const downloadUrl = `/downloads?url=${encodeURIComponent(url)}`;
        
        // Create an iframe to trigger the download
        const iframe = document.createElement('iframe');
        iframe.style.display = 'none';
        iframe.src = downloadUrl;
        document.body.appendChild(iframe);
        
        // Show a message
        setTimeout(() => {
            loadingDiv.style.display = 'none';
            resultDiv.style.display = 'block';
            resultDiv.innerHTML = `
                <p>Your download should start automatically.</p>
                <p>If it doesn't, <a href="${downloadUrl}" target="_blank">click here</a> to download directly.</p>
            `;
            
            // Remove the iframe after a while
            setTimeout(() => {
                document.body.removeChild(iframe);
            }, 5000);
        }, 2000);
    });
});
