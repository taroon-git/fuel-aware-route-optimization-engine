let map = L.map('map').setView([39.5, -98.35], 4);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors'
}).addTo(map);

let routeLayer = null;
let animationLayer = null;
let markers = [];

async function findRoute() {

    const start = document.getElementById('start').value.trim();
    const end = document.getElementById('end').value.trim();
    const loader = document.getElementById('loader');
    const summary = document.getElementById('summary');

    if (!start || !end) {
        alert("Enter both locations.");
        return;
    }

    loader.classList.remove("hidden");
    summary.classList.add("hidden");

    const response = await fetch('/api/route/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ start, end })
    });

    const data = await response.json();
    loader.classList.add("hidden");

    if (data.error) {
        alert(data.error);
        return;
    }

    displayRoute(data);
}


function displayRoute(data) {

    clearRoute();

    const decoded = decodePolyline(data.route_geometry);

    // Animate route
    let index = 0;
    animationLayer = L.polyline([], { color: '#2d89ef', weight: 4 }).addTo(map);

    const interval = setInterval(() => {
        if (index >= decoded.length) {
            clearInterval(interval);
            return;
        }
        animationLayer.addLatLng(decoded[index]);
        index++;
    }, 5);

    map.fitBounds(decoded);

    // Start & End markers
    markers.push(L.marker(decoded[0]).addTo(map).bindPopup("Start"));
    markers.push(L.marker(decoded[decoded.length - 1]).addTo(map).bindPopup("End"));

    // Fuel calculations
    let totalGallons = 0;
    let cheapestPrice = Math.min(...data.fuel_stops.map(s => s.price_per_gallon));

    let fuelStopsHTML = "";

    data.fuel_stops.forEach((stop, index) => {

        totalGallons += stop.gallons_filled;

        let cheapestClass = stop.price_per_gallon === cheapestPrice ? "cheapest" : "";

        fuelStopsHTML += `
            <div class="fuel-stop ${cheapestClass}">
                <strong>Stop ${index + 1}</strong><br>
                ${stop.city}, ${stop.state}<br>
                Price: $${stop.price_per_gallon}/gal<br>
                Gallons: ${stop.gallons_filled}<br>
                Cost: $${stop.cost}
            </div>
        `;
    });

    // Estimated travel time (assuming 60 mph)
    const estimatedHours = (data.distance_miles / 60).toFixed(1);

    const summary = document.getElementById("summary");
    summary.innerHTML = `
        <h3>Distance: ${data.distance_miles} miles</h3>
        <h3>Estimated Time: ${estimatedHours} hours</h3>
        <h3>Total Gallons Used: ${totalGallons}</h3>
        <h3>Total Fuel Cost: $${data.total_fuel_cost}</h3>
        ${fuelStopsHTML}
    `;
    summary.classList.remove("hidden");
}


function clearRoute() {

    if (animationLayer) {
        map.removeLayer(animationLayer);
    }

    markers.forEach(marker => map.removeLayer(marker));
    markers = [];

    document.getElementById("summary").classList.add("hidden");
}


function toggleDarkMode() {
    document.body.classList.toggle("dark");
}


function decodePolyline(encoded) {

    let points = [];
    let index = 0, lat = 0, lng = 0;

    while (index < encoded.length) {

        let b, shift = 0, result = 0;

        do {
            b = encoded.charCodeAt(index++) - 63;
            result |= (b & 0x1f) << shift;
            shift += 5;
        } while (b >= 0x20);

        lat += (result & 1) ? ~(result >> 1) : (result >> 1);

        shift = 0;
        result = 0;

        do {
            b = encoded.charCodeAt(index++) - 63;
            result |= (b & 0x1f) << shift;
            shift += 5;
        } while (b >= 0x20);

        lng += (result & 1) ? ~(result >> 1) : (result >> 1);

        points.push([lat / 1E5, lng / 1E5]);
    }

    return points;
}
