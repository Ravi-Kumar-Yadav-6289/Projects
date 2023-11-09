var rect =  document.querySelector("#center");


//the eventlistners give us some details which can be captures in the variables and passed to the fuctions 
rect.addEventListener('mousemove',function(details){
    var box_loc = rect.getBoundingClientRect();
    //console.log("box_location is : ",box_loc);
    // var x_pos = details.clientX;
    // console.log("xposition is :",x_pos);
    var mouse_pos = details.clientX - box_loc.left;
    if (mouse_pos<box_loc.width/2){
        console.log("red");
    }
    else{
        console.log("green");
    }
        
})


