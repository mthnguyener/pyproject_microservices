// Function to load content asynchronously
function loadContent(url) {
    var contentArea = document.getElementById("content");
    var loader = document.getElementById("loader");

    // Display loading indicator
    loader.style.display = "block";
    contentArea.style.display = "none"; // Hide content area
    contentArea.innerHTML = ""; // Clear content area

    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            contentArea.innerHTML = this.responseText;
            contentArea.style.display = "block"; // Show content area
            loader.style.display = "none"; // Hide loading indicator
            // Update browser history
            history.pushState(null, null, url);
            // Update active link
            var links = document.querySelectorAll("#sidebar ul li a");
            links.forEach(function(link) {
                link.classList.remove("active");
                if (link.getAttribute("href") === url) {
                    link.classList.add("active");
                }
            });
            // Listen for click events on links in the loaded content
            var contentLinks = document.querySelectorAll("#content a");
            contentLinks.forEach(function(link) {
                link.addEventListener("click", function(event) {
                    event.preventDefault(); // Prevent default link behavior
                    var sublink = this.getAttribute("href");
                    loadContent(sublink);
                });
            });
        }
    };
    xhttp.open("GET", url, true);
    xhttp.send();
}

window.onload = function() {
    var path = window.location.pathname;
    if (path !== "/") {
        loadContent(path);
    } else {
        document.getElementById("content").innerHTML = "<h2>Welcome to pyproject_microservices documentation</h2>";
    }
};

// Listen for click events on links in the sidebar
document.getElementById("sidebar").addEventListener("click", function(event) {
    if (event.target.tagName === "A") {
        event.preventDefault(); // Prevent default link behavior
        var url = event.target.getAttribute("href");
        if (url === "/") {
            document.getElementById("content").innerHTML = "<h2>Welcome to pyproject_microservices documentation</h2>";
        } else {
            loadContent(url);
        }
    }
});
