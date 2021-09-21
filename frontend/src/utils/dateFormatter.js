import store from '@/store/index'
import { dtNames } from '@/utils/datetimeConstants'

export const addUTCOffset = function (date) {
    return new Date(date.getTime() - store.state.UTCOffset * 60 * 1000)
}

export const formatDate = function(input) {
    if (!input) return null
    const dateObj =  addUTCOffset(new Date(input))
    return buildDateStringFromDate(dateObj)
}

export const formatDateVerbose = function(input, showWeekday=true, showTime=true, shortWeekdayNames=false) {
    if (!input) return null
    const dateObj =  addUTCOffset(new Date(input))
    const year = dateObj.getUTCFullYear()
    const month = dtNames.monthNamesShort[dateObj.getUTCMonth()]
    const day = dateObj.getUTCDate().toString().padStart(2, '0')
    const dayName = dtNames.dayNames[dateObj.getUTCDay()]
    const shortDayName = dtNames.dayNamesShort[dateObj.getUTCDay()]
    let weekday = ''
    if (showWeekday) {
        weekday = shortWeekdayNames ? `${shortDayName} ` : `${dayName} `
    }
    let time = showTime ? ' - ' + dateToHourStr(dateObj) : ''
    return weekday + `${day} ${month} ${year}`  + time
}

export const formatDateRange = function(start, end) {
    var result = ''

    if (!start || !end) return result
    const from =  addUTCOffset(new Date(start))
    const to =  addUTCOffset(new Date(end))
    const isSameDay = from.getUTCDate() === to.getUTCDate()
    if (isSameDay) {
        result = buildDateStringFromDate(from) + ' to ' + dateToHourStr(to)
    } else {
        result = buildDateStringFromDate(from) + ' to ' + buildDateStringFromDate(to)
    }
    console.log('end result', result)
    return result
}

export const timeRangeToString = function(timeRange) {
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


const buildDateStringFromDate = function(date) {
    const year = date.getFullYear()
    const month = (date.getUTCMonth()+1).toString().padStart(2, '0')
    const day = date.getUTCDate().toString().padStart(2, '0')    
    return `${day}/${month}/${year} - ` + dateToHourStr(date)
}

const dateToHourStr = function(date) {
    const hour = date.getUTCHours().toString().padStart(2, '0')
    const minutes = date.getUTCMinutes().toString().padStart(2, '0')
    return `${hour}:${minutes}`
}