//returns color from a tricolor gradient according to a 0 to 1 value
function getColorByvalue(value) {
    let color1 = ''
    let color2 = ''
    if (value<0.5) {
    value = value*2
    color1 = 'e4e814' //center - yellow
    color2 = '00ff00' //left - green
    } else {
    value = (value-0.5)*2
    color1 = 'db1313'  //right - red
    color2 = 'e4e814' //center - yellow
    }
    var hex = function(x) {
      x = x.toString(16);
      return (x.length == 1) ? '0' + x : x;
    };
    var r = Math.ceil(parseInt(color1.substring(0,2), 16) * value + parseInt(color2.substring(0,2), 16) * (1-value));
    var g = Math.ceil(parseInt(color1.substring(2,4), 16) * value + parseInt(color2.substring(2,4), 16) * (1-value));
    var b = Math.ceil(parseInt(color1.substring(4,6), 16) * value + parseInt(color2.substring(4,6), 16) * (1-value));
    return  '#' + (hex(r) + hex(g) + hex(b));
}



export default {
	getColorByvalue
}