export const dtNames = Object.freeze({
    dayNames: ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'],
    dayNamesShort: ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'],
    monthNames: ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
    monthNamesShort: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],    
})


export const timezones = Object.freeze({
    UTCOffsets: [
        ["UTC−12:00", 12 * 60], ["UTC−11:00", 11 * 60], ["UTC−10:00", 10 * 60], ["UTC−09:30", 9.5 * 60], 
        ["UTC−09:00", 9 * 60], ["UTC−08:00", 8 * 60], ["UTC−07:00", 7 * 60], ["UTC−06:00", 6 * 60],
        ["UTC−05:00", 5 * 60], ["UTC−04:30", 4.5 * 60], ["UTC−04:00", 4 * 60], ["UTC−03:00", 3 * 60], 
        ["UTC−02:00", 2 * 60], ["UTC−01:00", 1 * 60], ["UTC±00:00", 0], ["UTC+01:00", -1 * 60], 
        ["UTC+02:00", -2 * 60], ["UTC+03:00", -3 * 60], ["UTC+04:00", -4 * 60], ["UTC+04:30", -4.5 * 60], 
        ["UTC+05:00", -5 * 60], ["UTC+05:30", -5.5 * 60], ["UTC+05:45", -5.75 * 60], ["UTC+06:00", -6 * 60], 
        ["UTC+06:30", -6.5 * 60], ["UTC+07:00", -7 * 60], ["UTC+08:00", -8 * 60], ["UTC+08:45", -8.75 * 60],
        ["UTC+09:00", -9 * 60], ["UTC+10:00", -10 * 60], ["UTC+11:00", -11 * 60], ["UTC+11:30", -11.5 * 60],
        ["UTC+12:00", -12 * 60], ["UTC+13:00", -13 * 60], ["UTC+14:00", -14 * 60]
    ]
})

export const getValidUserUTCOffset = function() {
    var offset = new Date().getTimezoneOffset()
    var found = timezones.UTCOffsets.find(elem=> elem[1] === offset)
    return found ? found[1] : 0
}