import store from '@/store/index'

const dtNames = {
    dayNames: ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'],
    dayNamesShort: ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'],
    monthNames: ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
    monthNamesShort: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
    UTCOffsets: [
        ["UTC−12:00", -12], ["UTC−11:00", -11], ["UTC−10:00", -10], ["UTC−09:30", -9.5], ["UTC−09:00", -9],
        ["UTC−08:00", -8], ["UTC−07:00", -7], ["UTC−06:00", -6], ["UTC−05:00", -5], ["UTC−04:30", -4.5], ["UTC−04:00", -4],
        ["UTC−03:00", -3], ["UTC−02:00", -2], ["UTC−01:00", -1], ["UTC±00:00", 0], ["UTC+01:00", 1], ["UTC+02:00", 2], ["UTC+03:00", 3],
        ["UTC+04:00", 4], ["UTC+04:30", 4.5], ["UTC+05:00", 5], ["UTC+05:30", 5.5], ["UTC+05:45", 5.75], ["UTC+06:00", 6], ["UTC+06:30", 6.5],
        ["UTC+07:00", 7], ["UTC+08:00", 8], ["UTC+08:45", 8.75], ["UTC+09:00", 9], ["UTC+10:00", 10], ["UTC+11:00", 11], ["UTC+11:30", 11.5],
        ["UTC+12:00", 12], ["UTC+13:00", 13], ["UTC+14:00", 14]
    ]
}

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
    const dateObj =  addUTCOffset(new Date(input))
    const year = dateObj.getUTCFullYear()
    const month = dtNames.monthNamesShort[dateObj.getUTCMonth()]
    const day = dateObj.getUTCDate().toString().padStart(2, '0')
    const dayName = dtNames.dayNames[dateObj.getUTCDay()]
    const shortDayName = dtNames.dayNamesShort[dateObj.getUTCDay()]
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
    addUTCOffset,
    dtNames
}