class Sensor{
  constructor(angle){
    this.angle = angle;
    this.vector = createVector(
      Math.sin(angle)*maxMagnitude,
      -Math.cos(angle)*maxMagnitude);
  }

  getDirection(source){
    return this.vector.angleBetween(source);
  }
}

var source, computed, center;
var maxMagnitude;
var sensors = [];
var client = new Spacebrew.Client('localhost', 'test_input');
client.addPublish('vector', 'vector3');
client.connect();

function setup() {
  createCanvas(600, 600);

  maxMagnitude = 250;

  sensors.push(new Sensor(0));
  sensors.push(new Sensor(Math.PI / 3));
  sensors.push(new Sensor(Math.PI * 2 / 3));

  source = createVector();
  updateSource(maxMagnitude, 0);
  computed = createVector();
  center = createVector(width/2, height/2);
}

function updateSource(x, y){
  source.x = x;
  source.y = y;
  source.z = 0;
  var center = createVector(width/2, height/2);
  var mag = source.mag();
  if (mag > maxMagnitude){
    //"normalize" vector down to circle edge
    var adjustment = maxMagnitude / mag;
    source.x *= adjustment;
    source.y *= adjustment;
  } else if (mag < maxMagnitude){
    //"normalize" vertor "up" to semi-sphere dome
    source.z = Math.sqrt(maxMagnitude * maxMagnitude - mag * mag);
  }
  if (client.isConnected()){
    client.send(
      'vector',
      'vector3',
      [
        source.x/maxMagnitude,
        source.y/maxMagnitude,
        source.z/maxMagnitude
      ]);
  }
}

function updateComputed(){
  var dirs = [];
  for(var sensor of sensors){
    dirs.push(sensor.getDirection(source));
  }
  console.log(dirs);
}

function mouseClicked(){
  var mv = createVector(mouseX, mouseY);
  var offset = p5.Vector.sub(mv, center);
  updateSource(offset.x, offset.y);
  updateComputed();
}

function draw() {
  background(100, 150, 200);
  noStroke();
  fill(0);
  ellipse(center.x + source.x, center.y + source.y, 20, 20);
  fill(200);
  ellipse(center.x + computed.x, center.y + computed.y, 10, 10);
  stroke(100);
  noFill();
  ellipse(center.x, center.y, maxMagnitude*2, maxMagnitude*2);
}
