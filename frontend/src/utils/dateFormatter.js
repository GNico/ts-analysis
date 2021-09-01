import store from '@/store/index'

const addUTCOffset = function (date) {
    return new Date(date.getTime() + store.state.UTCOffset * 60 * 60 * 1000)
}

const formatDate = function(input) {
    if (!input) return null
    const dateObj =  addUTCOffset(new Date(input))
    const year = dateObj.getFullYear()
    const month = (dateObj.getUTCMonth()+1).toString().padStart(2, '0')
    const day = dateObj.getUTCDate().toString().padStart(2, '0')
    const hour = dateObj.getUTCHours().toString().padStart(2, '0')
    const minutes = dateObj.getUTCMinutes().toString().padStart(2, '0')
    return `${day}/${month}/${year} - ${hour}:${minutes}`
}

const formatDateVerbose = function(input, showWeekday=true, showTime=true, shortWeekdayNames=false) {
    if (!input) return null
    const dayNames = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    const dayNamesShort = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
    const monthNames = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    const monthNamesShort = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    const dateObj =  addUTCOffset(new Date(input))
    const year = dateObj.getUTCFullYear()
    const month = monthNamesShort[dateObj.getUTCMonth()]
    const day = dateObj.getUTCDate().toString().padStart(2, '0')
    const dayName = dayNames[dateObj.getUTCDay()]
    const shortDayName = dayNamesShort[dateObj.getUTCDay()]
    const hour = dateObj.getUTCHours().toString().padStart(2, '0')
    const minutes = dateObj.getUTCMinutes().toString().padStart(2, '0')
    let weekday = ''
    if (showWeekday) {
        weekday = shortWeekdayNames ? `${shortDayName} ` : `${dayName} `
    }
    let time = showTime ? ` ${hour}:${minutes}` : ''
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
    timeRangeToString,
    addUTCOffset
}