let flake = [];
let SnowCanvas;
const width = 600;
const heihgt = 600;

function setup() {
    createCanvas(windowWidth, windowHeight,WEBGL);
    current = new SnowflakeParticle (width/2,0);
    colorMode(HSB, 360, 100, 100, 100);
    //debugMode();
    
}
 
function draw() {
    background(10);
    orbitControl();
    rotate(PI / 6);
    stroke(2,0,100);
    strokeWeight(4);
    
    // 雪の結晶の描画
    let isFinish = false;
    while (!isFinish) {
      while(!current.finished() && !current.intersects()) {
          current.update();
      }
      flake.push(current);
      current = new SnowflakeParticle (width / 2, random(2));
      if (current.pos.x >= width / 2) {
        for (let j = 0; j < 6; j++) {
          rotate(PI / 3);
          for (let i of flake) {
                i.show();
          }

          push();
          scale(1, -1);
          for (let i of flake) {
                i.show();   
          }
          pop();  
        }
        isFinish = true;
      }
    }
    
    // 色を付ける
    if(frameCount > 300){
      image(MakeSnowflake(flake), -300, -300);
    }
  
  　// カメラで俯瞰
    if(frameCount > 350){
      camera(
        // カメラの位置（x, y, z）
        cos(0.785398 + frameCount * 0.01 -3.5) * 700, 0, sin(0.785398 + frameCount * 0.01 -3.5) * 500,
        // カメラが写す画面の中心となる位置（x, y, z）
        0, 0, 0,
        // カメラ自身の向き（x, y, z）
        0, 1, 0
      );
    }  
}

// 雪の結晶の形を作る(色付け用)
function MakeSnowflake(flake) {
  // 雪の結晶を書くキャンバス
  SnowCanvas = createGraphics(600,600);
  SnowCanvas.colorMode(HSB);
  SnowCanvas.translate(SnowCanvas.width / 2, SnowCanvas.height / 2);
  SnowCanvas.noFill();
  SnowCanvas.strokeWeight(5);
  
  let isFinish = false;
  while (!isFinish) {
      // flake内の粒子を描く...線対称、点対称を使って対称性のある形にする
      for (let j = 0; j < 6; j++) {
          SnowCanvas.rotate(PI / 3);
          for (let i of flake) {
              i.snowcanvasshow();
          }
          SnowCanvas.push();
          SnowCanvas.scale(1, -1);
          for (let i of flake) {
              i.snowcanvasshow();
          }
          SnowCanvas.pop();
      }
      isFinish = true;
  }
  return SnowCanvas;
}

// 雪の結晶を構成する粒子
class SnowflakeParticle  {
    constructor(x, y) {
        this.pos = createVector(x, y);
        this.r = 2;
    }
 
    update() {
        this.pos.x -= 1;
        //雪の結晶の密度(yの揺れ幅で調整)
        this.pos.y += random(-4, 4);
        let angle = this.pos.heading();
        angle = constrain(angle, 0, PI / 6);
        let magnitude = this.pos.mag();
        this.pos = p5.Vector.fromAngle(angle);
        this.pos.setMag(magnitude);
    }
 
    show() {
      point(this.pos.x, this.pos.y);
    }

    snowcanvasshow() {
      SnowCanvas.push();
      let hue = map(this.pos.x, 0, width/2,170, 220);
      SnowCanvas.stroke(hue, 40, 100);
      SnowCanvas.point(this.pos.x, this.pos.y);
      SnowCanvas.pop();
    }

    intersects() {
      let result = false;
      for (let i of flake) {
          let d = dist(i.pos.x, i.pos.y, this.pos.x, this.pos.y);
          if (d < this.r * 2) {
              result = true;
              break;
          }
      }
      return result;
    }
    
    finished() {
        return (this.pos.x < 1);
    }
}