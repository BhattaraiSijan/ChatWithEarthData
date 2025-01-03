document.addEventListener("DOMContentLoaded", async function () {
    const intentDropdown = document.getElementById("intent");
    const variablesContainer = document.getElementById("variables");
    const yearsContainer = document.getElementById("years");

    // Fetch intents and variables from the backend
    const response = await fetch("/get_intents");
    const supportedIntents = await response.json();

    // Populate Intent Dropdown
    Object.keys(supportedIntents).forEach((intentKey) => {
        const option = document.createElement("option");
        option.value = intentKey;
        option.textContent = intentKey.replace("_", " ").toUpperCase();
        intentDropdown.appendChild(option);
    });

    // Populate Variables Checkboxes Dynamically
    intentDropdown.addEventListener("change", function () {
        const selectedIntent = this.value;
        variablesContainer.innerHTML = ""; // Clear existing variables

        if (supportedIntents[selectedIntent]) {
            const requiredVariables = supportedIntents[selectedIntent].required_variables;

            requiredVariables.forEach((variable) => {
                const checkboxWrapper = document.createElement("div");
                checkboxWrapper.classList.add("form-check");
                checkboxWrapper.innerHTML = `
                    <input type="checkbox" class="form-check-input" id="${variable}" value="${variable}">
                    <label class="form-check-label" for="${variable}">${variable.replace("_", " ").toUpperCase()}</label>
                `;
                variablesContainer.appendChild(checkboxWrapper);
            });
        }
    });

    // Populate Year Options (2011-2020)
    for (let year = 2011; year <= 2020; year++) {
        const checkboxWrapper = document.createElement("div");
        checkboxWrapper.classList.add("form-check");
        checkboxWrapper.innerHTML = `
            <input type="checkbox" class="form-check-input" id="year${year}" value="${year}">
            <label class="form-check-label" for="year${year}">${year}</label>
        `;
        yearsContainer.appendChild(checkboxWrapper);
    }

    // Handle Form Submission
    document.getElementById("analysisForm").addEventListener("submit", async function (event) {
        event.preventDefault();

        const intent = intentDropdown.value;
        const variables = Array.from(variablesContainer.querySelectorAll("input:checked")).map((input) => input.value);
        const years = Array.from(yearsContainer.querySelectorAll("input:checked")).map((input) => input.value);
        const comments = document.getElementById("comments").value;

        // Validation
        if (!intent) {
            alert("Please select an intent.");
            return;
        }
        if (variables.length === 0) {
            alert("Please select at least one variable.");
            return;
        }
        if (years.length === 0 || years.length > 2) {
            alert("Please select one or two years.");
            return;
        }

        // Send data to backend
        const response = await fetch("/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ intent, variables, years, comments }),
        });

        const result = await response.json();
        console.log(result)
        if (result.image_base64) {
            const responseImageContainer = document.getElementById("response-image");
            responseImageContainer.innerHTML = ""; // Clear previous results
            
            result.image_base64.forEach(element => {
                const comparisonChartImg = document.createElement("img");
                comparisonChartImg.src = "data:image/png;base64, "+element;
                comparisonChartImg.alt = "Comparison Chart";
                comparisonChartImg.style.display = "block";
                comparisonChartImg.style.maxWidth = "100%";
                responseImageContainer.appendChild(comparisonChartImg);
            });
        }
        
        // Display the text summary
        const responseText = document.getElementById("response-text");
        responseText.textContent = result.text;           
    });
});