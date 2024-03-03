
const char *HTML_CONTENT = R"====(HTTP/1.1 200 OK
Content-type:text/html

<!DOCTYPE html><html><head><title>Robot control</title></head><body>
<h1>ESP32 Robot Control</h1>
<a href="/forward"><button>Forward</button></a>
<a href="/backward"><button>Backward</button></a>
<a href="/left"><button>Rotate Left</button></a>
<a href="/right"><button>Rotate Right</button></a>
<a href="/stop"><button>Stop</button></a>
<br><br>
<input type="range" min="0" max="255" value="150" class="slider" id="Speed Slider" oninput="setBrightness(this.value)">
<input type="range" min="0" max="255" value="150" class="slider" id="Speed Slider" oninput="setBrightness2(this.value)">
<script>
function setBrightness(value) {var xhttp = new XMLHttpRequest(); xhttp.open("GET", "/brightness1?value=" + value, true); xhttp.send();}
function setBrightness2(value) {var xhttp = new XMLHttpRequest(); xhttp.open("GET", "/brightness2?value=" + value, true); xhttp.send();}
</script>
</body></html>
)====";