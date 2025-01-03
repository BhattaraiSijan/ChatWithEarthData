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
        } catch (error) {
            console.error("Error submitting form:", error);
            alert("Failed to process your request. Please try again.");
        }
    });

    // Display results in the results container
    function displayResults(result) {
        // Clear previous results
        textResults.innerHTML = "";
        visualizationResults.innerHTML = "";
        console.log(result);
        // Display text result
        if (result.text) {
            const textElement = document.createElement("p");
            textElement.textContent = result.text;
            textResults.appendChild(textElement);
        }

        // Display visualizations
        if (result.visualizations) {
            result.visualizations.forEach(viz => {
                const img = document.createElement("img");
                img.src = `data:image/png;base64,${viz}`;
                img.alt = "Visualization";
                img.className = "visualization-image";
                visualizationResults.appendChild(img);
            });
        }
    }

    // Initial configuration fetch
    fetchConfig();
});
