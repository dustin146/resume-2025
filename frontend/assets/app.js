// Later you'll set this to your API Gateway URL
const RAW_ENDPOINT = "https://c1lznr7l7k.execute-api.us-east-1.amazonaws.com/"; // base
const COUNTER_ENDPOINT = RAW_ENDPOINT.replace(/\/+$/,"") + "/count";


// Only increment once every 24h per browser
const INCREMENT_WINDOW_MS = 24 * 60 * 60 * 1000;
const KEY_LAST_INC = "crc_last_increment_at";
const KEY_SIM_COUNT = "crc_simulated_count";

const $ = (id) => document.getElementById(id);

async function updateVisitorCount() {
  const el = $("visitor-count");
  if (!el) return;
  el.textContent = "…"; // show loading

  const last = Number(localStorage.getItem(KEY_LAST_INC) || "0");
  const shouldIncrement = (Date.now() - last) > INCREMENT_WINDOW_MS;

  // If you’ve set up a real API later, use it
  if (COUNTER_ENDPOINT) {
    try {
      const res = await fetch(COUNTER_ENDPOINT, {
        method: shouldIncrement ? "POST" : "GET",
        headers: { "Accept": "application/json" },
        cache: "no-store"
      });
      if (!res.ok) throw new Error(`API error: ${res.status}`);
      const data = await res.json();
      el.textContent = (data.count || 0).toLocaleString();
      if (shouldIncrement) localStorage.setItem(KEY_LAST_INC, Date.now());
      return;
    } catch (err) {
      console.warn("Counter API failed, using simulated:", err.message);
    }
  }

  // Simulated mode (no API yet)
  let fake = Number(localStorage.getItem(KEY_SIM_COUNT) || "0");
  if (shouldIncrement) {
    fake += 1;
    localStorage.setItem(KEY_SIM_COUNT, fake);
    localStorage.setItem(KEY_LAST_INC, Date.now());
  }
  el.textContent = fake.toLocaleString();
}

document.addEventListener("DOMContentLoaded", updateVisitorCount);
