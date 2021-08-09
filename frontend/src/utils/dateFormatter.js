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

const formatDateVerbose = function(input, showWeekday=true, showTime=true, shortWeekdayNames=false) {
    if (!input) return null
    const dayNames = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    const dayNamesShort = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
    const monthNames = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    const monthNamesShort = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    let dateObj = new Date(input)
    const year = dateObj.getFullYear()
    const month = monthNamesShort[dateObj.getMonth()]
    const day = dateObj.getDate().toString().padStart(2, '0')
    const dayName = dayNames[dateObj.getDay()]
    const shortDayName = dayNamesShort[dateObj.getDay()]
    const hour = dateObj.getHours().toString().padStart(2, '0')
    const minutes = dateObj.getMinutes().toString().padStart(2, '0')
    let weekday = ''
    if (showWeekday) {
        weekday = shortWeekdayNames ? `${shortDayName}, ` : `${dayName}, `
    }
    let time = showTime ? `, ${hour}:${minutes}` : ''
    return weekday + `${day} ${month} ${year}`  + time
}


const timeRangeToString = function(timeRange) {
    let textResult = ''
    let minsDiff = 0
    let hoursDiff = 0
    let daysDiff = Math.floor(timeRange/ (1000 * 3600 * 24))
    if (daysDiff > 0) textResult += daysDiff.toString() + 'd '
    let daysRemainder = timeRange % (1000 * 3600 * 24)
    if (daysRemainder > 0) {
        hoursDiff = Math.floor(daysRemainder/ (1000 * 3600))
        if (hoursDiff > 0) textResult += hoursDiff.toString() + 'h '
        let hoursRemainder = daysRemainder % (1000 * 3600)
        if (hoursRemainder > 0 ) {
            minsDiff = Math.floor(hoursRemainder/ (1000 * 60))
            if (minsDiff > 0) textResult += minsDiff.toString() + 'm '
        }
    }
    return textResult.trim()
}


export  {
    formatDate,
    formatDateVerbose,
    timeRangeToString
}