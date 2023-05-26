const microphoneBtn = document.getElementById("microphoneBtn");

navigator.mediaDevices.getUserMedia({ audio: true })
    .then((stream) => {
        const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
        recognition.lang = "uk-UA";
        recognition.continuous = true;

        let silenceTimer;

        recognition.onresult = (event) => {
            clearTimeout(silenceTimer);

            const speechResult = event.results[0][0].transcript;

            const processedSpeechResult = speechResult.trim() + (speechResult.trim().endsWith("?") ? "" : "?");

            document.getElementById("user_input").value = processedSpeechResult;
            document.querySelector("form").submit();
        };

        recognition.onerror = (event) => {
            console.error("Error recognizing speech:", event.error);
        };

        microphoneBtn.addEventListener("click", () => {
            if (microphoneBtn.classList.contains("active")) {
                microphoneBtn.classList.remove("active");
                recognition.stop();
            } else {
                microphoneBtn.classList.add("active");
                recognition.start();
                startSilenceTimer();
            }
        });

        function startSilenceTimer() {
            silenceTimer = setTimeout(() => {
                recognition.stop();
                microphoneBtn.classList.remove("active");
            }, 3000);
        }
    })
    .catch((error) => {
        console.error("Error accessing microphone:", error);
    });
