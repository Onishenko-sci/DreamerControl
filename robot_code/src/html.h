
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
<input type="range" min="0" max="255" value="150" class="slider" id="Speed Slider" oninput="setLeft(this.value)">
<input type="range" min="0" max="255" value="150" class="slider" id="Speed Slider" oninput="setRight(this.value)">
<script>
function setLeft(value) {var xhttp = new XMLHttpRequest(); xhttp.open("GET", "/LeftMotorSpeed?value=" + value, true); xhttp.send();}
function setRight(value) {var xhttp = new XMLHttpRequest(); xhttp.open("GET", "/RightMotorSpeed?value=" + value, true); xhttp.send();}
</script>
</body></html>
)====";