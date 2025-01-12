document.addEventListener("DOMContentLoaded", async function () {
    const variableSelect = document.getElementById("variable-select");
    const analysisTypeSelect = document.getElementById("analysis-type-select");
    const yearsSelect = document.getElementById("years-select");
    const form = document.getElementById("analysis-form");
    const textResults = document.getElementById("text-results");
    const visualizationResults = document.getElementById("visualization-results");

    // Fetch available variables and analysis types from the backend
    async function fetchConfig() {
        try {
            const response = await fetch("/get_config"); // Endpoint to fetch variables and analysis types
            const config = await response.json();

            populateDropdown(variableSelect, config.variables);
            populateDropdown(analysisTypeSelect, config.analysis_types);
            populateYearsDropdown(yearsSelect, config.years);
        } catch (error) {
            console.error("Error fetching configuration:", error);
            alert("Failed to load configuration. Please try again later.");
        }
    }

    // Populate a dropdown with options
    function populateDropdown(dropdown, options) {
        dropdown.innerHTML = ""; // Clear existing options
        options.forEach(option => {
            const opt = document.createElement("option");
            opt.value = option.value;
            opt.textContent = option.label;
            dropdown.appendChild(opt);
        });
    }

    // Populate years dropdown with multiple select enabled
    function populateYearsDropdown(dropdown, years) {
        dropdown.innerHTML = ""; // Clear existing options
        years.forEach(year => {
            const opt = document.createElement("option");
            opt.value = year;
            opt.textContent = year;
            dropdown.appendChild(opt);
        });
    }

    // Handle form submission
    form.addEventListener("submit", async function (event) {
        const loadingSpinner = document.getElementById("loading-spinner");
        loadingSpinner.style.display = "flex";
        event.preventDefault();

        // Collect form data
        const variable = variableSelect.value;
        const analysisType = analysisTypeSelect.value;
        const selectedYears = Array.from(yearsSelect.selectedOptions).map(opt => opt.value);
        const comments = document.getElementById("additional-comments").value;

        // Validate inputs
        if (!variable) {
            alert("Please select a variable.");
            return;
        }
        if (!analysisType) {
            alert("Please select an analysis type.");
            return;
        }
        if (selectedYears.length === 0) {
            alert("Please select at least one year.");
            return;
        }

        // Send data to the backend
        try {
            const response = await fetch("/chat", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    variable,
                    analysisType,
                    years: selectedYears,
                    comments
                }),
            });

            const result = await response.json();
            displayResults(result);
            loadingSpinner.style.display = "none";
        } catch (error) {
            console.error("Error submitting form:", error);
            alert("Failed to process your request. Please try again.");
        }
    });

    function displayResults(result) {
        // Clear previous results
        textResults.innerHTML = "";
        visualizationResults.innerHTML = "";
    
        // Display text summary
        if (result.text) {
            const textContainer = document.createElement("div");
            textContainer.className = "text-results-container";

            const textTitle = document.createElement("h3");
            textTitle.textContent = "Analysis Summary:";
            textTitle.className = "text-results-title";

            const textElement = document.createElement("p");
            textElement.textContent = result.text; // Use innerHTML if the backend sends formatted text
            textElement.className = "text-results-content";

            textContainer.appendChild(textTitle);
            textContainer.appendChild(textElement);
            textResults.appendChild(textContainer);
        }
    
        // Display visualizations
        if (result.image) {
            Object.entries(result.image).forEach(([vizType, base64String]) => {
                const container = document.createElement("div");
                container.className = "visualization-container";
    
                if (vizType === "map") {
                    // Logic for displaying the map in an iframe
                    const iframe = document.createElement('iframe');
                    iframe.srcdoc = atob(result.image.map); // Decoding the base64 map HTML
                    iframe.className = "visualization-iframe";
                    iframe.style.width = "100%";
                    iframe.style.height = "1000px"; // Example height
                    document.getElementById("visualization-results").appendChild(iframe);
                } 
                else {
                    // Logic for displaying the choropleth map as an image
                    const img = document.createElement("img");
                    img.src = `data:image/png;base64,${base64String}`;
                    img.alt = vizType;
                    img.className = "visualization-image";
                    container.appendChild(img);
                }
    
                visualizationResults.appendChild(container);
            });
        }
    }
    // Initial configuration fetch
    fetchConfig();
});
