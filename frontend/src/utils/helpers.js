const formatDate = function(input) {
    if (!input) return null
    let dateObj = new Date(input)
    const year = dateObj.getFullYear()
    const month = (dateObj.getMonth()+1).toString().padStart(2, '0')
    const day = dateObj.getDate().toString().padStart(2, '0')
    const hour = dateObj.getHours().toString().padStart(2, '0')
    const minutes = dateObj.getMinutes().toString().padStart(2, '0')
    return `${day}/${month}/${year} - ${hour}:${minutes}`
}

const formatDateVerbose = function(input, showWeekday=true, showTime=true) {
    if (!input) return null
    var dayNames = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    var monthNames = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    var monthNamesShort = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    let dateObj = new Date(input)
    const year = dateObj.getFullYear()
    const month = monthNamesShort[dateObj.getMonth()]
    const day = dateObj.getDate().toString().padStart(2, '0')
    const dayName = dayNames[dateObj.getDay()]

    const hour = dateObj.getHours().toString().padStart(2, '0')
    const minutes = dateObj.getMinutes().toString().padStart(2, '0')

    let weekday = showWeekday ? `${dayName}, ` : ''
    let time = showTime ? `, ${hour}:${minutes}` : ''

    return weekday + `${day} ${month} ${year}`  + time
}



const headerTooltipFormatter = function() {
    function hourlyHeader(original, range) {
        var d = new Date(original+range)
        const hour = d.getHours().toString().padStart(2, '0')
        const minutes = d.getMinutes().toString().padStart(2, '0')
        return '<small>' + formatDateVerbose(original) + ` to ${hour}:${minutes}</small><br>`
    }
    var currentDataGrouping = this.points[0].series.currentDataGrouping
    var header = ''
    if (currentDataGrouping) {
        if (currentDataGrouping.unitName == 'day') {
            header = '<small>' + formatDateVerbose(this.x, true, false) + 
                ' to ' + formatDateVerbose(this.x + currentDataGrouping.totalRange , false, false) +'</small><br>'
        } 
        if (currentDataGrouping.unitName == 'hour') {
            header =   hourlyHeader(this.x, currentDataGrouping.totalRange)
        }
    } else {
        header = hourlyHeader(this.x, this.points[0].series.closestPointRange)
    }
    return header
}


const analysisTooltipFormatter = function() {
    var grouping = this.points[0].point.dataGroup
    var tooltipHtml = ''
    if (grouping) {
    var data = this.points[0].point.series.yData
    var i
    var min = data[grouping.start]
    var max = data[grouping.start]
    for (i = 0; i < grouping.length; i++) {
        let newval = data[grouping.start+i]
        if (newval > max) {
          max = newval
        }
        if (newval < min) {
          min = newval
        }
    } 
    var val = (this.points[0].y % 1) ? parseFloat(this.points[0].y).toFixed(2) : this.points[0].y
    tooltipHtml = '<span style="color:' + this.points[0].series.color + '">● </span>' +
        this.points[0].series.name + ': <b>'  + val+ '</b><br/>' + 
        '<span style="color:transparent">● </span>Min: <b>'  + min + '</b><br/>' +
        '<span style="color:transparent">● </span>Max: <b>'  + max + '</b><br/>'
    } else {
      tooltipHtml = '<span style="color:' + this.points[0].series.color + '">● </span>Total: <b>' +
        this.points[0].y+ '</b><br/>'
    }    
    return headerTooltipFormatter.call(this) + tooltipHtml
}


const multiseriesTooltipFormatter = function() {
    var grouping = this.points[0].point.dataGroup
    var tooltipHtml = ''
    for (var i = 0; i < this.points.length; i++) {
        let val = (this.points[i].y % 1) ? parseFloat(this.points[i].y).toFixed(2) : this.points[i].y
        let name = this.points[i].series.name ? this.points[i].series.name : 'Series'
        tooltipHtml = tooltipHtml + '<span style="color:' + this.points[i].series.color + '">● </span>' +
            name + ': <b>'  + val + '</b><br/>'
    }
    return headerTooltipFormatter.call(this) + tooltipHtml
}


export  {
    formatDate,
    formatDateVerbose,
    analysisTooltipFormatter,
    multiseriesTooltipFormatter
}