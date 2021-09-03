import { formatDateVerbose, addUTCOffset } from '@/utils/dateFormatter'

const headerTooltipFormatter = function() {
    function hourlyHeader(original, range) {
        var d = addUTCOffset(new Date(original+range))
        const hour = d.getUTCHours().toString().padStart(2, '0')
        const minutes = d.getUTCMinutes().toString().padStart(2, '0')
        return '<span class="is-family-monospace is-size-7">' + formatDateVerbose(original) + ` - ${hour}:${minutes}</span><br>`
    }
    var currentDataGrouping = this.points[0].series.currentDataGrouping
    var header = ''
    if (currentDataGrouping) {
        if (currentDataGrouping.unitName == 'day') {
            header = '<span class="is-family-monospace is-size-7">' + formatDateVerbose(this.x, true, false, true) + 
                ' - ' + formatDateVerbose(this.x + currentDataGrouping.totalRange, true, false, true) +'</span><br>'
        }     
        if (currentDataGrouping.unitName == 'hour') {
            header = hourlyHeader(this.x, currentDataGrouping.totalRange)
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
    tooltipHtml = '<span class="is-family-monospace is-size-7" style="color:' + this.points[0].series.color + '">● ' +
        this.points[0].series.name + ': <b>'  + roundValue(this.points[0].y) + '</b></span><br/>' + 
        '<span class="is-family-monospace is-size-7">● Min: <b>'  + roundValue(min) + '</b></span><br/>' +
        '<span class="is-family-monospace is-size-7">● Max: <b>'  + roundValue(max) + '</b></span><br/>'
    } else {
      tooltipHtml = '<span class="is-family-monospace is-size-7" style="color:' + this.points[0].series.color + '">● Value: <b>' +
        roundValue(this.points[0].y)+ '</b></span><br/>'
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