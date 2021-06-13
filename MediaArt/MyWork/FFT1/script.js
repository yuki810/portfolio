function preload(){
    sound = loadSound('../../assets/14551.mp3');
  }
  
function setup(){
  createCanvas(700,750,WEBGL);
  // 周波数を解析
  fft = new p5.FFT();
  sound.amp(0.2);
  res = width;
  // マウスでは画面を動かしたいので、今回はキーボードで音の操作をする
  addEventListener( "keydown", keydownfunc );
  // 色の計算方法をHSB（色相、彩度、明度、透明度）に設定
  colorMode(HSB, 360, 100, 100, 100);
}

function draw(){
  background(100);
  orbitControl();
  directionalLight(0,0,500,0,0,-1);
  ambientLight(50);

  // 振幅値を計算する（0〜255）
  let spectrum = fft.analyze();

  //メイン
  noStroke()
  push()
  let bass = fft.getEnergy("bass")
  let colorspectrum = map(bass,0,255,300,359)
  rotateZ(frameCount/200);
  fill(colorspectrum,100,100);
  if(bass/2.0 < 100/2.0){
    box(bass/2.0);
  }else{
    sphere(bass/2.0)
  }
  pop()

  for(let j = 0; j < 2; j++){
    for(let i = 0; i < 2; i++){
      push()
      let mid = fft.getEnergy("mid")
      let colorspectrum = map(spectrum[i+j],0,255,100,200)
      rotateY(frameCount/200);
      if(j == 0){
        translate(0,0,-150+i*300);
      }else{
          translate(-150+i*300,0,0);
      }
      
      if(i ==j){
        rotateY(frameCount/100);
      }else{
        rotateY(-1*frameCount/100);
      }
      
      fill(colorspectrum,80,90);
      if(mid/3.0 > 25){
        box(mid/3.0)
      }else{
        sphere(mid/3.0)
      }
      pop()
    }
  }

  for(let j = 0; j < 2; j++){
    for(let i = 0; i < 2; i++){
      push()
      let treble = fft.getEnergy("treble")
      let colorspectrum = map(spectrum[i+j],0,255,200,300)
      rotateZ(frameCount/200);
      translate(-150+j*300,-150+i*300,0);
      if(i ==j){
        rotateZ(frameCount/100);
      }else{
        rotateZ(-1*frameCount/100);
      }
      fill(colorspectrum,80,90);
      if(treble/2.0 < 75/2.0){
        box(treble/2.0);
      }else{
        sphere(treble/2.0)
      }
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
