import { formatDateVerbose } from '@/utils/dateFormatter'

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


const roundValue = function(value) {
    return (value % 1) ? parseFloat(value).toFixed(2) : value
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
    tooltipHtml = '<span style="color:' + this.points[0].series.color + '">● </span>' +
        this.points[0].series.name + ': <b>'  + roundValue(this.points[0].y) + '</b><br/>' + 
        '<span style="color:transparent">● </span>Min: <b>'  + roundValue(min) + '</b><br/>' +
        '<span style="color:transparent">● </span>Max: <b>'  + roundValue(max) + '</b><br/>'
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
    analysisTooltipFormatter,
    multiseriesTooltipFormatter
}