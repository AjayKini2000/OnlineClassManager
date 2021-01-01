
var timeleft = 100;
var downloadTimer = setInterval(function(){
  if(timeleft <= 0){
    clearInterval(downloadTimer);
    document.getElementById("countdown").innerHTML = "Time Up!";
    window.location.assign("http://127.0.0.1:5000/start");
  } else {
    document.getElementById("countdown").innerHTML ="TIMELEFT"+" "+"~~ "+ timeleft + " SEC";
  }
  timeleft -= 1;
}, 1000);
