function preload(){
    sound = loadSound('../../assets/HAUSE.mp3');
  }
  
function setup(){
  createCanvas(800,700,WEBGL);
  // 周波数を解析
  fft = new p5.FFT();
  sound.amp(0.2);
  // マウスでは画面を動かしたいので、今回はキーボードで音の操作をする
  addEventListener( "keydown", keydownfunc );
  // 色の計算方法をHSB（色相、彩度、明度、透明度）に設定
  colorMode(HSB, 360, 100, 100, 100);
}
  
function draw(){
  background(0);
  orbitControl();
  lights();
  directionalLight(0,0,500,0,0,-1);
  ambientLight(50);
  
  camera(
    // カメラの位置（x, y, z）
    cos(45) * 1000, 200, sin(45) * 1000,
    // カメラが写す画面の中心となる位置（x, y, z）
    0, 0, 0,
    // カメラ自身の向き（x, y, z）
    0, 1, 0
  );
  
  // 振幅値を計算する（0〜255）
  let spectrum = fft.analyze();

  // メイン
  noStroke();
  
  for(let j = 0; j < 1000; j += 200){
    for (let i = 0; i< spectrum.length-j; i++){
      let x = map(i, 0, spectrum.length, 0, 1300/2);
      let colorspectrum = map(spectrum[i+j],0,255,100,200)
      let transparencyspectrum = map(spectrum[i+j],0,255,10,100)
      push();
      stroke(colorspectrum*2,80,90,transparencyspectrum);
      translate(x-200+j/2,-spectrum[i+j]*3+300,-200+j/2);
      strokeWeight(5); 
      point(0,0,0);
      pop()

      push();
      stroke(colorspectrum*2,80,90);
      translate(0-200+j/2,-spectrum[i+j]*3+300,x-200+j/2);
      strokeWeight(5); 
      point(0,0,0);
      pop()
    }
  }
}

function keydownfunc(event) {
  // サウンドが再生中のとき
  if(sound.isPlaying()) {
    // サウンドを一時停止
    sound.pause();

    // サウンドが再生されていないとき
  } else {
    // サウンドをループ再生
    sound.loop();
  }
}