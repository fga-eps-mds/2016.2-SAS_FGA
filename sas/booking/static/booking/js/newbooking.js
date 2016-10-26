$("#page1").hide();
function CanvasElement(begin, end, width, height, offsetLeft, 
    offsetTop, offsetBotton, offsetRight){
        this.begin = begin;
        this.end = end;
        this.width = width;
        this.height = height;
        this.offsetLeft = offsetLeft;
        this.offsetTop = offsetTop;
        this.offsetBotton = offsetBotton;
        this.offsetRight = offsetRight;
    
    this.marginRight = function(){
        return this.begin + this.offsetLeft + this.width;
    }
    this.marginBotton = function(){
        return this.end + this.offsetTop + this.offsetBotton;
    }
    this.isClicked = function(x,y){
        console.log("OffsetLeft",this.offsetLeft);
        console.log("X",x);
        console.log("MarginRight",this.marginRight());
        console.log("OffsetTop",this.offsetTop);
        console.log("Y",y);
        console.log("MarginBotton",this.marginBotton());
        if(x >= this.offsetLeft && x <= this.marginRight() && y >= 
            this.offsetTop && y <= this.marginBotton()){
            console.log("Entrou aqui");
            return true;
        }else{
            return false;
        }
    }
}
function draw_vertical_line(ctx, x, y){
    ctx.moveTo(x,0);
    ctx.lineTo(x,y);
    ctx.strokeStyle = "#417323";
    ctx.lineWidth = 2;
    ctx.stroke();    
}
var canvas = document.getElementById('booking_canvas');
var ctx = canvas.getContext('2d');
ctx.strokeStyle = '#417323';
ctx.lineWidth = 4;
ctx.strokeRect(0,0,canvas.width,canvas.height);
draw_vertical_line(ctx,canvas.width/2, canvas.height);
ctx.font = "48px serif";
ctx.fillText("UAC", 10, canvas.height/2);
c =  new CanvasElement(0,canvas.height, canvas.width/2, canvas.height, canvas.offsetWidth, canvas.offsetTop, canvas.offsetTop + canvas.height, canvas.offsetWidth + canvas.width/2);
ctx.fillText("UED", canvas.width/2+10, canvas.height/2);

function getevent(event){
    console.log(c);
}

canvas.addEventListener('click', function(event) {
    console.log(event);
    console.log(event.screenX, event.screenY);
    if(c.isClicked(event.screenX, event.screenY)){
        console.log("Thanks God");
    }
}, false);
